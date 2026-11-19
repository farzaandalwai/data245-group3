# Shared handoff interfaces — draft v0

Status: workspace contract draft, not a verified feature/eligibility implementation. Paths and active ownership are established by this migration; stockout semantics/indexing, exact predictor columns/statistics, preprocessing details, filter counts, and final run schema agreement still require the next bounded review. `configs/experiments.yaml` deliberately records `contract_frozen: false`.

## Common source

DELTA's fixed inputs are `data/processed/pilot_200_series.csv` and `data/manifests/pilot_series_manifest.csv`. Keys are `(store_id, product_id, dt)`; IDs are integer source identifiers but categorical model inputs, dates are ISO `YYYY-MM-DD`, and actual `sale_amount` is recorded normalized sales. Preserve the inherited manifest and original chronological split boundaries. The pilot's existing prediction columns and split/day metadata are not approved predictors.

## Proposed feature bundle

Version under `data/processed/feature_bundles/<bundle_id>/`, with immutable input/bundle hashes and acquisition instructions for other clones. No bundle exists yet.

- One eligible target-key set, split assignment, actual values, and exclusion/filter log shared by both conditions.
- Common feature columns and separately listed additional historical stockout columns; ordered explicit allowlists, dtypes, missingness rules, category policy, rolling-statistic conventions, and feature definitions.
- Eligibility/target-day availability and timing provenance kept separately from predictor frames. Target-day availability must not leak through an automatic all-column selection.
- Original/eligible counts per split and each filter, history-window identity, source hashes, schema/contract version, owner, and validation evidence.

Models consume the bundle rather than recalculate history/eligibility differently. Fit preprocessing using training rows only; model-specific transformations are documented and held matched across feature conditions. Daily features may use prior observed evaluation days without parameter refitting. Exact file names/serialization and predictor lists must be agreed before producers are implemented.

## Proposed prediction schema

Columns: `store_id`, `product_id`, `dt`, `actual`, `prediction`, `model`, `feature_set`, `split`, `run_id`. The first two are source integer IDs, `dt` is ISO date, actual/prediction are finite numbers, and the remaining identifiers are strings. `feature_set` is `sales_only` or `stockout_aware`; `split` is `train`, `validation`, or `test`, with primary evaluation on validation/test. Apply the agreed nonnegative prediction policy consistently. This migration defines no producer.

Within a run, require unique `(store_id, product_id, dt, model, feature_set, split)`. Store multiple runs in separate files/directories and keep `run_id` consistent with their metadata. Both conditions for a model must predict exactly the common eligible evaluation keys with identical actuals/splits. Do not silently drop difficult rows or fill failed predictions without an agreed policy.

Each run also needs model settings, train-fitted preprocessing metadata, validation selection/tuning budget, bundle/schema version and hash, code revision, date, environment, prediction policy, checks, owner, and evidence status. Save a separate run under its owner/model result directory; `results/predictions/` can hold an exchange manifest rather than divergent copies. Generated artifacts remain ignored unless explicitly reviewed for tracking.

Imported baseline files keep their original schema (`sale_amount` as actual, no feature-set/run ID). Preserve them; future matched baseline producers must explicitly adapt to the agreed schema and write separate outputs.

## Independent development and final gates

DELTA builds the shared data/feature layer; DEVGRU builds linear/ridge adapters; SAS builds tree/evaluation adapters. Before real bundle delivery, use a mutually agreed labeled fixture to test interfaces. It must not be confused with the inherited pilot, real training, or evaluation evidence. No fixtures/results were generated during migration.

SAS's evaluator consumes standardized predictions and bundle provenance, not other owners' notebooks. Final model comparisons wait for accepted real predictions from the same frozen bundle. New model test evaluation waits for the protocol/feature/model/metric and validation-choice freeze. Structural independence does not remove those scientific dependencies.
