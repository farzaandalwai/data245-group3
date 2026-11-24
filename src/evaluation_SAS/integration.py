"""Read-only original-artifact acceptance and separate DEVELOPMENT comparisons.

No fitted model is loaded, rewritten, trained or tuned here. Source prediction
bytes are immutable; only in-memory run labels are normalized for the evaluator.
"""
from pathlib import Path
import platform
import re

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.bootstrap import BOOTSTRAP_SPEC
from src.evaluation_SAS.runs import (
    ROOT, _inventory, load_prediction_run, new_run, pinned_bundle, read_json, source_snapshot,
)
from src.evaluation_SAS.v2 import CONDITIONS, evaluate_predictions, regression_metrics, validate_predictions
from src.features_DELTA.bundle import sha256, write_csv, write_json
from src.features_DELTA.v2 import COMMON, EXTRA

DEVGRU_MODELS = ("linear_regression", "ridge_regression")
LEARNED = [*DEVGRU_MODELS, "decision_tree", "random_forest"]
ALL_MODELS = [*LEARNED, "persistence", "recent_avg_7"]
# Recorded in docs/SAS_RANDOM_FOREST.md when run sas-forest-dev-200-r1 was made.
FOREST_RUN_MANIFEST_SHA256 = "ba8696f1cc7e780dfee1141be0f4a3e58df547fab98c7e522469e78c92e45bc9"


def verify_files(directory, records):
    """Verify a trusted inventory, never accept traversal or an input symlink."""
    directory = Path(directory)
    for name, record in records.items():
        path = directory / name
        if (Path(name).is_absolute() or ".." in Path(name).parts or "\\" in name
                or path.is_symlink() or not path.resolve().is_relative_to(directory.resolve())):
            raise ValueError(f"Unsafe artifact path: {name}")
        if (not path.is_file() or sha256(path) != record["sha256"]
                or ("bytes" in record and path.stat().st_size != record["bytes"])):
            raise ValueError(f"Artifact hash/size mismatch: {name}")


def sas_originals(directory, identity, observations, evidence):
    directory = Path(directory)
    expected = {}
    for label, subdir in (("real_tree", "decision_tree"), ("real_validation", "comparison")):
        item = evidence["runs"][label]
        expected[f"{subdir}/{Path(item['path']).name}"] = {"sha256": item["sha256"]}
        expected.update({f"{subdir}/{name}": record for name, record in item["artifact_hashes"].items()})
    verify_files(directory, expected)
    declared = read_json(directory / "ORIGINALS_MANIFEST.json")["files"]
    if set(declared) != set(expected) or any(declared[n]["sha256"] != r["sha256"] for n, r in expected.items()):
        raise ValueError("Original SAS inventory differs from prior committed evidence")
    predicted, manifest = load_prediction_run(directory / "decision_tree", identity, observations)
    return predicted, {"files": expected, "run_manifest_sha256": sha256(directory / "decision_tree/run_manifest.json"),
                       "policy": manifest["policy"], "source": manifest["source"],
                       "missing": ["Per-replicate bootstrap draw arrays were not saved",
                                   "No pickle/joblib; numeric selected tree JSON exports are provided"]}


def sas_forest(directory, identity, observations, expected_manifest_sha256=FOREST_RUN_MANIFEST_SHA256):
    """Accept the shared Random Forest run only at its recorded manifest identity."""
    directory = Path(directory)
    manifest_path = directory / "run_manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file() or sha256(manifest_path) != expected_manifest_sha256:
        raise ValueError("Random Forest run manifest differs from the recorded run")
    predicted, manifest = load_prediction_run(directory, identity, observations)
    if manifest["models"] != ["random_forest"]:
        raise ValueError("Forest run must contain only random_forest predictions")
    return predicted, {"run_id": manifest["run_id"], "run_manifest_sha256": expected_manifest_sha256,
                       "policy": manifest["policy"], "selected_parameters": manifest["selected_parameters"],
                       "source": manifest["source"],
                       "limitations": ["Development-only proposal; settings are not team-frozen",
                                       "No fitted forest file saved; the seeded run is reproducible from code/policy",
                                       "Run manifest records an uncommitted working tree with per-file source hashes"]}


