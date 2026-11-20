# DEVGRU development-results audit

Audit status: **PASS WITH LIMITATIONS**. This audit independently checked the existing DEVGRU implementation and development artifacts without changing them. No final bundle was opened, no test predictions or scores were generated, and no existing output was overwritten.

## Scope and repository state

Audited the DEVGRU model core, Linear and Ridge implementations, development runner, tests, decision documentation, development report, run metadata, all generated prediction/metric/bootstrap artifacts, and the shared prediction interface.

- Branch: `DEVGRU/linear-ridge-models`
- HEAD: `d2a323e` (`merge: integrate DELTA V2 data pipeline`)
- Working tree: existing DEVGRU files remain untracked and unstaged; no shared, DELTA, SAS, protocol, config, bundle, or historical files were changed.
- The known inaccessible `.codex_tmp_verify/tmp8nioeec1` directory still causes Git/repository-wide filesystem warnings.

## Implementation audit

### Findings

- **Feature allowlists: PASS.** `sales_only` contains the exact nine producer features in order; `stockout_aware` contains those nine followed by the exact five stockout-history features. Model matrices use `feature_names(feature_set)`, not exclusion-based discovery.
- **Predictor safety: PASS.** IDs, `actual`, split labels, target-day stockout metadata, raw source fields, and inherited predictions are excluded. The target-day evaluation metadata table is not consumed by the model runner.
- **Joins and paired populations: PASS.** Bundle joins use one-to-one keyed validation. Paired conditions require equal keys, actuals, and splits. Independent artifact checks confirmed this for both model families.
- **Preprocessing: PASS.** Standardization is fitted on training rows only and reused for validation. Zero-variance columns use scale 1.0.
- **Linear Regression: PASS.** Uses explicit-intercept NumPy least squares.
- **Ridge Regression: PASS.** Uses augmented least squares with `sqrt(alpha)` coefficient penalties and an unpenalized intercept. Positive finite alpha validation is enforced.
- **Alpha selection: PASS.** Candidates are bounded, unique, positive, and finite; fitting uses training rows; selection uses validation MAE only; equal-MAE ties select the smaller alpha. Test feature values are not used for fitting or scoring.
- **Test isolation: PASS.** `fit_predict_bundle`, `prediction_frame`, and `verify_prediction_frame` all reject test rows. Generated files contain no test rows.
- **Prediction validation: PASS.** Exact schema/order, ISO dates, finite values, supported labels, single model/feature-set/run ID, unique keys, and authoritative key/actual/split correspondence are checked.

No implementation weakness affecting the completed development results was found. Exact tie-breaking was regression-tested but was not exercised by an exact tie in the stored Ridge candidate results.

## Bundle audit

Only `data/processed/feature_bundles/v2-development-200-r2` was loaded. Its trusted top-level manifest hash independently matched:

`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`

The documented DELTA verification command passed with split counts `train=9200`, `validation=3000`, `test=3000`. The report and run metadata contain the same bundle ID and hash. The development bundle contains the expected 200-series population. No path or command accessed the final 1,000-series bundle.

## Artifact inventory and integrity

Run root:

`runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/`

Verified generated files:

- `linear_regression/sales_only.predictions.csv`
- `linear_regression/stockout_aware.predictions.csv`
- `ridge_regression/sales_only.predictions.csv`
- `ridge_regression/stockout_aware.predictions.csv`
- `ridge_alpha_selection.csv`
- `validation_metrics.csv`
- `paired_validation_comparison.csv`
- `run_metadata.json`
- `development_report.md`

Each prediction file has 12,200 rows: 9,200 train and 3,000 validation. Each has exactly:

`store_id,product_id,dt,actual,prediction,model,feature_set,split,run_id`

Independent checks confirmed zero test rows, unique keys, finite actuals/predictions, supported labels, and run IDs matching the DEVGRU report. All four files matched authoritative development-bundle actuals and splits. Sales-only and stockout-aware files had identical paired keys, actuals, and split assignments within each model family.

## Independent metric recomputation

Metrics were recomputed directly from the stored prediction CSVs using MAE, RMSE, and `mean(prediction - actual)`. Full-precision recomputation matched the stored metrics; report values are rounded to six decimal places only.

| Model | Feature set | Split | Rows | MAE | RMSE | Signed bias |
|---|---|---:|---:|---:|---:|---:|
| Linear | `sales_only` | train | 9,200 | 0.3228437204 | 0.5047871595 | 1.1593e-15 |
| Linear | `sales_only` | validation | 3,000 | 0.3342568283 | 0.5359985311 | 0.0039126593 |
| Linear | `stockout_aware` | train | 9,200 | 0.3186788241 | 0.5001610836 | 1.3773e-15 |
| Linear | `stockout_aware` | validation | 3,000 | 0.3341904534 | 0.5326892561 | -0.0063269440 |
| Ridge | `sales_only` | train | 9,200 | 0.3228378132 | 0.5047895887 | 1.3666e-15 |
| Ridge | `sales_only` | validation | 3,000 | 0.3342560218 | 0.5358897268 | 0.0037910809 |
| Ridge | `stockout_aware` | train | 9,200 | 0.3186744293 | 0.5002694334 | 1.3755e-15 |
| Ridge | `stockout_aware` | validation | 3,000 | 0.3341189138 | 0.5318851793 | -0.0069271260 |

