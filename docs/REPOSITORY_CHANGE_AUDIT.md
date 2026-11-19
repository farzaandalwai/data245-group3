# Repository documentation alignment audit

Historical snapshot of the initial documentation-only task. Current semantic reconciliation and expanded validation status: [V2 reconciliation record](V2_RECONCILIATION.md).

Date: 2026-11-19, America/Los_Angeles. Scope: Markdown documentation, common AI guidance and three YAML metadata files only. Scientific approval is v2.0; technical interfaces remain DRAFT CONTRACT.

## Repository and coordination evidence

- Initial working tree clean; local `main` at `35bfa71`; fetched `origin/main` at `1939586`, two commits ahead. Fetch succeeded at startup and checkpoint.
- Layout/startup PR #2 is merged locally; contract-freeze PR #3 is merged remotely. No automatic merge, branch creation, commit, staging, push or PR performed.
- Authenticated GitHub API identity: `Timothytran109` = DELTA / Timothy Tran. Open issues and PR lists were both empty. The `gh` command was unavailable; read-only authenticated API inspection succeeded.
- Fetched v1 contract/lock/audit/tests were inspected without importing changes. They retain conflicting day-29/stockout-free targets, ID predictors, old feature sets and course-fit gates. Reconcile them in a separate authorized integration/technical-contract task. Preserve their historical audit evidence.
- Historical migration/setup/provenance documents retain original dated evidence. Current context, README and log correct old pending-integration snapshots and link current authority. Archived/handoff/past prompt contents are unchanged.

## Approved methodology summary

Question: whether historical stockouts add predictive value for next-day normalized recorded `sale_amount`, not unobserved demand or causal effects. Primary population includes all otherwise eligible target dates, with stocked/stockout target-date subgroups for retrospective test evaluation only. No target-day stockout predictor is permitted.

Development uses 200 complete series; final uses 1,000 complete series, not yet selected/generated. Preserve historical pilot/evidence. Proposed seed 245 and reproducible selection guidance do not imply an implemented algorithm or guaranteed representativeness. Primary history is 14 days, targets from day 15, chronological days 1-60/61-75/76-90. Final target counts 46,000/15,000/15,000 (76,000 total) are projections conditional on completeness/no further exclusions.

Sales-only uses lags 1/2/3/7/14, prior 7/14 means, weekday and weekend indicator. Stockout-aware adds lag-1 stockout hours, prior 7/14 stockout-hour means and stockout-day proportions. IDs are keys. Conditions/models/baselines share targets/keys/splits. All rolling history excludes the target date.

Required core: Linear Regression/Decision Tree; approved extensions: Ridge/optional Random Forest. Required persistence/7-day-average baselines. MAE primary; RMSE and mean(prediction-actual) bias secondary; relative improvement, subgroup errors, under/overprediction and dependence-aware uncertainty where practical. DELTA supplies centralized data/features/baselines, DEVGRU linear/ridge, SAS tree/forest/shared evaluation. All three share scientific review/integration/submissions.

## Cross-tool guidance

`AGENTS.md` is common operational guidance; new `.github/copilot-instructions.md` points to the same protocol/context/interfaces/ownership. No Claude-specific instructions existed; none were duplicated. `starter_prompt.md` is an optional reusable prompt for any assistant. Scientific hierarchy is protocol, interfaces, responsibilities, YAML metadata, context, experiment log, other READMEs, historical archive. Explicit human task constraints govern workflow.

## Remaining technical work

Approved research decisions are not reopened. Remaining work is technical: reconcile remote v1 definition/lock/tests; verify stockout-hour/index semantics for v2 while retaining the historical audit; establish raw provenance/environment compatibility; implement/document final selection and coverage; finalize column names/types/serialization, quality/missingness, preprocessing, tuning grids/settings, prediction postprocessing and uncertainty method. New sample/features/models/evaluation remain NOT IMPLEMENTED. Real runs require the validated centralized bundle and frozen validation choices. Previously seen test results and retrospective completeness limitations remain disclosed.

## Validation results

- **PASS:** `python -B scripts/verify_setup.py`: all ten original hashes/bytes, unchanged canonical data/evidence, six Python files parsed, notebook JSON/31 cells/13 code cells parsed without execution, pilot keys/manifest/calendar/splits, inherited prediction/metric structure without rescoring, 55 Markdown files/local paths and ignore rules.
- **PASS:** `python -B -m unittest discover -s tests -v`: all three existing local layout/static tests. Initial discovery failed because PyYAML was missing; installed PyYAML 6.0.3 to the temporary directory outside this repository and reran successfully with process-local PYTHONPATH. Python 3.12.10. No requirements/environment files changed.
- **PASS:** all three YAML files parsed with duplicate-key rejection; read-only assertions checked v2 versions, pilot/final sizes and proposed seed, day-15/14-day timing, split boundaries/projected counts, all-eligible population, evaluation-only target stockouts, feature names, excluded IDs, model scopes, metric/bias definition and false freeze flag.
- **PASS:** `git -c core.whitespace=cr-at-eol diff --check`.
- **PASS:** changed/untracked path inspection: 32 modified plus 3 new files, exactly matching the inventory below; only Markdown and the three intended YAML files. No source code, notebook content, datasets, historical archives/handoff/old prompts or generated results modified. All 10 archived originals/canonical evidence hashes verified by the existing checker. Saved request is byte-identical (SHA-256 `c0d564360bad23fdd872f943ac51a523f7b1a207029ef76305f91d96b2f7db2b`).
- **PASS, manual consistency review:** active primary-cohort/history/features/samples/model approvals, bias, chronology, ownership, test exposure and cross-tool instructions align. Superseded statements remain only in clearly dated historical records or explicit supersession discussions. No Claude-specific guidance was present.
- **Unavailable here:** fetched main's v1 contract tests/files are absent from the local checkout and were not run or claimed to validate v2. Full environment/model compatibility remains pending. No preprocessing, training, notebook execution, feature generation or experimental scoring ran.

