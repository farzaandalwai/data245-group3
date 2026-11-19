# Shared project context

Updated **2026-11-19, America/Los_Angeles**. Orientation/handoff only, not live shared memory or a lock. Fetch and compare current Git/issue/PR state at startup.

## Active identity and ownership

- **DELTA - Timothy Tran (Tim)**; confirmed GitHub `Timothytran109`. Central dataset/data contract, raw validation, preparation, pilot/final sampling, splits, shared sales/stockout features, manifests, persistence/7-day baselines and provenance/preprocessing validation.
- **DEVGRU - Shoury**, named Shoury Ambarish Parab in the historical handoff. Linear Regression and approved Ridge extension, model training/tuning and standardized predictions.
- **SAS - Farzaan Dalwai**; confirmed GitHub `farzaandalwai`. Decision Tree, optional approved Random Forest, shared evaluation/comparison, leakage/integration checks, figures and summaries.

All three share scientific decisions, review, integration and final submissions. Folder ownership is not completed contribution credit. Historical five-member assignments retain attribution; Mansi/Denisha are not active owners. `shoddy16` has an unconfirmed full-name mapping; do not infer identity from Git settings or account count.

## Current bounded reconciliation task and Git state

Owner: DELTA / authenticated GitHub `Timothytran109` (recheck live identity at task startup). Actual inspected state differs from the supplied assumption: local `main` at `35bfa71`, V2 edits still uncommitted, two commits behind fetched `origin/main` at `1939586`, no MERGE_HEAD or unmerged index entries. No new commit, branch, merge, staging or push was performed. The initial 35 changed/new files were backed up outside the repository before reconciliation.

Scope: preserve remote V1 validation/provenance bytes, register active V2 metadata, adapt static tests/helpers and current guidance. Acceptance: V2 scientific invariants pass, V1 audit/lock reproduce separately, originals unchanged, no ML/data generation, and an honest Git handoff. Exact source copies and manifest live under `docs/history/contract_v1/`; active `configs/contract.yaml` is a metadata aggregator with DRAFT technical status, not the old scientific authority or an implemented producer schema.

Semantic reconciliation is complete in the working tree; Git ancestry integration is not. PR #2/layout is merged locally, PR #3/V1 is merged remotely. Preserve remote attribution records (copied exactly in historical evidence) and their valid integration corrections during the later Git merge. See [reconciliation record](docs/V2_RECONCILIATION.md) for files/checks/limitations. New tests/helpers are static validation only, not ML producer/evaluator implementations.

## Approved science and source of truth

Goal: test incremental value of historical stockouts for next-day normalized recorded `sale_amount`, not latent-demand estimation or causal inference. Approved v2 uses all eligible target dates including stockouts; secondary test subgroups are fully stocked/stockout target dates, labeled after prediction. Target-day stockouts are never predictors.

Development: 200 complete series, preserving inherited sample. Final: 1,000 complete series, manifest not generated; fixed reproducible algorithm, proposed seed 245, training-only stockout stratification and no validation/test outcome selection. Primary maximum history 14 days, candidate targets day 15; splits remain days 1 to 60/61 to 75/76 to 90. Final counts 46,000/15,000/15,000 are projections only.

Core Linear Regression/Decision Tree; approved Ridge/optional Random Forest; required persistence/7-day baselines. MAE primary, RMSE and mean(prediction-actual) bias secondary. Conditions share keys/targets/common features. DELTA owns the sole shared producer. Exact feature concepts and all scientific rules live in [experiment_protocol.md](docs/experiment_protocol.md), not this summary.

Read in precedence order: [protocol](docs/experiment_protocol.md), [interfaces](docs/interfaces.md), [responsibilities](docs/team_responsibilities.md), `configs/*.yaml`, this context, [experiment log](docs/experiment_log.md), workstream READMEs; archive is historical only. [AGENTS.md](AGENTS.md) governs workflow; Copilot points to it. Flag contradictions instead of silently choosing another methodology.

## Existing versus pending evidence

**HISTORICAL:** ten originals under `archive/original_pilot/`, canonical `data/processed/pilot_200_series.csv` (200 series/18,000 rows), `data/manifests/`, inherited results under `results/baselines_DELTA/inherited/`. Original attribution/hashes: [provenance](docs/provenance.md). Legacy scripts/notebook have adapted paths and separate reproduction destinations; they have not been rerun by this task.

**PRESERVED AND REPRODUCED:** the exact historical v1 source/pilot audit and frozen definitions are isolated under `docs/history/contract_v1/`. Its claims are bounded historical evidence, not v2 producer validation or new model results. The superseded stockout-free filter removed approximately 43.16% of candidates; it is not active eligibility.

**NOT IMPLEMENTED:** v2 bundle, final 1,000-series sample, model adapters/runs, evaluator, final uncertainty/results and full leakage audit. Raw export remains absent/unhashed; full export lineage remains unverified. Missing regenerated artifacts are expected, not defects.

## Next cross-team dependencies

1. Preserve/review the current working tree on a task branch, then integrate fetched main ancestry in a separately authorized Git operation, resolving overlaps against the reconciled V2 tree. No merge is currently in progress.
2. Jointly finalize the **DRAFT CONTRACT**: stockout-hour semantics/indexing verification for v2, final reproducible sampling/coverage, exact schemas/encodings, quality/missingness handling, preprocessing, prediction policy, model/tuning settings and uncertainty procedure. Science is approved; these are technical details.
3. DELTA implements/validates the centralized shared bundle and matched baselines. DEVGRU/SAS implement owned consumers against the same reviewed contract; agreed labeled fixtures can support development. Real paired runs wait for the same verified bundle.
4. Record validation selections before new test evaluation; final comparisons need accepted prediction files. Prior baseline test scores were seen; reused holdout is not pristine. Preserve retrospective 90-day completeness limitations and unmeasured sustainability claims.

Checks for reconciliation are recorded in [the reconciliation record](docs/V2_RECONCILIATION.md); [the alignment audit](docs/REPOSITORY_CHANGE_AUDIT.md) describes the earlier documentation-only snapshot. No implementation/training/preprocessing or experiment was executed. Environment/package/model compatibility and teammate-machine validation remain pending. Course deadlines/presentation slots and personal reports/disclosures remain each student's responsibility.