Stored Ridge candidate evidence independently supports:

- `sales_only`: selected alpha `10.0`, validation MAE `0.3342560218`.
- `stockout_aware`: selected alpha `100.0`, validation MAE `0.3341189138`.

## Paired bootstrap audit

The stored procedure and results were independently reproduced from prediction files:

- Pairing key: `(store_id, product_id, dt)`.
- Difference: `MAE(stockout_aware) - MAE(sales_only)`.
- Resampling unit: whole `(store_id, product_id)` series.
- Series count: 200.
- Repetitions: 2,000.
- Interval: percentile 95%.
- Seeds: 245 for Linear and 246 for Ridge.
- The same sampled series indices were used for both conditions within each replicate.

| Model | Difference | Independent 95% CI | Stored 95% CI |
|---|---:|---:|---:|
| Linear | -0.0000663749 | [-0.0023230173, 0.0021569316] | [-0.0023230173, 0.0021569316] |
| Ridge | -0.0001371079 | [-0.0022904930, 0.0019328168] | [-0.0022904930, 0.0019328168] |

The intervals include zero. These are validation-stage development intervals, and Ridge alpha selection also used validation MAE. They do not establish independent final-test confirmation or statistically established improvement.

## Documentation audit

**PASS.** `docs/DEVGRU_development_report.md` matches the stored bundle identity, run IDs, metrics, selected alphas, bootstrap settings, and limitations. It distinguishes train and validation results, labels settings provisional, avoids causal/latent-demand claims, and explicitly states that test and final-bundle evaluation did not occur. `docs/DEVGRU_linear_ridge_technical_decisions.md` continues to mark technical choices as proposed/pending team agreement.

Minor metadata limitation: `run_metadata.json` records the run-ID prefix, model/feature configuration, selected alphas, environment, and split populations, but does not itself enumerate the four per-combination run IDs, prediction paths, or metric rows. Those details are present and consistent in the prediction files, `validation_metrics.csv`, and DEVGRU report. This is a handoff completeness issue, not a numerical inconsistency.

## Integration readiness

The four prediction files are schema-compatible with the shared prediction exchange and can be consumed without column or label changes:

- Model labels: `linear_regression`, `ridge_regression`.
- Feature labels: `sales_only`, `stockout_aware`.
- Split labels: `train`, `validation` only.
- Actuals, keys, and uniqueness: independently verified.
- Metadata: available in `run_metadata.json`, candidate evidence, metrics, and report.

The SAS evaluator is not implemented locally; only `src/evaluation_SAS/README.md` is available. Therefore evaluator execution, comparison-manifest acceptance, and SAS-specific path ingestion are **NOT VERIFIED**. Integration still requires Farzaan's evaluator checks, accepted output paths/manifest, and joint confirmation of the draft technical contract. The current ignored `runs/` location is suitable for audit evidence but may need an agreed handoff path or manifest for SAS consumption.

## Safe verification performed

- Focused DEVGRU tests: `11/11 passed`.
- Python compilation of relevant DEVGRU modules: passed.
- `python -m scripts.delta_v2 verify data/processed/feature_bundles/v2-development-200-r2`: passed.
- `git diff --check`: passed.
- Independent artifact, metric, alpha, key, split, finiteness, and bootstrap checks: passed.

Repository-wide verification remains affected by the pre-existing Windows permission error for `.codex_tmp_verify/tmp8nioeec1`; no permissions were changed and the artifact was not deleted.

## Readiness conclusions

- Scientific correctness: **PASS WITH LIMITATIONS** — development validation is internally consistent, but settings remain provisional, intervals include zero, and no final-test evidence exists.
- Implementation correctness: **PASS** — source inspection, focused tests, bundle checks, and independent recomputation found no correctness defect affecting these results.
- Artifact integrity: **PASS** — four outputs and supporting artifacts are complete, keyed, finite, paired, and test-free.
- Documentation accuracy: **PASS WITH LIMITATIONS** — report values and claims match artifacts; run metadata should be enriched with explicit per-combination paths/run IDs/metrics before formal handoff.
- Integration readiness: **PASS WITH LIMITATIONS** — exchange schema is compatible, but the SAS evaluator and final handoff manifest are unavailable locally and require integration review.

Recommended next actions are metadata/handoff-manifest completion, SAS evaluator ingestion and review, and team confirmation of the provisional technical decisions. No model or scientific redesign is indicated by this audit.
