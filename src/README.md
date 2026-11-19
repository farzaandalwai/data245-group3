# Source ownership

- `data_preprocessing_DELTA/`, `features_DELTA/`, `models/baselines_DELTA/`: DELTA.
- `models/linear_regression_DEVGRU/`, `models/ridge_regression_DEVGRU/`: DEVGRU.
- `models/decision_tree_SAS/`, optional `models/random_forest_SAS/`, and `evaluation_SAS/`: SAS.

The only implemented working code at migration is the path-adapted inherited preparation/downloader. The other component READMEs define ownership, handoffs, and acceptance criteria; they are not completed model/feature implementations. Read `docs/team_responsibilities.md` and `docs/interfaces.md` first. Source folders are not installed Python packages yet; no package/import API is claimed.
