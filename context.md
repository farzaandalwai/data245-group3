# Shared project context

Updated: **2026-11-18, America/Los_Angeles**. This is orientation, not live shared memory or a lock. Fetch and inspect Git/PR state before tasks, checkpoints and final push. The fetched `origin/main` version is integrated shared state; a local copy alone does not prove integration.

## This is us — active owner mapping

- **DELTA = Timothy Tran (Tim)**; supplied GitHub `timothytran109` (canonical `Timothytran109`). Own data/preparation, the shared feature bundle, and baselines.
- **DEVGRU = Shoury / Shourya**, named Shoury Ambarish Parab in the inherited handoff. Own linear regression and course-approved ridge.
- **SAS = Farzaan Dalwai (you; also written Farzan in the request)**; authenticated GitHub `farzaandalwai`. Own decision tree, optional course-approved random forest, shared evaluation, formal leakage audit, and integration.

Use codenames for active folders/branches. Preserve real imported authorship. The user explicitly confirmed these three active contributors; Mansi/Denisha in the source are historical assignments only. `shoddy16` has previously verified write access, but its real-name/codename mapping remains unconfirmed; do not infer it from account count. Assignment is not personal agreement, validation or completion evidence.

## Integrated layout and current contract handoff

The user explicitly said “do it” to merging PR #2 and freezing the contract. PR #2 is merged as `35bfa71208d0297c72c41f00c104abed9027235b`: codename layout and automatic `AGENTS.md` startup are integrated. The earlier PR #1 was superseded with its changes retained. No separate teammate approval/human technical review is claimed.

Contract task owner: SAS; branch `SAS/freeze-shared-contract`, based on merged layout main. Scope: source/local stockout-field and eligibility audit, explicit shared feature/prediction/preprocessing/tuning/evaluation definitions, hash lock and focused checks. No feature producer, model, evaluator, fixture, full raw pipeline, notebook execution or new score is part of this task. The contract work is branch work until its PR merges; confirm the fetched main contains `configs/contract.yaml` v1.0.0 and its matching lock before treating it as integrated. When this v1 context is read from fetched `origin/main`, that definition is the current integrated contract. Git/PR history records the exact integration commit without a self-referential hash here.

Definition status in this snapshot: **v1.0.0 frozen for implementation**, not implementation verified. `docs/interfaces.md` is the readable guide; `configs/contract.yaml` is canonical and `configs/contract.lock.json` locks definition/input/audit bytes. Changes require a versioned amendment and coordinated dependent runs. Current scope/checks are in `docs/contract_freeze.md` and exact authorization in `docs/prompts/2026-11-18-merge-and-freeze.md`.

## Fixed design and newly verified eligibility

Predict next-day recorded normalized `sale_amount` for fixed `(store_id, product_id, dt)` keys. Preserve seed-245 manifest, 200 series, 18,000 rows, dates 2024-03-28 through 2024-06-25. Original splits: train days 1–60 (12,000), validation 61–75 (3,000), test 76–90 (3,000). Primary history 14; optional 7/28 retains the same day-29 eligible target keys.

Pinned publisher code and all 18,000 pilot rows confirm 24 binary stock entries, 1=out of stock, and business interval `[06:00,22:00)` / array slice `[6:22]`, with zero count mismatches. Sequentially require day>=29, then zero target-day business-hour stockouts: eligible counts are **train 3,693, validation 1,698, test 1,747**. All 113 pilot stores contribute in each split; eligible series counts are 198/198/199. Keep the full 200-series manifest; no-target series metrics are not evaluable, not zero. Evidence is `docs/contract_audit.json`; this is a field/count audit, not raw-export or forecasting performance reproduction.

Primary ordered common predictors: store_id, product_id, weekday, sales_lag_1, sales_lag_7, sales_mean_14, sales_std_14 (population std). Added aware predictors: stockout_hours_lag_1, stockout_hours_mean_14, stockout_day_fraction_14, stockout_free_lag_1. Use the exact allowlists. Build history on the full ordered same-series source through t-1, including stockout dates, before selecting eligible targets. Only weekday/known identity keys use target-date information; target availability stays separate metadata. No raw target/stock/weather/promotion/baseline/split columns enter predictors.

