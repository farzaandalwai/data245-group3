"""Read-only pilot stockout/index/eligibility audit; no features, fitting or scoring."""

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_COLUMNS = ["city_id", "management_group_id", "first_category_id",
                    "second_category_id", "third_category_id"]


def parse_stock_status(text):
    """Parse the exported NumPy-like binary vector without eval or code execution."""
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        raise ValueError("Stock-status vector must be bracketed")
    tokens = re.split(r"[\s,]+", text[1:-1].strip())
    if len(tokens) != 24 or any(token not in {"0", "1"} for token in tokens):
        raise ValueError("Stock-status vector must have 24 binary hour entries")
    return [int(token) for token in tokens]


def eligibility_reason(day_number, stockout_hours):
    """Sequential filter reason; retrospective target availability is not a feature."""
    if day_number < 29:
        return "insufficient_28_day_history"
    if stockout_hours != 0:
        return "target_stockout"
    return "eligible"


def business_stockout_hours(status):
    """Business interval is 06:00 inclusive to 22:00 exclusive (16 entries)."""
    return sum(status[6:22])


def audit(root=ROOT):
    path = root / "data/processed/pilot_200_series.csv"
    expected = next(record for record in json.loads(
        (root / "docs/handoff/import_manifest.json").read_text())
                    if record["dest"] == "data/processed/pilot_200_series.csv")
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()
    if checksum != expected["sha256"]:
        raise ValueError("Pilot differs from the fixed imported source")
    counts = {name: Counter() for name in ("train", "validation", "test")}
    category_map = {}
    series_dates = defaultdict(set)
    eligible_stores = defaultdict(set)
    eligible_series = defaultdict(Counter)
    source_mask_values = set()
    mismatches = alternative_mismatches = 0
    seen_keys = set()
    row_count = 0
    min_count, max_count = 16, 0
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            row_count += 1
            pair = (int(row["store_id"]), int(row["product_id"]))
            key = (*pair, row["dt"])
            if key in seen_keys:
                raise ValueError("Duplicate source key")
            seen_keys.add(key)
            series_dates[pair].add(row["dt"])
            status = parse_stock_status(row["hours_stock_status"])
            source_mask_values.update(status)
            hours = int(row["stock_hour6_22_cnt"])
            if not 0 <= hours <= 16:
                raise ValueError("Daily out-of-stock-hour count outside [0,16]")
            min_count, max_count = min(min_count, hours), max(max_count, hours)
            mismatches += business_stockout_hours(status) != hours
            alternative_mismatches += sum(status[6:23]) != hours
            actual = float(row["sale_amount"])
            if not math.isfinite(actual) or actual < 0:
                raise ValueError("Target must be finite and nonnegative")
            categories = tuple(row[name] for name in CATEGORY_COLUMNS)
            if pair in category_map and categories != category_map[pair]:
                raise ValueError("Proposed static context changes within a source series")
            category_map[pair] = categories
            split = row["split"]
            counts[split]["original"] += 1
            reason = eligibility_reason(int(row["day_number"]), hours)
            counts[split][reason] += 1
            if reason == "eligible":
                eligible_stores[split].add(pair[0])
                eligible_series[split][pair] += 1
    if row_count != 18000 or len(series_dates) != 200 or mismatches:
        raise ValueError("Pilot size/series or stockout-hour/index consistency failed")
    report = {
        "audit_scope": "fixed local 18000-row pilot only; read-only field/eligibility audit",
        "contract_freeze_date_local": "2026-11-18 America/Los_Angeles",
        "source_evidence": {
            "dataset_card": "https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md",
            "publisher_commit": "8af694a09a5a427d1d50648d348c022565a781f2",
            "publisher_source_blob": "fc56086de90fb075913e8d053b8e0a438dd1d030",
            "publisher_source": "https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/exp/data/generate_data.py#L61-L63",
        },
        "pilot_sha256": checksum,
        "rows_checked": row_count,
        "series_checked": len(series_dates),
        "stores_in_pilot": len({pair[0] for pair in series_dates}),
        "stock_status_vector_length": 24,
        "stock_status_values_observed": sorted(source_mask_values),
        "stockout_value": 1,
        "hour_interval": "[06:00,22:00), source array indices 6 through 21",
        "slice_start_inclusive": 6,
        "slice_stop_exclusive": 22,
        "daily_count_min": min_count,
        "daily_count_max": max_count,
        "slice_6_22_count_mismatches": mismatches,
        "slice_6_23_count_mismatches": alternative_mismatches,
        "static_context_columns_checked": CATEGORY_COLUMNS,
        "series_with_context_drift": 0,
        "filter_order": ["day_number >= 29", "target stock_hour6_22_cnt == 0"],
        "splits": {},
        "no_feature_table_model_predictions_or_scores_produced": True,
    }
    for split, values in counts.items():
        original = values["original"]
        removed_history = values["insufficient_28_day_history"]
        report["splits"][split] = {
            "original": original,
            "removed_history": removed_history,
            "after_history": original - removed_history,
            "removed_target_stockout_after_history": values["target_stockout"],
            "eligible": values["eligible"],
            "eligible_stores": len(eligible_stores[split]),
            "eligible_series": len(eligible_series[split]),
            "series_with_no_eligible_targets": len(series_dates) - len(eligible_series[split]),
        }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional explicit JSON audit evidence path")
    args = parser.parse_args()
    payload = json.dumps(audit(), indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
