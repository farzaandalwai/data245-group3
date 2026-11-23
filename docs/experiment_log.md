# Experiment and integration log

Current integration correction (2026-11-19): layout/startup PR #2 merged as `35bfa71`; v1 contract PR #3 merged on fetched main as `1939586`. Earlier pending-integration statements below describe their dated snapshots, not current status. V2 supersedes conflicting v1 definitions; these local v2 edits are uncommitted.

## 2026-11-18 — inherited evidence imported

Source: the original handoff by Timothy Tran, now archived. The fixed pilot, raw-export audit, persistence/seven-day baseline predictions, and four metric rows were imported. Their full pipeline and metric values were not independently reproduced. Original baseline test scores were already visible.

## 2026-11-18 — three-owner structure migration

Owner/requester: SAS. DELTA/DEVGRU/SAS directories, planning configs, current responsibilities and interface/dependency guidance were added. Canonical manifest/results paths moved; all ten originals were preserved in the archive. Working legacy paths were adapted to separate reproduction outputs; the working notebook has cleared execution state. Static/structural tests are migration evidence only. No data pipeline, notebook cells, features, fitting, scoring, or new model test evaluation was executed.

Status: integrated by PR #2, merge `35bfa71208d0297c72c41f00c104abed9027235b`, at the user’s explicit instruction after agent diff/check review; no independent teammate approval is claimed. See `docs/structure_migration.md`, `context.md`, and Git/PR history for exact scope and checks. No new experimental result exists to record.

## 2026-11-18 — source/local field audit and contract v1 definition freeze

Owner/requester: SAS, explicit “do it” continuation. Read the publisher's data card and pinned source code without executing it; audited all 18,000 pilot stock vectors/counts and the predetermined sequential eligibility rule. Count matches: zero mismatches for `[6:22]`; eligible rows 3,693/1,698/1,747. Exact evidence: `docs/contract_audit.json`; scope/limits: `docs/contract_freeze.md`. No forecast features, predictions or metric scores were generated.

Frozen `configs/contract.yaml` v1.0.0 and hash lock define primary feature allowlists, CSV/JSON bundle/prediction handoffs, train-only preprocessing, pooled OLS/tree budgets, selection/test gates, metrics/strata and uncertainty rules. Producer/model/evaluator implementations, validation-selected parameters and new model test scoring remain pending. Eight layout/contract tests passed; final static checks/publication are recorded in the freeze evidence/Git history. This is definition/audit evidence, not a model run or achieved research goal.

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

## 2026-11-19 - DELTA V2 implementation and local generation

User-authorized implementation by Codex for DELTA (`Timothytran109`, authenticated). Branch `DELTA/v2-data-pipeline`, base `5dcd128`; local uncommitted, no staging/publication. Raw identity verified and copied; 200-series development and deterministic 1,000-series final inputs generated with 15,200/76,000 observations and all eligible stockout targets retained. All features independently reconstructed. Development persistence/7-day baselines recomputed; no final scoring or learned-model training. Evidence, hashes, coverage and metrics: [run evidence](DELTA_V2_RUN_EVIDENCE.json), [implementation report](DELTA_V2_IMPLEMENTATION_REPORT.md), [handoff](DELTA_DATA_HANDOFF.md).

Producer semantics are operationally verified (24 binary hours, 1=stockout, [6:22]); undocumented closed/missing hours and export lineage remain provisional. Broader contract and validation choices remain unfrozen. No scientific design changed. Seed 245 and unstratified SHA-256 key ranking are explicit authorized technical decisions; training-only coverage is reported, not used to optimize selection. Historical test exposure remains disclosed. Original evidence is unchanged.

## 2026-11-19 - SAS synthetic implementation validation (no research run)

Owner/requester: SAS / Farzaan Dalwai (`farzaandalwai`, authenticated). Codex
implemented the local Decision Tree/development evaluator on
`SAS/local-tree-evaluator` from integrated DELTA base `d2a323e`. No staging,
commit or publication. Scope/evidence: [SAS handoff](SAS_LOCAL_HANDOFF.md).

