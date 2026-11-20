# DEVGRU cross-team compatibility audit

Audit date: 2026-11-20
Status: **PASS WITH LIMITATIONS**
Scope: DEVGRU prediction outputs versus the shared interface and locally available SAS evaluator

## Canonical exchange schema

The actual shared evaluator and DEVGRU validator use the same ordered columns:

`store_id,product_id,dt,actual,prediction,model,feature_set,split,run_id`

Required labels are `sales_only` and `stockout_aware`; learned-model labels are `linear_regression`, `ridge_regression`, `decision_tree`, and `random_forest`. Keys are `(store_id, product_id, dt)`. The evaluator requires exact key, actual, split, model, condition, and run coverage; it rejects missing, extra, duplicate, nonfinite, or mismatched rows. Retrospective target-day metadata is joined after prediction.

## Compatibility matrix

| Model | Feature condition | Prediction schema compatible | Evaluation compatible | Issues/status |
|---|---|---|---|---|
| Linear Regression | `sales_only` | PASS | BLOCKED for current run envelope | CSV is valid, but current SAS run loader expects one manifest-backed run containing both conditions for a model; DEVGRU currently has separate files/run IDs. |
| Linear Regression | `stockout_aware` | PASS | BLOCKED for current run envelope | Same issue; no SAS-owned adapter was changed. |
| Ridge Regression | `sales_only` | PASS | BLOCKED for current run envelope | Same issue; alpha evidence is separate and valid. |
| Ridge Regression | `stockout_aware` | PASS | BLOCKED for current run envelope | Same issue; alpha evidence is separate and valid. |
| Decision Tree | `sales_only` | PASS in SAS-generated envelope | PASS for recorded development evaluator path | Real SAS outputs are documented in `docs/SAS_INTEGRATION_EVIDENCE.json`, but generated result files are ignored/not present in this checkout for independent byte audit. |
| Decision Tree | `stockout_aware` | PASS in SAS-generated envelope | PASS for recorded development evaluator path | Same limitation; no DEVGRU changes made. |
| Random Forest | both conditions | NOT IMPLEMENTED | NOT AVAILABLE | No implementation or output was found; it remains optional and pending. |

## SAS evaluator findings

The local evaluator enforces train/validation-only development scoring in `src/evaluation_SAS/v2.py:28-34` and `scripts/sas_v2.py:20-23`. It validates exact prediction columns, complete authoritative coverage, actual/split identity, both feature conditions, unique model run IDs, and finite values in `src/evaluation_SAS/v2.py:70-110`. `evaluate_predictions` joins retrospective metadata after prediction and computes paired comparisons in `src/evaluation_SAS/v2.py:166-214`. The run adapter verifies artifact hashes and rejects learned-model test scoring in `src/evaluation_SAS/runs.py:144-193`.

The evaluator is therefore structurally compatible with DEVGRU files, but not directly with the four-file packaging shape. Farzaan must either accept a reviewed manifest/adapter that combines the two conditions per model without changing prediction values, or explicitly document a supported multi-run ingestion convention. This is a SAS integration decision; no SAS code was modified.

The evaluator's `MAE_reduction` field is `MAE_sales_only - MAE_stockout_aware`, while DEVGRU's stored bootstrap field is explicitly `MAE(stockout_aware) - MAE(sales_only)`. These are opposite signs and must remain clearly labeled during integration.

## Cross-team conclusions

- Shared keys, actuals, split labels, feature labels, and prediction columns: **PASS** for DEVGRU artifacts.
- Exact paired-population integrity: **PASS** within DEVGRU artifacts; SAS evaluator has matching keyed checks.
- Direct SAS run-envelope ingestion: **BLOCKED / NEEDS TEAM APPROVAL** because DEVGRU has four separate run IDs/files rather than one manifest-backed combined run per model.
- SAS Decision Tree results: **PASS WITH LIMITATIONS** based on recorded integration evidence; local generated artifacts were not available for fresh independent hash verification.
- Random Forest comparison: **NOT IMPLEMENTED**.
- Final comparison readiness: **BLOCKED** until the run-envelope shape, shared tuning/tie policy, uncertainty unit, and technical contract are accepted.
