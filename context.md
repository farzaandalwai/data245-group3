# Shared project context

## 2026-11-24 submission demo sharing checkpoint

Authenticated requester: DELTA / Timothytran109. The user explicitly requests
commit/push of the submission package for a teammate's presentation. Isolated
branch `DELTA/share-submission-demo` starts from fetched main `dc5c10c`; the
original checkout is unchanged. Main already contains the report, slides,
notebook and script. This task adds the previously ignored exact 3,810-byte
joblib, a narrow ignore exception and byte-preservation attributes, pinned demo
dependencies and [fresh-computer setup](submission_local/START_HERE.md).

IMPLEMENTED / VERIFIED packaging: model/script hashes match their original
verified bytes; notebook execution passes in the isolated checkout without an
external bundle and with all fitting prohibited; embedded CLI passes; dependency
dry-run resolves against the existing matching environment. No fresh environment
installation or another operating system was tested during packaging. No new
training, tuning, final evaluation or changes to scientific results/configs.
The package retains the aggregate-MAE versus missing row-level-reference caveat.
Notebook caches, raw data, environments and credentials are excluded. Publication
of the task branch and draft PR is authorized; main integration/human review
remain pending. Request: [saved authorization](docs/prompts/2026-11-24-share-submission-demo.md).

Updated **2026-11-20, America/Los_Angeles**. Orientation/handoff only, not live shared memory or a lock. Fetch and compare current Git/issue/PR state at startup.

## 2026-11-24 DELTA/DEVGRU publication checkpoint

Authenticated requester/account: DELTA / `Timothytran109`; explicit authorization
also covers DEVGRU. Branch `DELTA/delta-devgru-readiness` is based on fetched main
`4dffb0d`. The user now authorizes the reviewed source/test/documentation commit,
feature-branch push and PR targeting main, with no merge or final scoring. This
supersedes the earlier task-specific no-publication restriction. Integration and
independent human review remain pending.

Implemented and locally verified: trusted/past-only development baseline exports;
SAS-compatible DEVGRU run envelopes; numeric fitted-state exports for future
runs; approved development store intervals through the unchanged SAS library;
transactional writes and explicit LF/CRLF evidence identities. Owned tests: 37
passed. Saved original development metrics reproduce without fitting; final
inputs are compatible, but all three V2 freeze gates remain false. Missing
original fitted models/exact execution lineage are not reconstructed.

PR #9 (`SAS/rf-comparison-r4`, inspected `ec6abf1`) remains OPEN. Implementation
paths do not overlap its source changes; the three required shared ledgers now
have separate dated entries and require semantic reconciliation at integration.
SAS's final bootstrap/V1-lock defects and joint freeze remain blockers. No real
model was retrained and no final 1,000-series prediction/scoring was performed.
See [tracked readiness](docs/DELTA_DEVGRU_READINESS.md) and the
[publication authorization](docs/prompts/2026-11-24-delta-devgru-publication.txt).
Earlier dated session snapshots below remain historical context.

## Active identity and ownership

- **DELTA - Timothy Tran (Tim)**; confirmed GitHub `Timothytran109`. Central dataset/data contract, raw validation, preparation, pilot/final sampling, splits, shared sales/stockout features, manifests, persistence/7-day baselines and provenance/preprocessing validation.
- **DEVGRU - Shoury**, named Shoury Ambarish Parab in the historical handoff. Linear Regression and approved Ridge extension, model training/tuning and standardized predictions.
- **SAS - Farzaan Dalwai**; confirmed GitHub `farzaandalwai`. Decision Tree, optional approved Random Forest, shared evaluation/comparison, leakage/integration checks, figures and summaries.

All three share scientific decisions, review, integration and final submissions. Folder ownership is not completed contribution credit. Historical five-member assignments retain attribution; Mansi/Denisha are not active owners. `shoddy16` has an unconfirmed full-name mapping; do not infer identity from Git settings or account count.

## Current implementation and Git state

Live GitHub readback 2026-11-23: PRs #2–#8 are MERGED; `main` is `4dffb0d`. On
2026-11-23 Timothytran109 merged SAS PR #8 (Random Forest), SAS PR #7 (development
comparison) and DEVGRU PR #6 (original artifacts, including DEVGRU's checksum
correction `1f4e6a4`). The repository is public. No PR is merged by SAS tasks.

Current requester: SAS / Farzaan Dalwai (`farzaandalwai`). Branch
`SAS/rf-comparison-r4` from `4dffb0d`, per the
[SAS step-1 request](docs/prompts/2026-11-23-sas-step1.md): re-pin the merged PR #6
package, share the Random Forest run, add relative MAE improvement and publish a
separate r4 comparison. No final scoring, retraining or teammate edits. Evidence and
commands: [SAS development comparison](docs/SAS_DEVELOPMENT_COMPARISON.md).

