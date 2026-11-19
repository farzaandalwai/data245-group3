# Shared handoff interfaces — frozen v1.0.0

Definition status: **frozen for implementation on 2026-11-18 at SAS's explicit instruction**. Canonical machine-readable rules are [configs/contract.yaml](../configs/contract.yaml), with byte hashes in [contract.lock.json](../configs/contract.lock.json). These files define the interface; they do not implement or verify a feature producer, model, or evaluator. DELTA, DEVGRU, and SAS can develop their components against this version without inventing separate schemas.

Source/local stockout semantics and eligible counts are verified in [contract_freeze.md](contract_freeze.md) and [contract_audit.json](contract_audit.json). Full raw-data reproduction and experiment-wide feature/model leakage validation remain pending. Definition freezing is not a claim of independent teammate approval or completed implementation.

## Fixed input and eligibility

Use `data/processed/pilot_200_series.csv` and the exact `data/manifests/pilot_series_manifest.csv`; their SHA-256 values are locked. Preserve all 200 series and the original chronological boundaries. Target actual is the exact recorded normalized `sale_amount`, not latent demand. Keys are integer `store_id`, integer `product_id`, and ISO `dt`.

For every required/optional window and model, use the same target keys: first require day number >=29 (28 prior consecutive source days), then require target-day `stock_hour6_22_cnt == 0`. Stockout status is 1 for out of stock; business hours are `[06:00,22:00)`, Python indices 6 through 21, with 22 excluded. Availability is retrospective eligibility metadata only. Preserve all prior source dates, including stockout days, in the history. Unexpected missing/invalid inputs fail acceptance; do not silently drop extra rows or impute.

Eligible rows are train 3,693, validation 1,698, test 1,747 (7,138 total), across all 113 pilot stores in each split. Two series have no eligible train targets, two no eligible validation targets, and one no eligible test target. Keep the original manifest; a per-series result with no targets is not evaluable, not zero error. Pooled models must retain evaluation keys with training-unseen categories using the encoding policy below.

## Exact primary predictors

Required window: 14 days. Ordered common predictors:

`store_id`, `product_id`, `weekday`, `sales_lag_1`, `sales_lag_7`, `sales_mean_14`, `sales_std_14`.

The stockout-aware condition adds, in this order:

`stockout_hours_lag_1`, `stockout_hours_mean_14`, `stockout_day_fraction_14`, `stockout_free_lag_1`.

Definitions are exact in the YAML: lags use t-1/t-7 within the series; rolling means/std use all dates t-14 through t-1, full window, population std (`ddof=0`). Stockout fraction is the number of affected historical dates divided by 14. Last-day availability is 1 iff t-1 has zero business-hour stockout count. Do not add a redundant affected-day count as another predictor; retain that count in provenance for strata. Weekday is target-date Monday=0 through Sunday=6 and categorical. The two IDs are categorical inputs known from the forecast key.

No other source column is allowlisted. In particular, exclude actual/target-day raw sales/stock fields, baseline forecast columns, split/day metadata, realized weather, promotion/discount/activity/holiday fields, and additional hierarchy fields. The source-context invariance check is not permission to add columns. Select the exact list for the condition; never use every column in the feature CSV. IDs occur once in the CSV header even though they serve as keys and categorical predictors.

The optional 7/28-day comparison is not required for the first implementation. If separately authorized, replace rolling suffix `_14` with `_7`/`_28`, use the corresponding full prior window, keep lags/IDs/weekday, and retain the same day-29/availability target keys. Build historical features on the full ordered source before applying the eligible-target mask. No target actual enters feature computation.

## DELTA feature-bundle files

Bundle root: `data/processed/feature_bundles/<bundle_id>/`. Use UTF-8 CSV with LF newlines, ISO dates, base-10 integer IDs, finite round-trip-precision numeric values, unique headers, and numeric store/product/date sort order. JSON stores metadata. Generated contents stay ignored; share verified small artifacts only by a reviewed exception, or provide accessible acquisition links with hashes/bytes.

Required files and exact column order are in `contract.yaml`:

