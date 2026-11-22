# Evidence Index

## Project and protocol

- `README.md` — project scope, status, and historical test-exposure disclosure.
- `docs/experiment_protocol.md` — approved scientific protocol and feature/split rules.
- `docs/interfaces.md` — canonical prediction exchange schema.
- `docs/contract_freeze.md` — contract remains unfrozen and final scoring is blocked.
- `docs/DELTA_DATA_HANDOFF.md` and `docs/DELTA_V2_IMPLEMENTATION_REPORT.md` — DELTA producer and bundle evidence.
- `docs/team_responsibilities.md` — ownership boundaries.

## Harmonized R3 evidence

`artifacts/SAS/development/harmonized-200-series-20261120-r3/` contains the comparison manifest, coverage and input acceptance audits, comparison tables, paired intervals, per-series/per-store/subgroup tables, validation baseline predictions, figures, README, and `PACKAGE_SHA256SUMS`. The manifest records hash `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`, validation-only scoring, no retraining, and no test scoring. Its `bundle_id` field is null; no bundle ID is inferred.

## Decision Tree evidence

`artifacts/SAS/development/original-200-series-20261119/decision_tree/` contains predictions, metrics, manifest, numeric trees, selection, coverage audit, and paired intervals. Predictions have canonical columns, 24,400 rows, 18,400 train rows, 6,000 validation rows, and zero test rows. The manifest identifies the development bundle by the trusted hash.

## Baselines and source

- `results/baselines_DELTA/inherited/` contains inherited baseline predictions, metrics, and data audit.
- `src/models/linear_regression_DEVGRU/` and `src/models/ridge_regression_DEVGRU/` contain source/tests, but original DEVGRU prediction artifacts are absent.
- `src/models/random_forest_SAS/` contains RF source/policy/README and `tests/test_sas_forest.py`; generated RF outputs are absent.
- `docs/SAS_RANDOM_FOREST.md` is a report of a separate run, not independently verified artifact evidence here.

## Missing evidence

Exact DEVGRU prediction CSVs, DEVGRU run metadata/alpha records, exact DELTA development bundle, and serialized fitted models are not present in this isolated worktree. No final 1,000-series bundle was accessed.
