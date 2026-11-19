# Experiment and integration log

Current integration correction (2026-11-19): layout/startup PR #2 merged as `35bfa71`; v1 contract PR #3 merged on fetched main as `1939586`. Earlier pending-integration statements below describe their dated snapshots, not current status. V2 supersedes conflicting v1 definitions; these local v2 edits are uncommitted.

## 2026-11-18 — inherited evidence imported

Source: the original handoff by Timothy Tran, now archived. The fixed pilot, raw-export audit, persistence/seven-day baseline predictions, and four metric rows were imported. Their full pipeline and metric values were not independently reproduced. Original baseline test scores were already visible.

## 2026-11-18 — three-owner structure migration

Owner/requester: SAS. DELTA/DEVGRU/SAS directories, planning configs, current responsibilities and interface/dependency guidance were added. Canonical manifest/results paths moved; all ten originals were preserved in the archive. Working legacy paths were adapted to separate reproduction outputs; the working notebook has cleared execution state. Static/structural tests are migration evidence only. No data pipeline, notebook cells, features, fitting, scoring, or new model test evaluation was executed.

Status: branch work pending human integration into main. See `docs/structure_migration.md`, `context.md`, and Git/PR history for exact scope and checks. No new experimental result exists to record.

## 2026-11-19 - v2.0 three-member methodology approval

**Decision, not an experiment run.** DELTA (Timothy Tran), DEVGRU (Shoury) and SAS (Farzaan Dalwai) agreed to the scientific design supplied in the [saved request](prompts/2026-11-19-methodology-alignment.md). Authority: [approved protocol](experiment_protocol.md); schemas: [v2 DRAFT CONTRACT](interfaces.md).

- Replace stockout-free primary targets with all otherwise eligible targets including stockouts; the historical approximately 43.16% availability exclusion is superseded.
- Evaluate fully stocked/stockout target dates as retrospective secondary test subgroups only; target-day stockouts never enter predictors.
- Preserve the historical 200-series pilot for development; select a separate reproducible 1,000-series final sample, manifest not generated, proposed default seed 245.
- Primary maximum history is 14 days, targets from day 15, established 60/15/15 calendar split. Optional context sensitivities are not core requirements. Final 46,000/15,000/15,000 target counts are projections.
- Require Linear Regression and Decision Tree; approve Ridge and optional Random Forest extensions. Require persistence and 7-day-mean baselines. MAE primary, RMSE and mean(prediction-actual) bias secondary.
- DELTA owns the single centralized data/feature pipeline and baselines; DEVGRU consumes shared outputs for linear/ridge; SAS owns tree/optional forest and shared evaluation. Fair comparisons require shared keys/targets/splits, common predictors and documented matched tuning policies.
- Pending technical work: reconcile fetched main's old v1 definition/lock/tests without erasing historical audit evidence; verify stockout semantics/indexing and raw provenance; finalize selection/coverage, schemas, quality rules, preprocessing, grids/settings, prediction policy and dependence-aware uncertainty; verify environment compatibility.

Status: scientific design **APPROVED**; technical contract **DRAFT**; new sample/features/models/evaluation **NOT IMPLEMENTED**. No preprocessing/training or experiment executed, no gains claimed. Existing baseline test exposure and retrospective completeness limitations remain disclosed. Current-tree documentation task owner: DELTA, authenticated `Timothytran109`; local `main`, no commit/push/branch/merge/PR under this explicit request.

## Future run entries

Record owner, date, branch/PR/revision, contract/bundle/input hashes, target/filter counts, feature set/model/window, train/validation selection and tuning, prediction/run paths, environment, metrics with evidence, checks, deviations, AI assistance/human validation, and integration/test-freeze status. Do not append unexecuted plans as completed runs. Shared log edits must preserve other owners' valid entries.

## 2026-11-19 - V2 semantic contract reconciliation (local, uncommitted)

Owner/requester session: DELTA / Timothy Tran; latest [request](prompts/2026-11-19-v2-semantic-reconciliation.md) authorizes static test/helper and metadata reconciliation. Actual Git inspection found no local V2 commit or merge in progress: `main` is still `35bfa71`, behind fetched `1939586`. No commit, merge, staging or push was performed.

Preserved exact remote V1 contract/audit/four-entry lock/script/tests/freeze/prompt and provenance/AI/contribution records in `docs/history/contract_v1/`. Active V2 metadata registration and tests now enforce all otherwise eligible targets, day-15/14-day history, exact approved features, key-only IDs and approved extensions; V1 assertions reproduce only under historical tests. Useful parser/endpoints, source evidence, matching-key/paired-feature and train/validation/test safeguards are retained without freezing pending producer semantics. Technical interfaces remain DRAFT; no ML implementation, final sample/features/results or score improvements claimed. See [reconciliation record](V2_RECONCILIATION.md) for actual checks and Git handoff.
