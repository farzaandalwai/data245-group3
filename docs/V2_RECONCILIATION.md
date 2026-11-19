# V2 semantic reconciliation - 2026-11-19

Status: reconciled working-tree definitions; checks passed, pending human review and Git ancestry integration. Actual start: local `main` at `35bfa71`, two commits behind fetched `1939586`, V2 uncommitted, no MERGE_HEAD/unmerged index entries. No commit/merge/staging/push performed. Initial 35 changed/new files were backed up outside the checkout with a SHA-256 inventory before editing.

## Decisions and preserved remote work

`c10fd99` introduced the V1 audit/contract/lock/tests and metadata registration; `1939586` merged PR #3 with the identical tree. Their useful safe parser, endpoint tests, publisher references, provenance, exact source evidence, shared-key/feature-pairing and validation/test safeguards are retained. Exact contract/audit/four-entry lock, original script/tests/freeze/prompt and contribution/AI/provenance documents are isolated under [historical evidence](history/contract_v1/README.md), with source commit/hash manifest and byte-preserving Git attributes.

V1 day-29/28-day-history, zero-target-stockout eligibility, original counts, ID predictors, old features and course-fit-disabled extensions do not govern V2. Active metadata registers 14-day/day-15, all otherwise eligible targets, evaluation-only target-day subgroups, 200 development/1,000 pending final series, exact approved features, core linear/tree and approved Ridge/forest extensions. Target/splits/ownership/baselines/metrics remain unchanged. Historical lock entries are resolved to snapshot contract/audit and canonical root pilot/manifest without rewriting hashes; there is no active V2 freeze lock.

Technical schema/serialization, quality rules, final sampling algorithm/coverage, stockout semantics for V2 producer, preprocessing, clipping, grids/settings and uncertainty remain DRAFT/PENDING. No dataset, shared feature producer, model/evaluator experiment or final results were generated.

## Files changed by this reconciliation

- `configs/contract.yaml` (new), `pyproject.toml`: retain remote registration mechanism for active V2 metadata aggregator, with false freeze/implementation/test gates.
- `configs/{dataset,experiments}.yaml`: explicit historical evidence and active metadata references; V2 settings preserved.
- `scripts/audit_contract.py` (new locally): retained safe parser/endpoints and a history-only day-15 static guard; no V1 eligibility or producer.
- `tests/test_shared_contract.py` (new locally): active V2 invariants, metadata consistency, paired features/keys, scopes/statuses, calendar, validation/test safeguards, parser/endpoints and duplicate YAML-key detection.
- `tests/test_historical_contract_v1.py` (new): separate in-memory V1 audit reproduction, original eligibility/feature/gate checks, four-entry lock and exact snapshot hashes.
- `docs/history/contract_v1/` (new): ten exact remote source files, source hash manifest and historical navigation README; no original archive/evidence files edited.
- `.gitattributes`: disable text conversion for exact snapshot bytes.
- `scripts/verify_setup.py`: exempt relocated historical Markdown from current-layout link resolution, like existing historical handoffs; snapshot hashes and current navigation checked separately.
- `AGENTS.md`, `context.md`, `README.md`, `configs/README.md`, `docs/{experiment_protocol,interfaces,team_responsibilities,methodology,contract_freeze,provenance,REPOSITORY_CHANGE_AUDIT}.md`, `tests/README.md`: distinguish completed local semantic reconciliation from pending technical details and Git ancestry integration; preserve historical-source credit.
- `src/{data_preprocessing_DELTA,features_DELTA,evaluation_SAS}/README.md` and five existing model/baseline READMEs: update stale reconciliation dependency to draft-interface verification and Git integration. No ML source changed.
- `docs/{experiment_log,contributions,ai_assistance}.md`, saved reconciliation prompt and this record: task/decision/evidence handoff, no fabricated contribution credit.

The earlier 35-file V2 edits remain present; [the original alignment audit](REPOSITORY_CHANGE_AUDIT.md) is a dated snapshot, not the inventory for this expanded validation task.

## Validation

Passed `python -B -m unittest discover -s tests -v`: **18 tests** (10 active V2, 5 historical V1, 3 existing layout). Historical audit reproduced in memory exactly; all four original lock hashes and all ten copied source-file hashes match.

Passed `python -B scripts/verify_setup.py`: ten original archive/canonical hashes; 11 Python files parsed; notebook JSON/31 cells/13 code cells parsed without execution; pilot/prediction schemas/keys/calendars/splits; 57 current Markdown files/local paths and ignore rules. Copied historical Markdown uses original source-layout links and is deliberately excluded from current-layout link resolution.

Passed YAML parsing with duplicate-key rejection and consistency tests, and `git -c core.whitespace=cr-at-eol diff --check`. Python 3.12.10, PyYAML 6.0.3 from the existing temporary dependency directory outside checkout. No requirements or dependency locks changed. No preprocessing, fitting, notebook execution, feature table generation or score recomputation.

Original ML source, data, notebook and inherited-result bytes are unchanged; new Python code is limited to static helpers/tests and the existing checker's historical link exemption. No original archive or historical evidence edited. Final path-boundary review found 37 modified tracked files and 22 new files cumulatively (including the prior V2 task); only documentation/configuration, Git attributes/registration and static validation files changed. Final authenticated readback was `Timothytran109`, with no open issues or PRs; fetched remote main remained `1939586`. Static assertions do not claim that real feature values, model outputs or runtime compatibility have been verified.

## Git handoff

Not ready for a normal push to main: V2 remains uncommitted and remote ancestry is not integrated. Preserve/review on an authorized task branch, commit the reconciled changes, integrate current remote ancestry without losing valid source/contribution updates, rerun checks and review the resulting diff before publication. No force-push, reset or merge commit was performed. Future merge must not restore root V1 active authority or duplicate unscoped V1 tests; use this reconciled tree and preserved snapshot mapping.
