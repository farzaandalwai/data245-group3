# DELTA V2 implementation report

Completed local implementation, 2026-11-19 (America/Los_Angeles). Human review pending.

Owner: DELTA, user-confirmed Timothy Tran. Branch: `DELTA/v2-data-pipeline`, from fetched `origin/main` at `5dcd128`. Initial tree clean; fetched base and HEAD identical. Work stays in the explicitly required NEW directory, overriding the default separate-clone workflow. No commit, staging, push or merge authorized.

Authorized files: DELTA preprocessing/features/baselines, behavioral tests, CLI, active configuration and affected documentation. Dependencies: canonical pilot/manifest, verified local raw export, source stockout documentation, pandas/NumPy/PyYAML in ignored `.venv`. Other model owners' implementations and historical evidence are excluded.

Acceptance: validated immutable development/final bundles with identical feature-condition keys, deterministic sampling and artifact hashes, prior-only features, development baseline outputs, behavioral and historical checks, documented semantic limitations and no final test scoring. Shared producer decisions are recorded in the handoff; learned-model settings remain pending joint review.

## 1. Executive Summary

**CREATED / IMPLEMENTED / VERIFIED operationally:** centralized validation, sampling, shared features, immutable bundles, consumer loader, synthetic fixture, development baselines and tests. Development has 15,200 observations; final inputs have 76,000. **PROVISIONAL:** undocumented closed/missing-hour business semantics, export lineage and normalization coefficient. **NOT IMPLEMENTED:** learned models, common SAS evaluator and final comparisons/uncertainty. No final predictions or metrics were computed.

Authenticated GitHub identity was `Timothytran109`, matching DELTA. No open issues/PRs at inspection; local/fetched base were identical. The scope and acceptance above were recorded before implementation. No teammate messages or assignments were made.

## 2. Source and Migration Inventory

[Inventory](DELTA_MIGRATION_INVENTORY.json) records 44 OLD source/notebook/data/result/document files, sizes, hashes and preservation references. All 44 were rehashed unchanged afterward. Unique OLD stocked-only/secondary results remain **HISTORICAL** intact read-only references, outside active results. Existing identical NEW copies were not duplicated. Large historical tables were preserved by verified reference rather than copied into Git.

## 3. Files Reused from OLD

`src/prepare_and_baselines.py`: completeness, chronological splitting and baseline concepts adapted from legacy DELTA work. `src/build_features.py`: grouped shifts, shifted rolling means, positive-stockout fractions, calendar features and reconstruction concept reused. Old target-stockout filtering and hardcoded stocked-only/200-series assertions were removed. Canonical pilot/manifest bytes are unchanged. Notebook JSON was inspected without execution; no competing notebook producer was added. Historical attribution is preserved.

## 4. Files Newly Implemented

- `src/data_preprocessing_DELTA/v2.py`: validation, completeness, sampling, keyed subsets and coverage.
- `src/features_DELTA/v2.py`: features, eligibility audit and independent NumPy-slice reconstruction.
- `src/features_DELTA/bundle.py`: immutable transactional publication, schemas, hashes and consumer checks.
- `src/models/baselines_DELTA/v2.py`: common-reference forecasts and development-only scoring/provenance.
- `scripts/delta_v2.py`: build/verify/baselines CLI.
- `scripts/verify_delta_v2.py`: real artifact byte reproduction without final scoring.
- `tests/test_delta_v2.py`: 17 behavioral methods and edge subcases.

Dependencies were installed only in ignored `.venv`. `requirements-v2-tested.txt` captures the tested environment; `requirements.txt` retains primary declarations. No undeclared runtime package was introduced.

## 5. Raw Dataset Provenance and Verified Hash

OLD `data/freshretail.csv` was copied to NEW `data/raw/freshretail.csv` without modifying OLD. Both measure **323,577,557 bytes**, SHA-256 **`6d956f6cab0094e794beb97872d9047d7c49469d35044930f5d8a96a307110b5`**. The absent destination was created exclusively and rehashed. It is ignored and not staged.

Measured **1,459,198 records / 19 columns / 16,214 series / 16,213 complete series / 184 stores / 417 products**, dates 2024-03-28 through 2024-06-25. Full header and quality details are in [run evidence](DELTA_V2_RUN_EVIDENCE.json). Required fields were validated across all records; unused covariates were not semantically validated. Byte identity is not upstream lineage verification.