Contract v1 fixes CSV/JSON bundle/prediction schemas, train-only categorical/numeric preprocessing, pooled OLS/tree, equal per-condition tuning budgets (OLS 1; tree 12), validation selection/ties, consistent nonnegative clipping, metrics/strata and paired store bootstrap rules. Ridge/random forest are disabled until course fit and a versioned amendment. **Definition freeze does not freeze actual selected parameters:** new model test evaluation still requires a pre-test record binding both conditions' validation choices and code/contract/bundle hashes.

## What exists and what remains pending

- Ten originals are byte-identical under `archive/original_pilot/`. Source authorship/IDs/times/bytes/hashes and original/current paths are in `docs/provenance.md` and import/migration manifests.
- Canonical unchanged working input: `data/processed/pilot_200_series.csv`; manifest/exclusions: `data/manifests/`; inherited results: `results/baselines_DELTA/inherited/`.
- Legacy path-adapted scripts/notebook exist in `src/data_preprocessing_DELTA/` and `notebooks/DELTA_data/`; raw destination is `data/raw/freshretail.csv` and reproduction outputs are isolated. They have not been run. Working notebook outputs were cleared, while originals remain archived.
- Raw CSV remains absent/unhashed (323,577,557 bytes in prior Drive metadata); original proposal/intermediate report and professor starter code remain unavailable as separate imports. Full raw-export audit claims and baseline metrics remain inherited/unreproduced.
- The read-only field/eligibility audit and frozen definitions now exist. A real feature bundle, feature-value/timing producer checks, fitted preprocessing/models, matched baseline rescoring, evaluator, full experiment-wide leakage audit, uncertainty and final findings do not exist yet.
- The all-90-day completeness selection was retrospective rather than the proposal's training-only intention. Original baseline test scores have already been seen. Retrospective stockout-free target eligibility changes the evaluated population. Preserve all three limitations; recorded sales are not latent demand and sustainability benefits remain unmeasured.

## Owner status and parallel next tasks

**DELTA:** inherited preparation/pilot/baselines exist. Next bounded implementation: produce v1 `manifest.json`, `targets.csv`, `features_14.csv`, `eligibility.csv`, and `feature_provenance_14.csv` from the fixed pilot; independently verify actual values/timing/matched keys and hashes. Future matched baselines use the same eligible keys and separate results. Do not resample or relabel the legacy runner as the new producer.

**DEVGRU:** implement OLS adapter/validation code against the frozen schemas. Ridge adapter exploration can be scoped separately but actual ridge runs require course-fit amendment. All implementation/runs remain pending.

**SAS:** implement tree/evaluator adapters and their value/timing/key/metric tests against v1; full audit/integration is pending. Optional forest is disabled. Final comparisons need accepted predictions, and new model test evaluation needs the validation-freeze record.

All three can code, commit and push owned branches in parallel now. Use clearly labeled deterministic schema fixtures for development if needed; none were generated by this contract task and fixture outcomes are not research evidence. Real paired runs need DELTA's same verified bundle. Components exchange standardized files/metadata rather than call a teammate's notebook. Each next implementation still needs its own bounded assignment; do not start it automatically from this context.

## Collaboration, checks, and remaining limits

Use separate clones and `<codename>/<task>` branches; concurrent sessions need separate worktrees. Root `AGENTS.md` loads automatically, so a short task/orientation/resume request is enough. Coordinate shared configs/dependencies/protocol changes. Update owner sections/context and applicable contribution/AI records each substantive commit; preserve both valid updates in conflicts and integrate reviewed PRs one at a time. Dependent sessions fetch/reread after merges.

Contract tests passed: eight total layout/contract tests, including hour endpoints/parser safety, day-29/history-first filtering, recorded audit reproduction, exact locks, paired allowlists and optional/test gates. The final setup/static/path check is recorded in `docs/contract_freeze.md`. No model training/scoring or full pipeline was run; package installation, producer runtime, cross-machine workflow and the optional two-human doc-PR exercise remain unverified.

Private repo: [farzaandalwai/data245-group3](https://github.com/farzaandalwai/data245-group3). At last verified access readback both `shoddy16` and `Timothytran109` had accepted write without admin access; recheck live state when needed. Branch protection was rejected by the current plan (403); review/one approval/no force push remain conventions. Integration here is user-authorized agent review/merge, not fabricated independent human approval. Individual reports/disclosures and exact Canvas deadline/presentation checks remain each person's responsibility; no report was authored here.
