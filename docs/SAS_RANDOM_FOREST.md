# SAS Random Forest — DEVELOPMENT only (2026-11-20)

Owner: SAS / Farzaan Dalwai. Branch `SAS/random-forest-development`, stacked on
`SAS/development-comparison` (PR #7). Status: **IMPLEMENTED, development-only,
not group-frozen.** No final input was opened and no test row was fitted, predicted
or scored.

## What it is
`src/models/random_forest_SAS/v2.py` mirrors the Decision Tree consumer: DELTA's
exact keys, targets and allowlists (9 common / +5 stockout-aware features), train-only
fitting, validation-MAE selection, no refit, no clipping, first-in-grid tie rule.
Policy: `src/models/random_forest_SAS/development_policy.json`. The depth/leaf grid
(4 x 3 = 12 candidates per condition) and seed 245 equal the tree's, so the tuning
budget is matched; `n_estimators=200`, `max_features=1.0` and bootstrap are fixed and
not tuned. This is a development proposal, not a team-agreed final setting.
No fitted-model file is saved (no executable pickle); the seeded run is reproducible.

## Real development run (exact DELTA r2 bundle, manifest SHA-256
`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`)
Run `sas-forest-dev-200-r1` (ignored local path `results/random_forest_SAS/v2/`);
9,200 train / 3,000 validation rows, 113 validation stores. Selected: sales-only
depth 8 / leaf 5; aware depth 8 / leaf 20.

| Condition | Validation MAE | RMSE | Signed bias |
| --- | --- | --- | --- |
| sales-only | 0.335969 | 0.552579 | -0.003351 |
| stockout-aware | 0.336504 | 0.555457 | -0.019676 |

Aware minus sales-only MAE: **+0.000535**, 95% paired store-cluster interval
[-0.003533, +0.005357] (seed 245, 2,000 replicates). The interval includes zero:
no stockout-feature benefit is established. Forest MAE is better than the Decision
Tree's (0.348255 / 0.352070), slightly worse than Linear/Ridge sales-only (about
0.3343) and the previous-7-day mean's 0.337380 on the same rows. The subgroup split
(1,698 stocked / 1,302 stockout rows) is a retrospective diagnostic only. These
figures condition on validation selection and are not final, causal or
sustainability findings.

Comparison `sas-forest-vs-tree-dev-r1` evaluated the forest and the original tree
predictions together. Since 2026-11-23 the run is shared byte-for-byte under
`artifacts/SAS/development/random-forest-200-series-20261120/` and included in the r4
harmonized comparison with all models and baselines (relative MAE improvement −0.159%).

Local hashes (ignored files): forest `run_manifest.json`
`ba8696f1cc7e780dfee1141be0f4a3e58df547fab98c7e522469e78c92e45bc9`, `predictions.csv`
`dbdd6d333277b894f115b76ce42bf130248fc7b451e91d8a0971190c1dd47462`, `selection.json`
`0c384ff87d34f36ea5869cacf5a78e2931848afc57dcd5d2a8d827175663bcde`; comparison
`comparison_manifest.json`
`1e0ea79d906c444c0f64f69da073e23499b31c4dd1728742c61b089e85bdf038`. The run was made
before these files were committed, so its manifest records a dirty working tree and
the per-file source hashes.

## Reproduce
```sh
python3 -m scripts.sas_v2 train-forest --bundle data/processed/feature_bundles/v2-development-200-r2 --manifest-sha256 043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7 --run-id <new-run-id>
```
Needs DELTA's ignored development bundle. Runtime was about 41 seconds.

## Checks
Seven new synthetic tests in `tests/test_sas_forest.py` cover fit rows, allowlists,
matched budget, test-row isolation, reproducibility, tie rule, fail-closed policy,
a run round trip, and rejection of a final-purpose bundle.

## Still needs the team
Adopt or reject the forest, its fixed `n_estimators`/`max_features` and the grid as
a final setting; tie rule; final workflow and reviewed final-scoring entry point.
