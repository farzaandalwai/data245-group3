# Shared project context

Updated: **2026-11-18, America/Los_Angeles**. This is orientation, not live shared memory or a work lock. Verify code/artifacts, issues/PRs, and Git history after fetching.

## This is us — active owner mapping

The user explicitly confirmed only three active contributors and supplied these codenames:

- **DELTA = Timothy Tran (Tim)**; supplied GitHub account `timothytran109` (canonical case `Timothytran109`). Own data preparation, the shared sales-only/stockout-aware feature bundle, and baselines.
- **DEVGRU = Shoury / Shourya**, named Shoury Ambarish Parab in the historical handoff. Own linear regression and course-approved ridge.
- **SAS = Farzaan Dalwai (you; also written Farzan in the request)**; authenticated GitHub account verified as `farzaandalwai`. Own decision tree, optional course-approved random forest, common evaluation, formal leakage audit, and integration.

Use DELTA/DEVGRU/SAS in active folder/branch/ownership labels. Retain original real-name authorship in imported sources and provenance. `shoddy16` has write access but its real-name/codename mapping remains unconfirmed; do not infer it from the three-account roster. Mansi and Denisha appear only in the historical five-person handoff; they are not active owners in the current user-authorized plan. This plan does not claim each teammate has personally reviewed or completed their future assignment.

## Current bounded task and integration state

Owner/requester: SAS. Branch: `SAS/three-person-layout`, started from current `origin/main` and retaining the automatic-startup doc improvement from PR #1. Scope: adapt the proposed workspace structure to these three owners, archive originals unchanged, relocate working inputs/results and adjust legacy paths, preserve all collaboration records, and document parallel work/dependencies. No experiments are authorized by this migration.

Acceptance: useful owner-specific folders/config metadata, exact codename mapping, original-byte archive and unchanged canonical data/evidence, safe reproduction output paths, passing static/schema/layout checks, and one reviewable migration PR. PR #1 is the known overlapping predecessor; this migration retains its startup improvement and replaces that PR without merging main. This branch's restructuring is **pending human integration into main**; the integrated main snapshot at task start contains only the original bootstrap. Never describe unmerged layout work as already on main.

Migration verification: `python3 scripts/verify_setup.py` passed (ten original hashes, unchanged canonical data/evidence, syntax/JSON, schemas/manifest/calendar/splits, Markdown paths and ignore rules); `python3 -m unittest discover -s tests -v` passed all three path/config/ownership tests. No raw file or generated experiment is present. See `docs/structure_migration.md` for scope and runtime limits.

## Fixed scientific design

Question: do historical stockout features improve next-day recorded normalized `sale_amount` beyond recent sales history? Preserve the seed-245 manifest of 200 series, 18,000 rows, 2024-03-28 through 2024-06-25. Train days 1–60 (12,000 rows), validation 61–75 (3,000), test 76–90 (3,000), before lag/eligibility filtering. Primary history 14 days; planned common 7/14/28 comparison starts targets on day 29. Planned zero-stockout targets require semantics/indexing confirmation first. Predictors use through t-1 except known calendar; target-day availability is eligibility metadata only. Explicit allowlists, matched keys/budgets, train-only preprocessing, validation-only tuning, and a freeze before new model test evaluation remain required. See `docs/experiment_protocol.md`.

The pilot used all-90-day completeness rather than the proposal's training-only selection intention; preserve/disclose that availability-selection limitation. Baseline test scores have already been seen. Recorded sales are not unrestricted latent demand; sustainability benefits remain unmeasured.

## What exists and what is pending

- Ten downloaded originals are byte-identical under `archive/original_pilot/`; source URLs/IDs/times/bytes/hashes, original authorship, and initial/current destinations are in `docs/provenance.md` and `docs/handoff/import_manifest.json`.
- Shared working input: `data/processed/pilot_200_series.csv`; canonical manifest/exclusions: `data/manifests/`; inherited results: `results/baselines_DELTA/inherited/`. These working data/evidence bytes are unchanged.
- Adapted legacy code: `src/data_preprocessing_DELTA/`; working notebook: `notebooks/DELTA_data/`. Raw input is now `data/raw/freshretail.csv`. Reproduction outputs go to separate ignored directories, not canonical inputs/evidence. The working notebook outputs/counters were cleared; originals retain historical outputs. Nothing was rerun.
- The raw CSV remains absent by design (323,577,557 bytes in prior Drive metadata); no raw hash exists. The original proposal/intermediate report and professor starter code remain unavailable as separate imports.
- Raw-export audit counts and baseline scores remain inherited/unreproduced. Structural checks are narrower evidence.
- Configs and component READMEs describe planned work, not implementations. Feature/eligibility producers, model adapters, evaluator, formal leakage audit, and real feature bundle remain pending. Exact allowlists/statistics/stockout semantics must still be frozen; `contract_frozen: false` is intentional.

## Owner status — update your own section

**DELTA:** inherited preparation/pilot/baselines exist. Future task: verify data/stockout semantics with SAS, then produce the shared feature bundle and matched baseline predictions after contract approval. No new implementation/run completed by this migration.

**DEVGRU:** linear/ridge adapters and validation work pending. Can develop against an agreed labeled schema fixture after the interface review; real paired runs require DELTA's verified frozen bundle. Ridge requires course fit.

**SAS:** tree/evaluator/audit work pending. Can develop adapters/key/metric tests against labeled fixtures after the interface review. Final comparisons require accepted predictions; new model test evaluation also requires frozen protocol and validation choices. Random forest stays optional.

## How we avoid waiting unnecessarily

Everyone can implement their owned component, commit/push their own task branch, and open PRs independently after the shared interface review. Use common versioned inputs/outputs rather than calling another owner's notebook. A real scientific dependency remains: model runs need the same verified DELTA feature bundle; final evaluation needs accepted predictions. Fixtures are development tools, never research findings. No fixture was generated by migration. Detailed handoffs are in `docs/interfaces.md` and `docs/team_responsibilities.md`.

Shared configs/protocol/dependency changes require coordination. Each substantive task commit updates this context and applicable contribution/AI records; edit owner sections narrowly and resolve conflicts semantically. Merge one reviewed PR at a time; dependent sessions fetch/reread afterwards. Each human uses a separate clone; concurrent sessions need separate worktrees. Automatic `AGENTS.md` guidance means no repeated starter-prompt pasting is needed; a short task/orientation/resume message is enough.

## Access, limitations, and next action

Private repo: [farzaandalwai/data245-group3](https://github.com/farzaandalwai/data245-group3). At the last verified setup readback both `shoddy16` and `Timothytran109` had accepted write access without admin access. Recheck live state before access claims. GitHub rejected branch protection with a plan-level 403; PR review/one approval/no force pushes are conventions, not enforced rules. No plan/visibility change was made.

First integrate the reviewed layout/startup changes, then freeze the shared feature/eligibility/prediction contract as the next explicit bounded technical task. Verify exact course deadline/presentation slot in Canvas. The optional two-human tiny-doc PR coordination exercise and teammate-machine execution checks have not been performed. Individual reports/disclosures remain each person's responsibility; no report or new model experiment was created here.