- `manifest.json`: contract version/hash; bundle ID; producer code revision/date; source hashes; every file's SHA-256/bytes/rows; split/filter counts; definitions and producer checks. Validate against the lock before consumption.
- `targets.csv`: keys, split, actual, only the 7,138 eligible targets.
- `features_14.csv`: keys plus the allowlisted derived features for both conditions, with each ID column included once. Exactly the target keys; target values and eligibility columns are absent.
- `eligibility.csv`: all 18,000 source keys, split/day, history eligibility, retrospective target count/free flag, final eligibility, and sequential first-failure reason. Boolean fields are 0/1. Reasons are `insufficient_28_day_history`, `target_stockout`, or `eligible`.
- `feature_provenance_14.csv`: eligible keys, history start/end/max source dates, window length, affected-history-day count, and history stratum. Start is t-14, end/max source is t-1; stratum is `history_with_stockout` iff the count is positive, else `history_without_stockout`.

Targets/features/provenance have identical unique keys and deterministic order; consumers still join/validate by keys rather than assume positions. No real bundle exists yet. DELTA must independently test actual feature values, chronology, hashes, filtering, and common keys before marking the first bundle verified. Do not relabel the legacy reproduction script as this feature producer.

## Model and evaluator contract

One pooled estimator per model/condition/window. Fit one-hot vocabularies on eligible training rows only. IDs/weekday are categorical strings; unknown categories become all-zero indicators, never dropped targets. Linear/ridge drop the first category per field and standardize only numeric columns using training mean/population std (constant scale=1). Tree uses all one-hot categories and unscaled numeric values. No imputation and no parameter/preprocessor refitting on validation/test. Clip all model/baseline predictions to `max(raw,0)`.

Core linear regression: ordinary least squares with intercept, one candidate. Core tree: squared error, best splitter, seed 245, all features, min split 2; grid depths 3/5/8/unlimited crossed with minimum leaf sizes 5/20/50, 12 candidates per condition. Select by validation row-weighted MAE after clipping; exact ties prefer shallower depth (unlimited last), then larger leaf size. Each condition receives the same budget; its selected settings may differ. These are planned settings, not fitted results. Ridge and random forest are disabled until course fit and an explicit versioned amendment; neither blocks the core implementation.

Each model owner writes `predictions.csv` and `run_metadata.json` under the explicit `run_roots_by_model` path in the YAML: learned models use their existing owner/model directory; fixed baselines use `results/baselines_DELTA/<model>/<run_id>/`. Each run contains exactly one feature condition and one history window; run IDs separate conditions/windows. Column order: `store_id, product_id, dt, actual, prediction, model, feature_set, split, run_id`. Within a run, require uniqueness by key/model/feature-set/split; separate multiple runs by directory and run ID. Actuals/keys/splits must match the shared targets exactly, predictions must be finite/nonnegative, and missing/extra/duplicate keys fail. During development, produce validation handoffs; training diagnostics are separate, and new model test evaluation is blocked until validation settings and code/contract/bundle hashes are recorded as frozen in a pre-test record for both conditions. That record binds the contract/bundle hashes, model/conditions, selected parameters, validation candidate metrics, history-window length, code revision, timestamp and SAS integrator; run metadata cites its SHA-256 (null while still in validation development).

Run metadata includes contract/bundle hashes, code revision, owner/model/condition/window/run/date/environment, fitted preprocessing, tuning budget and selected settings, clipping policy, checks, and test-gate status. SAS's evaluator consumes these files, not model/notebook internals. Metrics, strata, aggregation, paired store bootstrap and tie rules are fixed in the canonical YAML. Existing baseline test exposure is disclosed; no new model test score has been calculated here. Original baseline files retain their inherited schema and remain unchanged; DELTA's future matched baseline outputs use this contract.

## Parallel work and changes

DELTA builds the real shared features/baselines, DEVGRU builds linear adapters, and SAS builds tree/evaluator adapters. All can code and push independently now. Clearly labeled deterministic schema fixtures can be used for development; fixture outputs must never be research findings. This task did not generate a fixture or feature table. Real paired runs wait for the verified DELTA bundle; final comparisons wait for accepted predictions and the test gate.

Changing predictor definitions/order, target eligibility, serialization, preprocessing/tuning/evaluation rules, or required schema requires a versioned contract amendment and corresponding lock update, with affected owners coordinating before dependent runs. Freeze a new contract/bundle identity, never silently mutate a consumed bundle. Repository/package setup is still subject to course/runtime verification; no trained-model environment is claimed reproducible by these interface checks.
