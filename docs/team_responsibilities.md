# Active three-person responsibilities

**APPROVED 2026-11-19:** all three members agreed to the allocation below and the [v2 scientific protocol](experiment_protocol.md). Assignment/agreement is not execution credit. Preserve historical five-member assignments in archival/attribution material.

| Owner | Paths | Responsibilities |
| --- | --- | --- |
| DELTA - Timothy Tran | `src/data_preprocessing_DELTA/`, `src/features_DELTA/`, `src/models/baselines_DELTA/`, `notebooks/DELTA_data/`, data/manifests and baseline outputs | Central authoritative dataset/data contract; raw validation; preparation and 200/1,000-series selection; chronological splits; all shared sales/stockout features and manifests; persistence/7-day baselines; provenance/preprocessing checks |
| DEVGRU - Shoury | Linear/ridge components under `src/models/`, `notebooks/DEVGRU_linear_models/`, matching result directories | Core Linear Regression; approved Ridge extension; model-specific training/tuning; standardized prediction outputs |
| SAS - Farzaan Dalwai | Tree/forest components under `src/models/`, `src/evaluation_SAS/`, `notebooks/SAS_evaluation/`, matching outputs/comparisons | Core Decision Tree; optional approved Random Forest; shared evaluation/comparison; leakage/integration checks; figures and result summaries |

All three share scientific decisions, final integration, review and submissions. Each individual report reflects actual contributions and distinct prose. Integration ownership does not transfer teammates' authorship or authorize their report writing. The GitHub identity map is in [context](../context.md).

## Shared producer and dependencies

DELTA alone produces the approved shared dataset/features. DEVGRU and SAS consume them without independently redefining targets, sampling, eligibility, windows, split boundaries, shared evaluation keys or metrics. Use the [interfaces](interfaces.md) and explicit predictor allowlists.

V1 evidence/tests are now separated from active V2 checks in the local tree. DELTA producer v2.0.0 and test-only fixture are implemented; see [handoff](DELTA_DATA_HANDOFF.md). Base ancestry integration is complete. Owners can build their components against the producer interface while jointly finalizing remaining model/evaluation details. Fixtures are never research evidence. Real runs need DELTA's common validated bundle; comparisons need accepted predictions; test evaluation also needs frozen validation selections. DELTA producer and development baselines are verified operationally; learned models/common evaluator remain pending.

Use separate clones and task branches/worktrees for normal implementation. Coordinate shared docs/configs/dependencies and other owners' implementations; issue assignments are not locks. Preserve valid context/contribution updates, review and merge one PR at a time, then fetch/reread. The current DELTA implementation request requires NEW-only implementation with no commit, push or merge.