def relative_mae_improvement(summary):
    """Protocol's 100*(MAE_sales - MAE_aware)/MAE_sales per learned model; undefined at zero."""
    pivot = summary.loc[summary.feature_set.isin(["sales_only", "stockout_aware"])].pivot(
        index="model", columns="feature_set", values="MAE")
    sales, aware = pivot["sales_only"], pivot["stockout_aware"]
    value = (100 * (sales - aware) / sales).where(sales != 0)
    return value.rename("relative_MAE_improvement_pct")


def _inventory_findings(directory, pin):
    text = (directory / "INVENTORY.md").read_text(encoding="utf-8")
    findings = []
    for name, record in pin["files"].items():
        lines = [line for line in text.splitlines() if "|" in line and f"`{name}`" in line]
        if not lines:
            # Prediction inventory includes the original runs/... prefix.
            lines = [line for line in text.splitlines() if "|" in line and name in line]
        # Also report malformed digest lengths rather than treating them as absent.
        matches = re.findall(r"`([0-9a-f]{50,80})`", "\n".join(lines))
        if matches and record["sha256"] not in matches:
            findings.append({"file": name, "status": "original_inventory_checksum_mismatch",
                             "declared_sha256": matches, "published_git_blob_sha256": record["sha256"]})
    return findings


def _audit_metrics_and_selection(directory, frames, metadata):
    metrics = pd.read_csv(directory / "validation_metrics.csv")
    required = {"model", "feature_set", "split", "MAE", "RMSE", "signed_bias", "rows"}
    if not required <= set(metrics) or len(metrics) != 8 or metrics.duplicated(["model", "feature_set", "split"]).any():
        raise ValueError("Invalid DEVGRU metric coverage")
    for frame in frames:
        model, condition = frame.model.iloc[0], frame.feature_set.iloc[0]
        for split in ("train", "validation"):
            part = frame.loc[frame.split.eq(split)]
            row = metrics.loc[metrics.model.eq(model) & metrics.feature_set.eq(condition) & metrics.split.eq(split)]
            if len(row) != 1 or int(row.iloc[0]["rows"]) != len(part):
                raise ValueError("DEVGRU metric population mismatch")
            measured = regression_metrics(part.actual, part.prediction)
            if not all(np.isclose(measured[k], row.iloc[0][k], rtol=1e-12, atol=1e-12)
                       for k in ("MAE", "RMSE", "signed_bias")):
                raise ValueError("DEVGRU stored metrics differ from original predictions")
    tuning = pd.read_csv(directory / "ridge_alpha_selection.csv")
    candidates = metadata["ridge_alpha_candidates"]
    if list(tuning) != ["feature_set", "alpha", "validation_mae"] or len(tuning) != 2 * len(candidates):
        raise ValueError("DEVGRU alpha evidence schema/budget mismatch")
    if not np.isfinite(tuning[["alpha", "validation_mae"]]).all().all() or tuning.validation_mae.lt(0).any():
        raise ValueError("Invalid DEVGRU alpha evidence")
    for condition in CONDITIONS:
        rows = tuning.loc[tuning.feature_set.eq(condition)]
        if len(rows) != len(candidates) or sorted(rows.alpha) != sorted(candidates):
            raise ValueError("Unequal/incorrect DEVGRU candidate grid")
        chosen = rows.sort_values(["validation_mae", "alpha"]).iloc[0]
        if chosen.alpha != metadata["selected_ridge_alphas"][condition]:
            raise ValueError("Selected Ridge alpha differs from recorded validation-MAE rule")
        score = metrics.loc[metrics.model.eq("ridge_regression") & metrics.feature_set.eq(condition)
                            & metrics.split.eq("validation"), "MAE"].iloc[0]
        if not np.isclose(chosen.validation_mae, score, rtol=1e-12, atol=1e-12):
            raise ValueError("Selected Ridge score differs from prediction score")