## 6. Stockout Semantic Verification

The [publisher dictionary](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md) and [pinned publisher code](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/exp/data/generate_data.py) describe scaled sales, hourly stockout status, 24 entries, 1=stockout and slice [6:22]. Every local vector reconciles with the exported count: **zero mismatches in 1,459,198 records**. Counts are bounded 0-16; endpoint tests distinguish hours 5/6/21/22.

**PROVISIONAL:** `fully_stocked` means zero annotated stockout in [06:00,22:00), not unrestricted availability. No invalid/missing sentinel occurred in required local data; upstream closed/missing-hour handling remains undocumented. Exact scaling coefficient and export extraction procedure remain unknown. Fully verified final business-semantic acceptance is not claimed.

## 7. Data Validation Changes

Required fields/types, null/invalid keys, finite nonnegative sales, integer IDs/counts, bounds, exact calendar, duplicates and vector/count reconciliation fail before publication. No imputation. Sorting normalizes order, not proves source order. Incomplete valid series are separate exclusions: `(420,764)` has 28 dates and 62 missing days. Selected series all have exactly 90 approved dates.

Precision reconciliation found **54 canonical pilot sales floats** differing from raw by at most **4.440892098500626e-16**, due to legacy serialization. Development preserves canonical values; final uses raw. Explicit rtol/atol 1e-12 comparison and manifest disclosure bound this difference; keys/calendar remain exact. All conditions/models within a bundle share identical targets. No canonical bytes were rewritten.

## 8. Development Sampling and Dataset

Original 200-series manifest/18,000-row pilot preserved. Coverage **113 stores / 113 products**. Generated **9,200 train / 3,000 validation / 3,000 test** targets. Warmup excludes 2,800 train rows; zero additional quality or target-stockout exclusions. Independent reconstruction verified **212,800 predictor values**, plus keys/actuals/splits.

## 9. Final 1,000-Series Selection

Rank complete-series keys by SHA-256 of ASCII `v2|245|integer_store|integer_product`, break ties numerically, take 1,000, serialize in numeric order. No outcomes/performance influence selection. Simple ranking avoids unstable tiny strata; coverage does not guarantee representativeness. Full-90-day completeness is retrospective availability selection.

Coverage **183/184 stores**, **239/417 products**, **1,000/16,213 = 6.1679%** of complete series. Training stockout-day fraction min/Q1/median/Q3/max: **0.133333/0.35/0.433333/0.533333/1.0**; population: 0.033333/0.35/0.433333/0.533333/1.0. No selected series had zero training stockout days. Selection reproduces; held-out outcome perturbations do not change ranking. Final inputs are not a completed experiment.

## 10. Exact Feature Definitions

Sales-only: `sales_lag_1`, `sales_lag_2`, `sales_lag_3`, `sales_lag_7`, `sales_lag_14`, `sales_mean_7`, `sales_mean_14`, `weekday`, `is_weekend`.

Stockout-aware adds `stockout_hours_lag_1`, `stockout_hours_mean_7`, `stockout_hours_mean_14`, `stockout_day_fraction_7`, `stockout_day_fraction_14`. Lag k reads t-k; mean/fraction w reads t-w through t-1 within series. Positive count defines a historical stockout day. Weekday Monday=0; weekend Saturday/Sunday=1. No scaling/imputation/fitting. IDs, target-day stockouts, targets/splits and inherited predictions are excluded from X. `feature_spec.json` records ordered names, types, units and timing.

## 11. V2 Eligibility and Target Retention

One mask retains every otherwise valid day 15 onward, including stockouts. First target April 11; train ends May 26; validation May 27-June 10; test June 11-25. Final counts **46,000 / 15,000 / 15,000**; 14,000 warmup rows, zero further exclusions. Feature conditions share exact keys/common values. Independently reconstructed **1,064,000 final predictor values** and keys/actuals/splits. Earlier observed evaluation dates supply rolling one-day history without refitting.

## 12. Shared Bundle Contract

Producer `2.0.0`, protocol `2.0`; overall contract `2.0-draft`, unfrozen. [Handoff](DELTA_DATA_HANDOFF.md) specifies ten files and keyed loader. CSV uses 17 significant digits, integer IDs and ISO dates. Manifests record artifact/source/sample/module hashes, revision, environment, purpose, configuration, counts and limits. Trusted top-level hashes are in run evidence. Immutable source copies: `data/manifests/v2-source-r2/`. Publication validates a temporary sibling then renames; overwrite is rejected. Consumers need only the bundle.

