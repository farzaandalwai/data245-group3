# Shared interfaces - V2 producer 2.0.0; experiment contract DRAFT

The [v2 protocol](experiment_protocol.md) is scientific authority. DELTA's producer schema/serialization, quality checks, feature spellings and deterministic sampling are now **IMPLEMENTED / VERIFIED operationally** under the user's explicit DELTA authorization. See [the technical handoff](DELTA_DATA_HANDOFF.md) for exact files, commands and measured counts. Undocumented business semantics/export lineage remain **PROVISIONAL**. Learned-model preprocessing, tuning, postprocessing and uncertainty remain **DRAFT CONTRACT**; `contract_frozen: false` blocks final scoring.

## Shared observation and bundle

DELTA owns the authoritative producer for the 200-series development pilot and generated 1,000-series final sample. Existing pilot/manifest bytes are historical inputs, not the final sample. Implemented bundle root: `data/processed/feature_bundles/<bundle_id>/`; exact filenames and paths are registered in the handoff.

| Requirement | Existing/proposed fields and meaning |
| --- | --- |
| Stable observation key | `(store_id, product_id, dt)`; `dt` is ISO target date; preserve source ID identity |
| Actual | Normalized recorded `sale_amount`; implemented modeling/prediction alias `actual`, exactly equal to source target |
| Split | `split`: `train`, `validation`, `test`, assigned by protocol calendar |
| Common predictors | Explicit `sales_only` allowlist below |
| Added history | Explicit stockout allowlist below; union with common list gives `stockout_aware` |
| Evaluation metadata | Retrospective target-day stockout count/status and stocked/stockout group, separate from model inputs; implemented names in handoff; operational definition verified, business semantics provisional |
| Lineage | Experiment version, development/final purpose, sample manifest/hash, source revision/hash, timing provenance, eligibility/filter counts/reasons, bundle/schema version/hash |

IDs are keys only. Source `sale_amount`, `stock_hour6_22_cnt`, `hours_stock_status`, `hours_sale`, inherited prediction columns, subgroup metadata and split/day metadata stay outside predictor allowlists. The calendar features below are the only approved target-date inputs.

## Approved concepts and implemented column spellings

Concepts are approved; producer v2.0.0 implements these ordered allowlists:

- `sales_only`: `sales_lag_1`, `sales_lag_2`, `sales_lag_3`, `sales_lag_7`, `sales_lag_14`, `sales_mean_7`, `sales_mean_14`, `weekday`, `is_weekend`.
- Added stockout features: `stockout_hours_lag_1`, `stockout_hours_mean_7`, `stockout_hours_mean_14`, `stockout_day_fraction_7`, `stockout_day_fraction_14`.
- `stockout_aware`: ordered union of both lists, with shared values unchanged.

For target `t`, lag `k` reads `t-k`; each `w`-day rolling mean/proportion uses prior dates `t-w` through `t-1`, grouped/sorted by series. Retain prior stockout days in history. Positive count defines an annotated stockout day; the verified local count sums indices [6:22] of 24 binary values (1=stockout). Weekday is Monday=0; weekend is Saturday/Sunday. Business-hour missing/closed handling remains provisional.

One common target mask starts from day 15 and implemented sample/history/quality rules (fail on invalid records; exclude incomplete series), with no exclusion solely for target-day stockout. Conditions must share identical keys, actuals and splits. All model families use the same comparison observations; baselines use the same evaluation population. Do not silently drop failures, join by row position or redefine selection in an adapter. The evaluator joins target-day subgroup metadata by key after prediction.

## Prediction exchange

Implemented producer/baseline exchange columns: `store_id`, `product_id`, `dt`, `actual`, `prediction`, `model`, `feature_set`, `split`, `run_id`. Serialization/types: preserve source integer IDs, ISO dates, finite numeric actuals/predictions, string labels. `feature_set` uses `sales_only`/`stockout_aware`; split uses the three values above. Baselines use `feature_set=common_reference` once per model; no separate stockout-aware variant.

Within a run require unique `(store_id, product_id, dt, model, feature_set, split)`. Separate run namespaces prevent collisions. Learned models emit paired conditions with exact shared evaluation keys/actuals. Outputs belong beneath owner/model result folders; a proposed `results/predictions/` exchange manifest should point to authoritative outputs. Preserve historical baseline schema/bytes (`sale_amount` actual, no feature-set/run ID); future adapters write separate outputs.

Runs record experiment/protocol and technical-contract versions, development/final purpose, sample manifest/hash, feature definitions, input/bundle hashes, hyperparameters, random seed, train-fitted preprocessing, validation tuning policy/budget and selected settings, source revision, environment, prediction policy, date, owner, checks and evidence status. Freeze choices before new test evaluation. Metadata serialization and prediction postprocessing remain draft.

## Evaluator checks and dependencies

SAS's evaluator must reject missing/extra/duplicate keys, split inconsistencies, target mismatches, nonfinite predictions, incorrect model/condition coverage and incompatible experiment/sample/bundle versions. Compare to the shared expected key set rather than an inner join hiding failures. Check subgroup metadata coverage separately; never remove stockout targets to repair a primary-population comparison. Empty groups are not evaluable, not zero error. Metrics follow the protocol.

The current tree registers [V2 metadata](../configs/contract.yaml) and preserves [historical V1 evidence](history/contract_v1/README.md) separately. V1 does not freeze V2. Git ancestry integration is complete in base `5dcd128`; this DELTA task is local and uncommitted. Human producer acceptance, remaining business-semantics limitations, learned-model settings/validation choices and uncertainty require review. Final input generation is not permission for final scoring. DEVGRU/SAS can implement against the synthetic fixture and development bundle now; see [handoff](DELTA_DATA_HANDOFF.md).
