"""Path-adapted copy of Timothy Tran's inherited preparation/baseline script.

This legacy reproduction entry point has not been rerun during migration.
It writes separate reproduction outputs, never the fixed shared pilot/manifest
or inherited baseline evidence. The original bytes are in archive/original_pilot.
"""

from pathlib import Path

import pandas as pd


RANDOM_SEED = 245
EXPECTED_DAYS = 90
SERIES = ["store_id", "product_id"]
KEY = [*SERIES, "dt"]
ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "raw" / "freshretail.csv"
PROCESSED = ROOT / "data" / "processed" / "reproduction"
MANIFESTS = ROOT / "data" / "manifests" / "reproduction"
RESULTS = ROOT / "results" / "baselines_DELTA" / "reproduction"


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT, parse_dates=["dt"])
    required = {"store_id", "product_id", "dt", "sale_amount", "stock_hour6_22_cnt"}
    missing = required.difference(df.columns)
    assert not missing, f"Missing required columns: {sorted(missing)}"
    assert df["dt"].notna().all(), "dt contains missing or unparseable values"

    df = df.sort_values(KEY, kind="mergesort").reset_index(drop=True)
    series_group = df.groupby(SERIES, sort=False, observed=True)
    increasing = series_group["dt"].apply(lambda dates: dates.is_monotonic_increasing)
    assert increasing.all(), "Dates are not increasing within every series"

    expected_dates = pd.date_range(df["dt"].min(), df["dt"].max(), freq="D")
    n_dates = df["dt"].nunique()
    assert len(expected_dates) == EXPECTED_DAYS and n_dates == EXPECTED_DAYS, (
        f"Expected {EXPECTED_DAYS} consecutive dates; observed {n_dates} distinct "
        f"dates from {df['dt'].min().date()} through {df['dt'].max().date()}"
    )

    lengths = series_group.size().rename("row_count")
    dates_by_series = series_group["dt"].agg(lambda s: frozenset(s))
    full_set = frozenset(expected_dates)
    complete_index = dates_by_series.index[dates_by_series.eq(full_set)]
    incomplete_index = dates_by_series.index[~dates_by_series.eq(full_set)]
    complete_count = len(complete_index)

    incomplete_rows = []
    for store_id, product_id in incomplete_index:
        actual = dates_by_series.loc[(store_id, product_id)]
        incomplete_rows.append(
            {
                "store_id": store_id,
                "product_id": product_id,
                "row_count": int(lengths.loc[(store_id, product_id)]),
                "distinct_dates": len(actual),
                "missing_dates": ";".join(
                    d.strftime("%Y-%m-%d") for d in expected_dates if d not in actual
                ),
                "unexpected_dates": ";".join(
                    sorted(d.strftime("%Y-%m-%d") for d in actual - full_set)
                ),
            }
        )
    excluded = pd.DataFrame(
        incomplete_rows,
        columns=["store_id", "product_id", "row_count", "distinct_dates", "missing_dates", "unexpected_dates"],
    )
    excluded.to_csv(MANIFESTS / "excluded_series.csv", index=False)

    duplicate_count = int(df.duplicated(KEY).sum())
    assert duplicate_count == 0, f"Found {duplicate_count} duplicate series-date rows"
    null_counts = df.isna().sum()
    length_distribution = lengths.value_counts().sort_index()
    audit_lines = [
        "FreshRetail data audit",
        f"Rows: {len(df):,}",
        f"Columns: {len(df.columns)}",
        f"Date range: {df['dt'].min().date()} through {df['dt'].max().date()}",
        f"Distinct dates: {n_dates}",
        f"Unique store-product series: {len(lengths):,}",
        f"Duplicate (store_id, product_id, dt) rows: {duplicate_count}",
        f"Complete {EXPECTED_DAYS}-date series: {complete_count:,}",
        f"Incomplete series: {len(incomplete_index):,}",
        "Series-length distribution (rows per series: series count):",
        *(f"  {int(k)}: {int(v):,}" for k, v in length_distribution.items()),
        "Null count by column:",
        *(f"  {col}: {int(count):,}" for col, count in null_counts.items()),
        "Incomplete series details (also saved to data/manifests/reproduction/excluded_series.csv):",
    ]
    if excluded.empty:
        audit_lines.append("  None")
    else:
        audit_lines.extend(
            f"  store={r.store_id}, product={r.product_id}, rows={r.row_count}, "
            f"distinct_dates={r.distinct_dates}, missing={r.missing_dates or 'none'}"
            for r in excluded.itertuples(index=False)
        )
    audit_text = "\n".join(audit_lines) + "\n"
    (RESULTS / "data_audit.txt").write_text(audit_text, encoding="utf-8")
    print(audit_text, end="")

    complete_pairs = pd.DataFrame(complete_index.tolist(), columns=SERIES)
    assert len(complete_pairs) >= 200, "Fewer than 200 complete series are available"
    pilot_pairs = complete_pairs.sample(n=200, random_state=RANDOM_SEED).sort_values(SERIES)
    pilot_pairs.to_csv(MANIFESTS / "pilot_series_manifest.csv", index=False)
    pilot = df.merge(pilot_pairs, on=SERIES, how="inner", validate="many_to_one")
    pilot = pilot.sort_values(KEY, kind="mergesort").reset_index(drop=True)
    assert len(pilot) == 200 * EXPECTED_DAYS, f"Unexpected pilot size: {len(pilot)}"

    date_to_day = {date: day for day, date in enumerate(expected_dates, start=1)}
    pilot["day_number"] = pilot["dt"].map(date_to_day).astype("int8")
    assert pilot.groupby("dt")["day_number"].nunique().eq(1).all()
    pilot["split"] = pd.cut(
        pilot["day_number"],
        bins=[0, 60, 75, 90],
        labels=["train", "validation", "test"],
    ).astype("string")

    grouped_sales = pilot.groupby(SERIES, sort=False, observed=True)["sale_amount"]
    pilot["pred_persistence"] = grouped_sales.shift(1)
    pilot["pred_recent_avg_7"] = grouped_sales.transform(
        lambda sales: sales.shift(1).rolling(window=7, min_periods=7).mean()
    )
    pilot.to_csv(PROCESSED / "pilot_200_series.csv", index=False)

    split_summary = []
    for split in ("train", "validation", "test"):
        part = pilot.loc[pilot["split"].eq(split)]
        split_summary.append(
            f"{split}: {part['dt'].min().date()} through {part['dt'].max().date()}, "
            f"{len(part):,} rows"
        )

    metric_rows = []
    prediction_rows = []
    for model, prediction in (
        ("persistence", "pred_persistence"),
        ("recent_avg_7", "pred_recent_avg_7"),
    ):
        for split in ("validation", "test"):
            evaluated = pilot.loc[
                pilot["split"].eq(split) & pilot[prediction].notna(),
                [*SERIES, "dt", "day_number", "split", "sale_amount", prediction],
            ].copy()
            actual = evaluated["sale_amount"]
            predicted = evaluated[prediction]
            metric_rows.append(
                {
                    "model": model,
                    "split": split,
                    "n_observations": len(evaluated),
                    "MAE": (predicted - actual).abs().mean(),
                    "RMSE": ((predicted - actual).pow(2).mean()) ** 0.5,
                    "bias": (predicted - actual).mean(),
                }
            )
            evaluated = evaluated.rename(columns={prediction: "prediction"})
            evaluated.insert(0, "model", model)
            prediction_rows.append(evaluated)

    metrics = pd.DataFrame(metric_rows)
    predictions = pd.concat(prediction_rows, ignore_index=True)
    predictions.to_csv(RESULTS / "baseline_predictions.csv", index=False)
    metrics.to_csv(RESULTS / "baseline_metrics.csv", index=False, float_format="%.6f")

    print("\nPilot summary")
    print(f"Rows loaded: {len(df):,}")
    print(f"Complete series available: {complete_count:,}")
    print(f"Excluded series: {len(incomplete_index):,}")
    print(f"Pilot series: {len(pilot_pairs)}")
    print(f"Pilot rows: {len(pilot):,}")
    print("Split boundaries:")
    print("\n".join(f"  {line}" for line in split_summary))
    print("Baseline metrics (MAE, RMSE, bias):")
    for row in metrics.itertuples(index=False):
        print(
            f"  {row.model} {row.split}: MAE={row.MAE:.6f}, "
            f"RMSE={row.RMSE:.6f}, bias={row.bias:.6f} (n={row.n_observations:,})"
        )


if __name__ == "__main__":
    main()
