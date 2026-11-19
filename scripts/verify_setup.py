"""Read-only setup integrity checks; never execute the imported ML pipeline."""

import ast
import csv
import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(relative, expected):
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == expected, f"Unexpected schema: {relative}")
        rows = list(reader)
    require(all(None not in row and None not in row.values() for row in rows),
            f"Malformed CSV row: {relative}")
    return rows


def pair(row):
    return int(row["store_id"]), int(row["product_id"])


def key(row):
    return (*pair(row), row["dt"])


def main():
    manifest = json.loads((ROOT / "docs/handoff/import_manifest.json").read_text())
    require(len(manifest) == 10, "Expected ten original handoff files")
    for record in manifest:
        payload = (ROOT / record["current_original_destination"]).read_bytes()
        require(len(payload) == record["bytes"] == int(record["size"]),
                f"Byte mismatch: {record['dest']}")
        require(hashlib.sha256(payload).hexdigest() == record["sha256"],
                f"Hash mismatch: {record['dest']}")
    for record in manifest:
        working = ROOT / record["working_destination"]
        require(working.is_file(), f"Missing working copy: {working}")
        if working.suffix not in {".py", ".ipynb"}:
            require(hashlib.sha256(working.read_bytes()).hexdigest() == record["sha256"],
                    f"Canonical data/evidence changed: {working}")
    original = (ROOT / "docs/handoff/README.original.md").read_bytes()
    require(original.startswith((b"\xff\xfe", b"\xfe\xff")), "Missing UTF-16 BOM")
    reading = (ROOT / "docs/handoff/README.utf8.md").read_bytes().decode("utf-8")
    require(original.decode("utf-16") == reading, "Reading-copy text changed")
    print("PASS: ten original file hashes/byte counts and README encoding conversion")

    scripts = sorted(p for p in ROOT.rglob("*.py")
                     if not any(part in {".git", ".venv", "venv", "env", "__pycache__"}
                                for part in p.relative_to(ROOT).parts))
    for script in scripts:
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    notebook = json.loads((ROOT / "notebooks/DELTA_data/prepare_and_baselines.ipynb").read_text())
    require(notebook["nbformat"] == 4 and isinstance(notebook["metadata"], dict),
            "Unexpected notebook format")
    require(isinstance(notebook["cells"], list) and notebook["cells"], "No notebook cells")
    code_cells = 0
    for index, cell in enumerate(notebook["cells"]):
        require(cell["cell_type"] in {"code", "markdown", "raw"}, "Unknown cell type")
        require(isinstance(cell.get("metadata"), dict), "Missing cell metadata")
        source = cell["source"]
        require(isinstance(source, (str, list)), "Invalid cell source")
        if cell["cell_type"] == "code":
            require(isinstance(cell.get("outputs"), list), "Missing notebook outputs list")
            ast.parse("".join(source), filename=f"notebook cell {index}")
            code_cells += 1
    print(f"PASS: {len(scripts)} Python files parsed; notebook JSON/{len(notebook['cells'])} cells, "
          f"{code_cells} code cells parsed without execution")

    pairs = read_csv("data/manifests/pilot_series_manifest.csv", ["store_id", "product_id"])
    selected = {pair(row) for row in pairs}
    require(len(pairs) == len(selected) == 200, "Manifest is not 200 unique series")
    raw_columns = ["city_id", "store_id", "management_group_id", "first_category_id",
                   "second_category_id", "third_category_id", "product_id", "dt",
                   "sale_amount", "hours_sale", "stock_hour6_22_cnt", "hours_stock_status",
                   "discount", "holiday_flag", "activity_flag", "precpt",
                   "avg_temperature", "avg_humidity", "avg_wind_level"]
    pilot = read_csv("data/processed/pilot_200_series.csv", raw_columns +
                     ["day_number", "split", "pred_persistence", "pred_recent_avg_7"])
    indexed = {key(row): row for row in pilot}
    require(len(pilot) == len(indexed) == 18000, "Pilot row count or duplicate keys")
    require({pair(row) for row in pilot} == selected, "Pilot/manifest mismatch")
    expected_dates = {(date(2024, 3, 28) + timedelta(days=i)).isoformat() for i in range(90)}
    dates_by_series = defaultdict(set)
    for row in pilot:
        observed = date.fromisoformat(row["dt"])
        day = (observed - date(2024, 3, 28)).days + 1
        require(day == int(row["day_number"]), "Wrong day_number")
        split = "train" if day <= 60 else "validation" if day <= 75 else "test"
        require(row["split"] == split, "Wrong chronological split")
        require(all(row[column] != "" for column in raw_columns), "Empty source field")
        dates_by_series[pair(row)].add(row["dt"])
    require(all(dates == expected_dates for dates in dates_by_series.values()),
            "A pilot series lacks the exact 90-day calendar")
    counts = Counter(row["split"] for row in pilot)
    require(counts == {"train": 12000, "validation": 3000, "test": 3000}, "Split count mismatch")
    excluded = read_csv("data/manifests/excluded_series.csv", ["store_id", "product_id",
                        "row_count", "distinct_dates", "missing_dates", "unexpected_dates"])
    require(len(excluded) == 1 and pair(excluded[0]) == (420, 764), "Wrong excluded series")
    require(excluded[0]["row_count"] == excluded[0]["distinct_dates"] == "28",
            "Wrong inherited exclusion length")
    require(pair(excluded[0]) not in selected, "Excluded series appears in manifest")
    print(f"PASS: pilot schema, unique keys, exact manifest/calendar and splits {dict(counts)}")

    predictions = read_csv("results/baselines_DELTA/inherited/baseline_predictions.csv", ["model", "store_id",
                           "product_id", "dt", "day_number", "split", "sale_amount", "prediction"])
    models = {"persistence", "recent_avg_7"}
    predicted_keys = {(row["model"], *key(row), row["split"]) for row in predictions}
    expected_keys = {(model, *key(row), row["split"]) for model in models
                     for row in pilot if row["split"] in {"validation", "test"}}
    require(len(predictions) == len(predicted_keys) == 12000 and predicted_keys == expected_keys,
            "Prediction key coverage mismatch")
    for row in predictions:
        source = indexed[key(row)]
        require(row["day_number"] == source["day_number"] and row["split"] == source["split"],
                "Prediction metadata differs from pilot")
        require(float(row["sale_amount"]) == float(source["sale_amount"]), "Actual mismatch")
        require(math.isfinite(float(row["prediction"])), "Non-finite prediction")
    metrics = read_csv("results/baselines_DELTA/inherited/baseline_metrics.csv", ["model", "split", "n_observations",
                       "MAE", "RMSE", "bias"])
    require(len(metrics) == 4 and {(r["model"], r["split"]) for r in metrics} ==
            {(m, s) for m in models for s in ("validation", "test")}, "Metric key mismatch")
    require(all(r["n_observations"] == "3000" and
                all(math.isfinite(float(r[c])) for c in ("MAE", "RMSE", "bias"))
                for r in metrics), "Metric schema/value issue")
    print("PASS: inherited prediction/metric schemas, coverage and actuals (scores not recomputed)")

    historical = {"docs/handoff/README.original.md", "docs/handoff/README.utf8.md",
                  "archive/original_pilot/README.md"}
    checked_markdown = 0
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT).as_posix()
        if relative in historical or relative.startswith("docs/prompts/") or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        require("\x00" not in text, f"NUL in Markdown: {relative}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            local = unquote(target.split("#", 1)[0].strip("<>"))
            require((path.parent / local).exists(), f"Broken path in {relative}: {local}")
        checked_markdown += 1
    ignored = ["data/raw/freshretail.csv", "data/freshretail.csv", "data/other.csv",
               "archive/original_pilot/data/freshretail.csv", ".env", ".env.local", "credentials.json",
               ".venv/lib/test.py", "__pycache__/test.pyc", "models/model.joblib", "runs/new.csv",
               "data/manifests/reproduction/pilot_series_manifest.csv",
               "data/processed/reproduction/pilot_200_series.csv",
               "data/processed/feature_bundles/new/features.csv",
               "results/baselines_DELTA/reproduction/baseline_metrics.csv",
               "results/linear_regression_DEVGRU/new/predictions.csv", "results/models/tree.joblib"]
    retained = ([r["current_original_destination"] for r in manifest] +
                [r["working_destination"] for r in manifest] +
                [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("README.md")
                 if not any(part in {".git", ".venv", "venv", "env"}
                            for part in p.relative_to(ROOT).parts)])
    for path, should_ignore in [(p, True) for p in ignored] + [(p, False) for p in retained]:
        result = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT,
                                check=False)
        require(result.returncode in {0, 1}, "git check-ignore failed")
        require((result.returncode == 0) == should_ignore, f"Ignore rule mismatch: {path}")
    print(f"PASS: {checked_markdown} current Markdown files/paths and Git ignore/retention rules")
    print("SETUP CHECKS PASSED. No raw pipeline, notebook cells, features, fitting, or scoring executed.")


if __name__ == "__main__":
    main()