Authoritative **r2** explicitly records precision reconciliation and actual generation date. r1 remains intact as superseded verification output. Configuration snapshots precede subsequent active status/path updates and were not retroactively edited.

## 13. Baseline Implementation and Results

Persistence and preceding-seven-day mean use shared keys/actuals/splits and `feature_set=common_reference`. No fitting/tuning/clipping. **CREATED / VERIFIED development only:** 30,400 predictions, six metric groups and run manifest. Exact numeric/CSV-byte reproduction passed. Historical test exposure remains disclosed; final scoring is rejected.

| Model | Split | Rows | MAE | RMSE | Signed bias |
| --- | --- | ---: | ---: | ---: | ---: |
| Persistence | Train | 9,200 | 0.411151087 | 0.657686864 | -0.008985870 |
| Persistence | Validation | 3,000 | 0.417756667 | 0.677440748 | +0.002356667 |
| Persistence | Test (development) | 3,000 | 0.444063333 | 0.697379834 | -0.002776667 |
| Recent average 7 | Train | 9,200 | 0.338660093 | 0.534540597 | -0.013435870 |
| Recent average 7 | Validation | 3,000 | 0.337380476 | 0.551964787 | -0.007275714 |
| Recent average 7 | Test (development) | 3,000 | 0.362621905 | 0.564407043 | -0.051646667 |

These are recomputed development results, not final improvement evidence. Agreement with inherited validation/test metrics is expected where rows/formulas coincide; metrics were not copied.

## 14. Automated Test Coverage

17 methods cover the requested categories through edge subcases: required/null/invalid fields/keys, duplicates/missing/wrong dates, finite values/count bounds/vector reconciliation, sampling/held-out independence, series isolation, golden windows/day-15/split edges, stockout retention, target/future perturbations, allowlists/paired keys/targets/splits, metadata exclusion, baseline formulas/coverage, deterministic serialization/tampering/overwrite protection, purpose separation and scoring gates. Independent real reconstruction uses NumPy slices rather than repeating pandas rolling expressions.

Active status tests reflect generated inputs; scientific gates and historical V1 tests remain intact. Setup now excludes ignored environment/cache Markdown from repository retention checks, retaining explicit raw-ignore safeguards.

## 15. Test Results and Failures

**35 passed / 0 failed:** 17 behavioral, 10 active V2, 5 historical V1, 3 layout. Setup integrity/link/ignore checks passed. `python -m scripts.verify_delta_v2` passed source identity, three bundles, selection reproduction, **10 real CSV byte hashes**, source snapshots and **two development baseline CSV byte hashes**, without final scoring. CLI final-bundle verification passed. All 44 OLD hashes remained unchanged; staging and historical/canonical diffs were empty.

Fixed initial issues: oversized IDs raised TypeError (now meaningful ValueError); pandas deprecated aliases (updated); setup expected ignored pytest-cache README tracking (cache exclusion corrected); raw-based development byte reproduction exposed legacy precision differences (canonical preserved, tolerance tightened/documented, correct input used). No unresolved required test failure. Learned-model/other-machine validation is not claimed.

## 16. Generated Artifact Paths and Sizes

| Path | Bytes | Status |
| --- | ---: | --- |
| `data/raw/freshretail.csv` | 323,577,557 | COPIED / VERIFIED local identity |
| `data/processed/feature_bundles/v2-development-200-r2/` | 6,284,204 | CREATED / VERIFIED operational; PROVISIONAL business semantics |
| `data/processed/feature_bundles/v2-final-1000-r2/` | 31,373,083 | CREATED / VERIFIED inputs; final scoring pending |
| `data/processed/feature_bundles/v2-synthetic-fixture-r2/` | 54,597 | CREATED / VERIFIED test-only |

Baseline files: `results/baselines_DELTA/v2/v2-development-baselines-r2/`. All individual sizes/hashes, including baseline files, are in [run evidence](DELTA_V2_RUN_EVIDENCE.json). Superseded r1 outputs/source snapshots remain intact and ignored. Synthetic data are never research evidence.

## 17. Git Tracking and Ignore Verification