## Approved science and source of truth

Goal: test incremental value of historical stockouts for next-day normalized recorded `sale_amount`, not latent-demand estimation or causal inference. Approved v2 uses all eligible target dates including stockouts; secondary test subgroups are fully stocked/stockout target dates, labeled after prediction. Target-day stockouts are never predictors.

Development: 200 complete series, preserving inherited sample. Final: 1,000 complete series generated by seeded SHA-256 key ranking (245), no outcome-derived strata or validation/test outcome selection. Primary maximum history 14 days, candidate targets day 15; splits remain days 1 to 60/61 to 75/76 to 90. Verified final counts are 46,000/15,000/15,000; development counts are 9,200/3,000/3,000.

Core Linear Regression/Decision Tree; approved Ridge/optional Random Forest; required persistence/7-day baselines. MAE primary, RMSE and mean(prediction-actual) bias secondary. Conditions share keys/targets/common features. DELTA owns the sole shared producer. Exact feature concepts and all scientific rules live in [experiment_protocol.md](docs/experiment_protocol.md), not this summary.

Read in precedence order: [protocol](docs/experiment_protocol.md), [interfaces](docs/interfaces.md), [responsibilities](docs/team_responsibilities.md), `configs/*.yaml`, this context, [experiment log](docs/experiment_log.md), workstream READMEs; archive is historical only. [AGENTS.md](AGENTS.md) governs workflow; Copilot points to it. Flag contradictions instead of silently choosing another methodology.

## Existing versus pending evidence

**HISTORICAL:** ten originals under `archive/original_pilot/`, canonical `data/processed/pilot_200_series.csv` (200 series/18,000 rows), `data/manifests/`, inherited results under `results/baselines_DELTA/inherited/`. Original attribution/hashes: [provenance](docs/provenance.md). Legacy scripts/notebook have adapted paths and separate reproduction destinations; they have not been rerun by this task.

**PRESERVED AND REPRODUCED:** the exact historical v1 source/pilot audit and frozen definitions are isolated under `docs/history/contract_v1/`. Its claims are bounded historical evidence, not v2 producer validation or new model results. The superseded stockout-free filter removed approximately 43.16% of candidates; it is not active eligibility.

**DELTA RECORDED / VERIFIED operationally in its run evidence:** raw export copied with matching SHA-256; 1,459,198 rows validated, 16,213 complete series; immutable development/final/synthetic bundles, feature reconstruction and development baselines. See handoff for exact identities. The raw export/final bundle remain absent here. DELTA’s exact development r2 bundle was found in Drive, downloaded and verified against the trusted manifest/all artifact hashes; it is now available locally and ignored. DELTA's recorded real-data runs were not independently replayed here. Final scoring has not run.

**SAS IMPLEMENTED / SYNTHETIC AND REAL DEVELOPMENT VERIFIED:** paired Decision Tree consumer, shared development metrics/subgroups/series/store summaries, strict key/target/split/provenance checks, versioned local runs and CLI. Real validation on 3,000 paired rows/113 stores completed with 95% paired store-cluster MAE-difference intervals (seed 245, 2,000 replicates). No test predictions/scoring. The local synthetic fixture uses DELTA's unchanged producer. Current evidence and limits: [SAS integration](docs/SAS_INTEGRATION.md); earlier local-only handoff is historical.

