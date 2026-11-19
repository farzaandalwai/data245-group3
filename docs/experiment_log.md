# Experiment and integration log

## 2026-11-18 — inherited evidence imported

Source: the original handoff by Timothy Tran, now archived. The fixed pilot, raw-export audit, persistence/seven-day baseline predictions, and four metric rows were imported. Their full pipeline and metric values were not independently reproduced. Original baseline test scores were already visible.

## 2026-11-18 — three-owner structure migration

Owner/requester: SAS. DELTA/DEVGRU/SAS directories, planning configs, current responsibilities and interface/dependency guidance were added. Canonical manifest/results paths moved; all ten originals were preserved in the archive. Working legacy paths were adapted to separate reproduction outputs; the working notebook has cleared execution state. Static/structural tests are migration evidence only. No data pipeline, notebook cells, features, fitting, scoring, or new model test evaluation was executed.

Status: integrated by PR #2, merge `35bfa71208d0297c72c41f00c104abed9027235b`, at the user’s explicit instruction after agent diff/check review; no independent teammate approval is claimed. See `docs/structure_migration.md`, `context.md`, and Git/PR history for exact scope and checks. No new experimental result exists to record.

## 2026-11-18 — source/local field audit and contract v1 definition freeze

Owner/requester: SAS, explicit “do it” continuation. Read the publisher's data card and pinned source code without executing it; audited all 18,000 pilot stock vectors/counts and the predetermined sequential eligibility rule. Count matches: zero mismatches for `[6:22]`; eligible rows 3,693/1,698/1,747. Exact evidence: `docs/contract_audit.json`; scope/limits: `docs/contract_freeze.md`. No forecast features, predictions or metric scores were generated.

Frozen `configs/contract.yaml` v1.0.0 and hash lock define primary feature allowlists, CSV/JSON bundle/prediction handoffs, train-only preprocessing, pooled OLS/tree budgets, selection/test gates, metrics/strata and uncertainty rules. Producer/model/evaluator implementations, validation-selected parameters and new model test scoring remain pending. Eight layout/contract tests passed; final static checks/publication are recorded in the freeze evidence/Git history. This is definition/audit evidence, not a model run or achieved research goal.

## Future run entries

Record owner, date, branch/PR/revision, contract/bundle/input hashes, target/filter counts, feature set/model/window, train/validation selection and tuning, prediction/run paths, environment, metrics with evidence, checks, deviations, AI assistance/human validation, and integration/test-freeze status. Do not append unexecuted plans as completed runs. Shared log edits must preserve other owners' valid entries.
