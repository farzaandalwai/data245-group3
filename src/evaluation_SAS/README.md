# Evaluation, leakage audit, and integration — SAS

Status: not implemented. Own the shared metric definitions/implementation, paired-key validation, provenance/timing audit, overall/per-series/store-level and retrospective target-day stocked/stockout subgroup analysis, and store-clustered uncertainty when justified.

The evaluator should consume standardized prediction files rather than import a teammate's notebook or model internals. It can be developed against labeled deterministic fixtures before real predictions exist; fixture results are not findings. Final comparisons need accepted predictions from the same frozen verified bundle. Coordinate the protocol/validation freeze before any new model test evaluation.

Write comparison evidence under `results/comparisons_SAS/`. Integrate one reviewed PR at a time; do not silently merge or replace another owner's valid context/contribution updates.

Follow the [v2 protocol](../../docs/experiment_protocol.md) and [draft interfaces](../../docs/interfaces.md). Primary evaluation includes all otherwise eligible target dates. Secondary test subgroups use retrospective target-day metadata, never predictors or separately trained subgroup models. V1 evidence/tests are now separate from V2 validation; finalize the draft interface before implementation; uncertainty details remain draft.
