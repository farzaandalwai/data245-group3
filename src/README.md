# Source ownership

- `data_preprocessing_DELTA/`, `features_DELTA/`, `models/baselines_DELTA/`: DELTA.
- `models/linear_regression_DEVGRU/`, `models/ridge_regression_DEVGRU/`: DEVGRU.
- `models/decision_tree_SAS/`, optional `models/random_forest_SAS/`, and `evaluation_SAS/`: SAS.

The legacy preparation/downloader remain preserved reproduction tools. DELTA V2 modules now implement shared data/features/baselines; other owners' model/evaluator folders remain guidance only. Read `docs/team_responsibilities.md` and `docs/interfaces.md` first. Imports shown in the handoff work from repository root using Python namespace packages; this repository is not a separately installed distribution.

## DELTA V2 update - 2026-11-19

DELTA V2 producer and baselines are implemented; learned models/common evaluator remain pending. See [handoff](../docs/DELTA_DATA_HANDOFF.md).