DELTA's unchanged producer generated a labeled two-series synthetic fixture
(92 train / 30 validation / 30 test observations). SAS fitted/selected paired
trees with an equal 12-candidate development budget per condition, generated
244 train/validation predictions and evaluated only 30 validation keys per
condition in the CLI comparison. No test predictions/scoring; numeric fixture
scores are not forecasting findings. All 56 tests and the setup checker passed.

Real development/final r2 bundles are absent here. No real learned-model run,
shared validation freeze, final comparison, uncertainty interval or environmental
benefit is claimed. Optional forest remains deferred until the core comparison
works. Real-run results will be recorded separately after artifact acceptance.

## 2026-11-19 - SAS real development validation with paired intervals

SAS authorization: [integration request](prompts/2026-11-19-sas-integration.md).
Input: exact DELTA `v2-development-200-r2`, trusted manifest SHA-256
`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`;
discovered in the shared Drive folder, all ten files verified. No substitution.
Training 9,200 / validation 3,000; 113 validation stores. Run
`sas-tree-dev-200-bootstrap-r1`; comparison `sas-dev-validation-bootstrap-r1`.
Both conditions selected depth 5/minimum leaf 5 using equal 12-candidate budgets,
train-only fitting and validation MAE; no clipping/refitting on validation.

Validation MAE sales-only 0.348255 / aware 0.352070. Difference aware minus sales
+0.003814, 95% paired store-cluster percentile interval [-0.003332, +0.013629],
seed 245/2,000 replicates. These are developmental estimates conditional on
validation selection, not a final claim; no clear improvement established.
No test predictions/scoring, no teammates' model implementation, no merge.
Synthetic bootstrap smoke runs are separately labeled and are not research
findings. All 61 tests passed; exact provenance/limits in
[SAS integration](SAS_INTEGRATION.md) and [evidence](SAS_INTEGRATION_EVIDENCE.json).

## 2026-11-20 — harmonized DEVELOPMENT evaluation of original predictions

No model rerun/retuning. Exact development r2 manifest
`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`;
PR6 artifact commit `044fac1a9ed0fae52179df25946a5a994f2826b5`; original SAS outputs
checked against previously committed evidence and copied unchanged for sharing.
Three supporting PR6 inventory inconsistencies remain flagged; all four original
prediction checksums, keys, targets/splits, finiteness and paired coverage passed.

Run `artifacts/SAS/development/harmonized-200-series-20261120-r3` evaluates original
Linear/Ridge/Tree predictions on 3,000 identical validation rows, 200 series,
113 stores, plus newly materialized validation-only persistence/7-day references.
Whole-store paired percentile intervals, 95%, 2,000 replicates, seed 245, pooled
row weighting, aware-minus-sales MAE. Original DEVGRU series-bootstrap results
were reproduced and preserved separately. Only run IDs changed in memory.

Linear/Ridge aware MAEs 0.334190/0.334119 versus sales 0.334257/0.334256; Tree
aware 0.352070 versus sales 0.348255. All three harmonized paired intervals include
zero. Baseline MAEs persistence 0.417757 / 7-day mean 0.337380. No clear
stockout-feature benefit established; no final, causal or sustainability finding.
Retrospective subgroups: 1,698 fully-stocked / 1,302 stockout rows. Detailed
metrics, limitations, source hashes and PNG/SVG figures are in the versioned run
and [handoff](SAS_DEVELOPMENT_COMPARISON.md). Final scoring remains blocked;
no final input/outcomes were inspected, no PR merged.

## 2026-11-20 — SAS Random Forest, DEVELOPMENT only

Requester: SAS / Farzaan Dalwai. [Request](prompts/2026-11-20-sas-random-forest.md).
Implemented the approved optional Random Forest on `SAS/random-forest-development`
with the tree's grid, seed and train-only/validation-MAE protocol. Real run
`sas-forest-dev-200-r1` on the exact r2 development bundle: validation MAE
sales-only 0.335969 / aware 0.336504; aware minus sales +0.000535, 95% store
interval [-0.003533, +0.005357], so no clear stockout-feature benefit. No test
scoring, no final input, no team-frozen setting. Details: [SAS Random Forest](SAS_RANDOM_FOREST.md).