Raw, generated bundles/source snapshots and baseline outputs are ignored. No staging/publication/history rewrite occurred. Original archive, V1 evidence, canonical pilot/manifests and inherited results have no diff. Base ancestry is integrated at `5dcd128`; earlier unresolved-merge descriptions are historical. Branch `DELTA/v2-data-pipeline`, no PR. Human review precedes separately authorized publication.

## 18. Updated Documentation

Affected active README/AGENTS/context/starter guidance, interfaces, technical protocol status, methodology, ownership dependencies, YAML, data/src/results/tests/notebook READMEs, provenance and experiment/AI/contribution records are synchronized. Scientific target/features/population/splits did not change. Exact prompt preserved; historical logs appended to. Changed/new files are listed below.

## 19. DELTA-to-DEVGRU/SAS Handoff

Ready for keyed consumers/adapters using producer 2.0.0, test fixture and operationally verified development inputs. Obtain ignored bundles from DELTA and pin manifest hashes. [Handoff](DELTA_DATA_HANDOFF.md) has exact paths, allowlists, joins, schema and commands. Consumers need not execute preprocessing. Teammate implementations/reports remain theirs; human producer acceptance is pending.

## 20. Remaining Risks or Blockers

Final acceptance remains provisional for closed/missing-hour business handling, export lineage and normalization coefficient. Human review, learned-model preprocessing/postprocessing, tuning budgets/settings, validation choices and uncertainty require joint freeze before final scoring. Learned models/common evaluator/final findings are **NOT IMPLEMENTED**. Historical holdout exposure and retrospective completeness limit inference. Local bundles are not distributed by Git; teammate environments remain unverified. No sustainability finding is supported.

## 21. Final Technical Assessment

Authorized DELTA implementation/local generation are complete and operationally verified; final inputs exist with explicit provisional limits. Final findings remain intentionally gated. Next: human source/test/handoff/evidence review, producer acceptance and owned consumer work; publication requires separate authorization.

For independent ChatGPT review, upload this report, handoff, run evidence, migration inventory, protocol/interfaces/configs, DELTA source/CLI/tests, tested requirements and working-tree diff. Include the synthetic bundle for executable contract review. Raw/full final data are unnecessary for first review; use appropriate private sharing if later needed.

### Review file inventory

Modified tracked files:

- `.github/copilot-instructions.md`
- `AGENTS.md`
- `README.md`
- `configs/README.md`
- `configs/contract.yaml`
- `configs/dataset.yaml`
- `configs/experiments.yaml`
- `configs/models.yaml`
- `context.md`
- `data/README.md`
- `data/manifests/README.md`
- `data/processed/README.md`
- `data/raw/README.md`
- `docs/ai_assistance.md`
- `docs/contributions.md`
- `docs/experiment_log.md`
- `docs/experiment_protocol.md`
- `docs/interfaces.md`
- `docs/methodology.md`
- `docs/provenance.md`
- `docs/team_responsibilities.md`
- `notebooks/DELTA_data/README.md`
- `notebooks/README.md`
- `results/README.md`
- `results/baselines_DELTA/README.md`
- `results/predictions/README.md`
- `scripts/verify_setup.py`
- `src/README.md`
- `src/data_preprocessing_DELTA/README.md`
- `src/features_DELTA/README.md`
- `src/models/baselines_DELTA/README.md`
- `src/models/decision_tree_SAS/README.md`
- `src/models/linear_regression_DEVGRU/README.md`
- `src/models/random_forest_SAS/README.md`
- `src/models/ridge_regression_DEVGRU/README.md`
- `starter_prompt.md`
- `tests/README.md`
- `tests/test_shared_contract.py`

New reviewable files:

- `docs/DELTA_DATA_HANDOFF.md`
- `docs/DELTA_MIGRATION_INVENTORY.json`
- `docs/DELTA_V2_IMPLEMENTATION_REPORT.md`
- `docs/DELTA_V2_RUN_EVIDENCE.json`
- `docs/prompts/2026-11-19-delta-v2-implementation.txt`
- `requirements-v2-tested.txt`
- `scripts/delta_v2.py`
- `scripts/verify_delta_v2.py`
- `src/data_preprocessing_DELTA/v2.py`
- `src/features_DELTA/bundle.py`
- `src/features_DELTA/v2.py`
- `src/models/baselines_DELTA/v2.py`
- `tests/test_delta_v2.py`