def _audit_original_series_bootstrap(directory, frames, metadata):
    stored = pd.read_csv(directory / "paired_validation_comparison.csv")
    if len(stored) != 2 or set(stored.model) != set(DEVGRU_MODELS):
        raise ValueError("Incorrect original DEVGRU bootstrap model coverage")
    results = []
    for model in DEVGRU_MODELS:
        parts = {f.feature_set.iloc[0]: f.loc[f.split.eq("validation")] for f in frames if f.model.iloc[0] == model}
        paired = parts["sales_only"].merge(parts["stockout_aware"], on=KEY, validate="one_to_one", suffixes=("_sales", "_aware"))
        paired["loss_difference"] = ((paired.prediction_aware - paired.actual_aware).abs()
                                     - (paired.prediction_sales - paired.actual_sales).abs())
        series = paired.groupby(SERIES, sort=True).loss_difference.mean().to_numpy()
        seed = metadata["bootstrap"]["seed_by_model"][model]
        count = metadata["bootstrap"]["repetitions"]
        if count != 2000 or seed != (245 if model == "linear_regression" else 246):
            raise ValueError("Unexpected original DEVGRU bootstrap settings; review before adaptation")
        rng = np.random.default_rng(seed)
        samples = rng.integers(0, len(series), size=(count, len(series)))
        low, high = np.percentile(series[samples].mean(axis=1), [2.5, 97.5])
        row = stored.loc[stored.model.eq(model)].iloc[0]
        for name, actual in [("MAE_difference_stockout_aware_minus_sales_only", paired.loss_difference.mean()),
                             ("bootstrap_ci_lower", low), ("bootstrap_ci_upper", high)]:
            if not np.isclose(row[name], actual, rtol=1e-12, atol=1e-12):
                raise ValueError(f"Original series-bootstrap reproduction mismatch: {model}/{name}")
        if (row.bootstrap_seed != seed or row.bootstrap_repetitions != count
                or row.resampled_series != len(series) or row.bootstrap_unit != "store-product series"):
            raise ValueError("Original bootstrap record settings disagree with metadata")
        results.append({"model": model, "original_unit": "store-product series", "original_seed": int(seed),
                        "original_replicates": int(count), "original_ci_lower": float(low),
                        "original_ci_upper": float(high), "reproduced_from_original_predictions": True,
                        "series_have_equal_validation_rows": paired.groupby(SERIES).size().nunique() == 1})
    return results


def devgru_originals(directory, pin, identity, observations):
    """Accept the published Git package, reporting inaccurate original inventory entries."""
    directory = Path(directory)
    verify_files(directory, pin["files"])
    metadata = read_json(directory / "run_metadata.json")
    for name in ("purpose", "protocol_version", "bundle_manifest_sha256"):
        if metadata.get(name) != identity[name]:
            raise ValueError(f"DEVGRU incompatible {name}")
    if (metadata.get("preprocessing_policy") != "standardize"
            or metadata.get("prediction_postprocessing") != "none"
            or metadata.get("feature_sets") != {"sales_only": COMMON, "stockout_aware": COMMON + EXTRA}
            or metadata.get("models") != list(DEVGRU_MODELS)):
        raise ValueError("DEVGRU declarations contradict the shared input/prediction requirements")
    records = metadata.get("experiments", [])
    combos = {(r["model_name"], r["feature_set"]) for r in records}
    if len(records) != 4 or combos != {(m, c) for m in DEVGRU_MODELS for c in CONDITIONS}:
        raise ValueError("DEVGRU experiment metadata coverage mismatch")
    frames, original_frames, mappings = [], [], []
    for record in records:
        model, condition = record["model_name"], record["feature_set"]
        if record.get("bundle_manifest_sha256") != identity["bundle_manifest_sha256"]:
            raise ValueError("DEVGRU per-experiment bundle mismatch")
        path = directory / model / f"{condition}.predictions.csv"
        frame = pd.read_csv(path, converters={"actual": float, "prediction": float})
        if (set(frame.model) != {model} or set(frame.feature_set) != {condition}
                or set(frame.run_id) != {record["run_id"]} or len(frame) != record["prediction_rows"]
                or set(record["split_coverage"]) != {"train", "validation"}):
            raise ValueError("DEVGRU per-file model/condition/run/row metadata mismatch")
        original_frames.append(frame.copy())
        normalized_id = f"SAS-adapted-{metadata['run_id']}-{model}"
        mappings.append({"model": model, "feature_set": condition, "original_run_id": record["run_id"],
                         "evaluation_run_id": normalized_id, "changed_fields": ["run_id"],
                         "file": f"{model}/{condition}.predictions.csv",
                         "negative_predictions": int(frame.prediction.lt(0).sum())})
        frame["run_id"] = normalized_id
        frames.append(frame)
    predicted = pd.concat(frames, ignore_index=True)
    coverage = validate_predictions(predicted, observations, list(DEVGRU_MODELS), ["train", "validation"])
    _audit_metrics_and_selection(directory, original_frames, metadata)
    old_intervals = _audit_original_series_bootstrap(directory, original_frames, metadata)
    findings = _inventory_findings(directory, pin)
    return predicted, {
        "source_commit": pin["commit"], "source_pr": pin["pr_url"], "files": pin["files"],
        "pin_supersedes": pin.get("supersedes"),
        "original_inventory_discrepancies": findings,
        "run_id_mapping": mappings, "coverage": coverage, "original_bootstrap_audit": old_intervals,
        "declarations": {k: metadata[k] for k in ("preprocessing_policy", "prediction_postprocessing", "selected_ridge_alphas", "source_git_revision")},
        "limitations": ["Original DEVGRU fitted model files were never saved",
                        ("Metadata was enriched for handoff; supporting inventory entries still differ from published bytes: "
                         + ", ".join(sorted(f["file"] for f in findings))) if findings
                        else "Metadata was enriched for handoff; inventory entries match published bytes",
                        "Source revision records base d2a323e, without original dirty-source hashes",
                        "Code inspection/synthetic behavioral checks support policy; declarations alone do not prove original execution"],
    }