Git diff summary: **32 tracked files changed, 325 insertions(+), 214 deletions(-)**; three untracked additions are Copilot guidance, this audit and the exact saved request. Git diff statistics exclude these untracked file contents. No deletions, renames, staged files, commits, local branch creation/switches or remote publication. Fetch updated remote-tracking information only. Only owner README files changed beneath source/notebook/result/data directories.

## Changed files and purpose

The inventory below includes every modified/new file. Existing accurate guidance and historical records are preserved.

| File | Reason |
| --- | --- |
| `AGENTS.md` | Common operational guidance, precedence/status rules and explicit current-task Git constraint |
| `README.md` | Current design/status/navigation; correct integrated layout and disclose remote v1 dependency |
| `context.md` | Reliable handoff with identity, scope/acceptance, approved summary and technical dependencies |
| `starter_prompt.md` | Concise reusable startup prompt for all assistants |
| `.github/copilot-instructions.md` (new) | Pointer to common guidance, no separate methodology |
| `configs/README.md` | Explain metadata-only fields, draft/approved separation and v1 reconciliation |
| `configs/dataset.yaml` | Target, development/final sample strategy, selection recommendations and pending verification |
| `configs/experiments.yaml` | All-eligible population, features/history/splits, projections, metrics and honest freeze flag |
| `configs/models.yaml` | Core/extension/baseline ownership, pending implementation/settings and draft output columns |
| `docs/experiment_protocol.md` | Authoritative approved v2 scientific methodology and hierarchy |
| `docs/interfaces.md` | Minimum shared observation/feature/prediction/evaluation requirements with draft details |
| `docs/team_responsibilities.md` | Agreed three-member responsibilities and centralized pipeline dependencies |
| `docs/methodology.md` | Short navigation entry point to authority and status |
| `docs/experiment_log.md` | Dated/versioned group decision and current integration correction |
| `docs/contributions.md` | Evidence-backed local documentation contribution/AI distinction and agreement status |
| `docs/ai_assistance.md` | Exact task disclosure, checks/limits and historical integration clarification |
| `docs/prompts/2026-11-19-methodology-alignment.md` (new) | Exact supplied substantive request, byte-identical |
| `docs/REPOSITORY_CHANGE_AUDIT.md` (new) | Complete handoff, changed-file inventory, validation and limits |
| `data/README.md` | Separate historical development manifest from final sampling; current population/semantic status |
| `data/manifests/README.md` | Pending separate final manifest and reproducible selection guidance |
| `data/processed/README.md` | Separate development/final bundles, candidate timing and draft status |
| `src/data_preprocessing_DELTA/README.md` | Central producer/final sampling responsibilities and implementation dependency |
| `src/features_DELTA/README.md` | New sample/history/population and shared feature contract guidance |
| `src/models/baselines_DELTA/README.md` | Required matched baselines and separate historical/noncore ideas |
| `src/models/linear_regression_DEVGRU/README.md` | Remove automatic ID predictors and unfrozen postprocessing; shared v2 requirements |
| `src/models/ridge_regression_DEVGRU/README.md` | Approved extension and paired contract; remove obsolete course-fit gate |
| `src/models/decision_tree_SAS/README.md` | Shared v2 population/bundle and contract dependency |
| `src/models/random_forest_SAS/README.md` | Approved optional extension; remove obsolete course-fit gate |
| `src/evaluation_SAS/README.md` | Retrospective target-date subgroups, primary population and draft uncertainty |
| `notebooks/README.md` | Common protocol and development/final version guidance |
| `notebooks/DEVGRU_linear_models/README.md` | Approved Ridge extension wording |
| `results/README.md` | Distinguish historical/development/final evidence and unimplemented final results |
| `results/predictions/README.md` | Experiment/sample identity and draft exchange contract |
| `results/ridge_regression_DEVGRU/README.md` | Approved extension label |
| `results/random_forest_SAS/README.md` | Approved optional extension label |

## Final status

The local documentation/metadata describe one approved scientific design. Full implementation readiness is not claimed: interfaces remain draft and fetched main's conflicting v1 contract/lock/tests require reconciliation. No new experiment or improvement is claimed. Working branch remains `main`; no PR exists for these edits.

## Subsequent reconciliation

The inventory/checks above describe the earlier documentation-only task, not the cumulative tree. See [the V2 reconciliation record](V2_RECONCILIATION.md) for newly authorized static test/helper changes, preserved V1 evidence, current validation and actual Git state.
