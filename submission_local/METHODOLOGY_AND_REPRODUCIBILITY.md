# Methodology and Reproducibility

## Scientific contract

The target is normalized recorded `sale_amount`, represented as `actual`, keyed by `(store_id, product_id, dt)`. The approved question compares recent-sales forecasting with and without past stockout history. `sales_only` has the nine approved sales/calendar predictors; `stockout_aware` adds the five approved historical stockout predictors. Target-day stockout status is retrospective metadata only.

The protocol uses 14 days of past-only history, target eligibility beginning on day 15, development population 200 series, and chronological days 1–60 train, 61–75 validation, 76–90 test. Preprocessing is training-only, tuning is validation-only, MAE is primary, RMSE and signed bias are secondary, and no clipping is recorded. Conditions must share keys, actuals, and splits.

## Evidence provenance

The trusted development manifest SHA-256 is `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`. The development bundle itself is not present in this isolated worktree, so its contents were not opened or verified here. The R3 comparison manifest records development-only purpose, validation scoring, no retraining, and no test scoring.

The R3 package's `PACKAGE_SHA256SUMS` corresponds to committed Git blob bytes. Several text/CSV files in the current checkout have different raw hashes because of checkout line endings/encoding and assume-unchanged state; their textual records were not rewritten. This is an evidence-handling limitation, not a reason to overwrite originals.

## Commands actually run

```text
python scripts/verify_setup.py
.venv/Scripts/python.exe -m unittest tests.test_devgru_linear_ridge tests.test_sas_v2 -v
.venv/Scripts/python.exe -m scripts.verify_delta_v2
.venv/Scripts/python.exe -m scripts.sas_final_preflight
git diff --check
```

Setup verification passed. Unit tests stopped at import because `numpy` is absent; DELTA verification stopped at import because `pandas` is absent; final preflight stopped at import because `yaml` is absent. No fitting, prediction generation, bundle reproduction, or scoring was performed.

## Reproduction limitations

The original DEVGRU prediction outputs and exact DELTA development bundle are absent from this execution copy. Therefore the Linear/Ridge fits and source-to-prediction provenance cannot be independently rerun here. No serialized DEVGRU or Random Forest model artifacts were found in this copy.