def validation_baselines(tables, run_id):
    """Apply DELTA formulas to validation inputs only; no test forecasts materialized."""
    from src.models.baselines_DELTA.v2 import predictions
    keys = tables["observations"].loc[tables["observations"].split.eq("validation"), KEY]
    sliced = {"observations": tables["observations"].merge(keys, on=KEY, validate="one_to_one"),
              "features_sales_only": tables["features_sales_only"].merge(keys, on=KEY, validate="one_to_one")}
    return predictions(sliced, run_id)


def verify_sas_tree_exports(directory, tables, predictions):
    """Reconstruct existing train/validation predictions from saved numeric trees, without fitting."""
    for condition in CONDITIONS:
        tree = read_json(Path(directory) / "decision_tree" / f"{condition}_tree.json")
        expected_names = COMMON if condition == "sales_only" else COMMON + EXTRA
        if tree["feature_names"] != expected_names:
            raise ValueError("Saved SAS tree feature order differs from approved allowlist")
        frame = predictions.loc[predictions.feature_set.eq(condition)]
        joined = frame.merge(tables[f"features_{condition}"], on=KEY, validate="one_to_one")
        reconstructed = []
        for row in joined[expected_names].to_numpy(dtype=np.float32):
            node = 0
            for _ in range(len(tree["feature"]) + 1):
                if tree["children_left"][node] == -1:
                    reconstructed.append(tree["value"][node])
                    break
                go_left = float(row[tree["feature"][node]]) <= tree["threshold"][node]
                node = tree["children_left"][node] if go_left else tree["children_right"][node]
            else:
                raise ValueError("Saved SAS tree contains a cycle")
        if not np.array_equal(np.asarray(reconstructed), joined.prediction.to_numpy()):
            raise ValueError("Original SAS predictions do not match saved tree exports")