**PROVISIONAL:** missing/closed-hour business semantics and exact export lineage/scaling coefficient. The [publisher's documented hourly convention](docs/DELTA_DATA_HANDOFF.md#semantics-and-sampling-limits) reconciles with every local row. Zero annotated stockout defines the retrospective label but does not prove unrestricted availability.

**CURRENT DEVELOPMENT INTEGRATION:** all 16 original SAS files are copied byte-for-byte
under `artifacts/SAS/development/original-200-series-20261119/`; prior manifests and
hashes remain authoritative. Original tree JSONs reproduce all 24,400 saved
train/validation predictions without fitting. PR6's four original prediction
files pass exact key/target/split/finiteness/coverage checks. Its original series
bootstrap summaries reproduce, but three supporting inventory entries disagree
with published bytes; exact Git-blob pins and provenance limits are recorded.
Only run IDs are normalized in memory. All three learned families plus both
validation-only simple baselines now use one evaluator on 3,000 matched rows /
113 stores. New comparison/PNG/SVG figures live under
`artifacts/SAS/development/harmonized-200-series-20261120-r3/`. All paired
whole-store 95% intervals include zero. These are DEVELOPMENT, not final evidence.

**SAS RANDOM FOREST (branch `SAS/random-forest-development`, DEVELOPMENT only):**
the approved optional forest is implemented with the tree's grid/seed and
train-only/validation-MAE protocol (fixed 200 trees, `max_features=1.0`). Real
validation MAE sales-only 0.335969 / aware 0.336504; aware minus sales +0.000535,
store interval [-0.003533, +0.005357] includes zero. Not group-frozen; no test
scoring. See [SAS Random Forest](docs/SAS_RANDOM_FOREST.md). Merged in PR #8; the run is
shared under `artifacts/SAS/development/random-forest-200-series-20261120/` and included in
the r4 comparison `artifacts/SAS/development/harmonized-200-series-20261123-r4/`, which
reproduces every r3 number and adds relative MAE improvement (Linear +0.020%, Ridge
+0.041%, Tree −1.095%, Forest −0.159%; negative = stockout-aware worse).

**PENDING:** PR6 inventory/execution-lineage confirmation, final model/settings
and collective tie-rule agreement, final freeze/entry-point acceptance and final
reports. DEVGRU models are implemented; earlier not-implemented labels are stale.
No clipping is agreed; actual SAS tie rule is first grid candidate, actual Ridge
rule prefers smaller alpha on exact ties. The complexity-based alternative
remains a proposal. Development store bootstrap is approved; applying it in a
final workflow still needs review. Final test scoring is blocked.

**SAS FINAL-EVALUATOR REPAIR (2026-11-24, branch `SAS/final-evaluator-repair`, draft PR):**
new reviewed entry point `scripts/sas_final_evaluation.py` / `src/evaluation_SAS/final.py`
with V2 gates, shared exact-coverage checks, pooled-row store bootstrap, a PROPOSED (not
approved) `configs/final_settings.json`, optional Random Forest and transactional output.
Synthetic tests only; 114 tests pass; preflight and `check` exit 2 (blocked). Legacy
`scripts/final_evaluation.py` (`91fab8d`) is unchanged; the Nov 20 final run cited by
`submission_local/` is unverified (outputs not in Git, gates were closed). See
[SAS final evaluator](docs/SAS_FINAL_EVALUATOR.md).

## Next cross-team dependencies

1. DEVGRU: `1f4e6a4` fixed the malformed `paired_validation_comparison.csv` checksum.
   The inventory entries for `development_report.md` and `run_metadata.json` still differ
   from the published bytes (declared `ef50e380…` / `563c5cbc…`, published `5257f456…` /
   `e3331387…`); please correct or explain. Also confirm base-only source
   revision and unsaved fitted-model limits; do not replace original predictions
   with newly trained outputs. Review the in-memory run-ID mapping and common
   store-bootstrap development comparison.
2. DELTA: accept the exact producer/final bundle and outstanding business/export
   semantics; participate in technical freeze/review. No new final input was
   opened by SAS. Raw/final inputs remain out of Git.
3. SAS: step-1 work (re-pin, shared forest run, r4 comparison with relative MAE) is on
   `SAS/rf-comparison-r4`; next coordinate final settings/tie/validation-freeze and,
   after the freeze, build the final-scoring entry point for DELTA/DEVGRU review.
   `python3 -m scripts.sas_final_preflight` is config-only and exits 2 (blocked).
4. All 95 tests pass on `SAS/rf-comparison-r4` (84 earlier, 7 forest, 4 new integration
   checks). The exact missing ignored synthetic fixture was imported
   after a pinned Drive verification; no teammate tests were changed. Synthetic
   tests and real original-prediction acceptance/evaluation are separate evidence.
   Human review and personal contribution validation remain pending.

Implementation checkout for this handoff is explicitly `/Users/farzu/Desktop/data245-group3` on `SAS/rf-comparison-r4`. The app-attached PR6 review worktree is detached/read-only and retained because the managed archival tool marks it protected; do not implement SAS changes in that review checkout.


## 2026-11-24 verified-final publication handoff

Owner/requester: DELTA / Timothytran109; branch DELTA/verified-final-publication, base47f531f. Explicit user authorization covers scoped commit/push/PR, not merge or bulk upload. Publishes reconciled report/slide sources, original freeze/attestation, byte-identical small evidence for final-1000-attested-20261124T094349Z, storage inventory and two team guides. Main live configs are unchanged/default-closed; enabled execution configs and bulk predictions/per-series remain local. Existing pipeline code is inherited unchanged. No new scoring, training, tuning, metrics or plots. Original November20 claims remain unverified; DEVGRU/SAS approval is lead-attested. Integration requires human PR review and merge; external PDF/PPTX updates and authorized bulk sharing remain outstanding.
