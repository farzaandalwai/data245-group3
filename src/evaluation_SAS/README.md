# Evaluation, leakage audit, and integration — SAS

Status: not implemented. Own the shared metric definitions/implementation, paired-key validation, provenance/timing audit, overall/per-series/store-level and history-stockout strata analysis, and store-clustered uncertainty when justified.

The evaluator should consume standardized prediction files rather than import a teammate's notebook or model internals. It can be developed against labeled deterministic fixtures before real predictions exist; fixture results are not findings. Final comparisons need accepted predictions from the same frozen verified bundle. Coordinate the protocol/validation freeze before any new model test evaluation.

Write comparison evidence under `results/comparisons_SAS/`. Integrate one reviewed PR at a time; do not silently merge or replace another owner's valid context/contribution updates.