def compare_development(bundle, bundle_hash, sas_directory, devgru_directory, pin, destination,
                        forest_directory=None):
    destination = Path(destination)
    sources = [sas_directory, devgru_directory, bundle] + ([forest_directory] if forest_directory else [])
    for original in sources:
        if destination.resolve().is_relative_to(Path(original).resolve()):
            raise ValueError("Comparison destination must be separate from source artifacts")
    if destination.exists():
        raise FileExistsError(destination)
    tables, _, identity = pinned_bundle(bundle, bundle_hash)
    evidence = read_json(ROOT / "docs/SAS_INTEGRATION_EVIDENCE.json")
    sas, sas_audit = sas_originals(sas_directory, identity, tables["observations"], evidence)
    verify_sas_tree_exports(sas_directory, tables, sas)
    sas_audit["saved_tree_predictions_reconstructed_without_refitting"] = True
    devgru, devgru_audit = devgru_originals(devgru_directory, pin, identity, tables["observations"])
    frames = [sas.loc[sas.split.eq("validation")], devgru.loc[devgru.split.eq("validation")]]
    models = [m for m in ALL_MODELS if m != "random_forest"]
    forest_audit = None
    if forest_directory:
        forest, forest_audit = sas_forest(forest_directory, identity, tables["observations"])
        frames.append(forest.loc[forest.split.eq("validation")])
        models = list(ALL_MODELS)
    baseline = validation_baselines(tables, "SAS-validation-reference-formulas-20261120")
    predictions = pd.concat([*frames, baseline], ignore_index=True)
    report = evaluate_predictions(predictions, tables["observations"], tables["evaluation_metadata"],
                                  purpose=identity["purpose"], models=models)
    summary = report["overall"].copy()
    summary = summary.merge(relative_mae_improvement(summary), left_on="model", right_index=True, how="left")
    summary["n_stores"] = tables["observations"].loc[tables["observations"].split.eq("validation"), "store_id"].nunique()
    summary["evidence_status"] = "DEVELOPMENT_VALIDATION_NOT_FINAL"
    summary = summary.merge(report["mae_difference_intervals"][["model", "split", "MAE_difference", "ci_lower", "ci_upper"]],
                            on=["model", "split"], how="left", validate="many_to_one")
    subgroup_counts = (tables["observations"].query('split == "validation"').merge(
        tables["evaluation_metadata"], on=KEY, validate="one_to_one").groupby("target_stockout_group").store_id.nunique())
    report["subgroups"]["n_stores"] = report["subgroups"].target_stockout_group.map(subgroup_counts).fillna(0).astype(int)
    with new_run(destination) as temporary:
        write_csv(temporary / "development_comparison.csv", summary)
        for name in ("overall", "subgroups", "per_series", "per_store", "paired_comparisons", "mae_difference_intervals"):
            write_csv(temporary / f"{name}.csv", report[name])
        write_csv(temporary / "validation_baseline_predictions.csv", baseline)
        write_json(temporary / "input_acceptance.json", {"SAS": sas_audit, "SAS_random_forest": forest_audit,
                   "DEVGRU": devgru_audit,
                   "baselines": "New validation-only materialization of DELTA lag-1/mean-7 formulas from exact bundle; not original DELTA output files"})
        write_json(temporary / "coverage_audit.json", report["coverage_audit"])
        from src.evaluation_SAS.figures import development_figures
        development_figures(summary, report["mae_difference_intervals"], temporary)
        source = source_snapshot()
        for name in ("scripts/sas_development_comparison.py", "docs/SAS_DEVGRU_PR6_PIN.json",
                     "src/models/random_forest_SAS/v2.py"):
            source["files_sha256"][name] = sha256(ROOT / name)
        manifest = {**identity, "comparison_version": "SAS-harmonized-development-1", "owner": "SAS",
                    "status": "DEVELOPMENT_VALIDATION_NOT_FINAL", "source": source,
                    "models": models, "scored_splits": ["validation"], "test_scored": False,
                    "relative_MAE_improvement": "100*(MAE_sales_only-MAE_stockout_aware)/MAE_sales_only; point estimate only, no interval",
                    "uncertainty": BOOTSTRAP_SPEC, "DEVGRU_source_commit": pin["commit"],
                    "originals_modified": False, "model_retraining": False,
                    "environment": {"python": platform.python_version(), "numpy": np.__version__,
                                    "pandas": pd.__version__, "matplotlib": __import__("matplotlib").__version__},
                    "artifacts": _inventory(temporary)}
        write_json(temporary / "comparison_manifest.json", manifest)
    return manifest
