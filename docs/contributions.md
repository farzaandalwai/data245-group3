# Contributions and historical roles

Updated 2026-11-18 (America/Los_Angeles). Task ownership is not proof of completion. This record can support later individual CRediT statements, but final statements require each human's validation and evidence.

## Historical assignments from the original handoff

- **Timothy Tran** — existing preparation, pilot, baseline work; reproduction support. The handoff explicitly states that he completed the pilot preparation/baselines, and source files/outputs are present. Setup imported and structurally checked them; full reproduction remains pending. Supplied GitHub mapping: `timothytran109` (GitHub canonical case `Timothytran109`).
- **Farzaan Dalwai** — experiment protocol, integration, formal leakage audit, evaluation and bias analysis. Those technical experiments/audits remain pending. The authenticated setup account was verified as `farzaandalwai`; the user authorized repository setup under that account.
- **Shoury Ambarish Parab** — planned linear regression and ridge experiments. No implementation or completion evidence imported.
- **Denisha Tank** — planned decision-tree experiments; random forest optional after course-fit confirmation. No implementation or completion evidence imported.
- **Mansi** — planned historical stockout features and optional context-length comparisons. No implementation or completion evidence imported.

`shoddy16` is an explicitly requested collaborator with **unconfirmed full-name mapping**. Do not infer that this account belongs to any named member. Only `shoddy16` and `timothytran109` were invited. No task redistribution was inferred from account count during setup. The user subsequently explicitly confirmed only three active contributors and authorized the revised allocation below; the original five-person assignments remain historical provenance.

## Current user-authorized active allocation

The exact identity map is in `context.md`. Use codenames for current workspace labels: DELTA owns data/shared features/baselines; DEVGRU owns linear/ridge; SAS owns tree/evaluation/audit/integration. The user explicitly requested this three-person split and codename mapping after setup. Mansi and Denisha are not current active owners. This records the requested plan, not personal agreement/completion evidence or additional work credit. Full-name mapping for `shoddy16` is still unconfirmed.

## Evidence-backed contribution log

### Imported work — original execution date not independently established

Human contributor as stated by source: **Timothy Tran**. Scope: raw-export preparation/audit, complete-series pilot selection, chronological split, persistence and seven-day-average baselines, predictions and metrics, handoff script/notebook/documentation.

Evidence: the original script/notebook/downloader, pilot/manifest/exclusions, results, and README under `archive/original_pilot/`; canonical working input/evidence paths are documented in the migration record. Exact per-file sources, timestamps, and hashes are in [provenance](provenance.md). Drive modification times are not presented as execution dates. The supplied handoff attributes this work to Timothy; this setup does not invent his prior tools, AI usage, or validation process. CRediT categories such as data curation/software/validation remain subject to his confirmation.

### 2026-11-18 — repository bootstrap and migration

Human requester/account: **Farzaan Dalwai / verified GitHub `farzaandalwai`**. Human action evidenced here: authorizing the bounded setup and providing the setup document, collaborator names, and source links. Existing Git author settings were used for the import commit; Git author identity alone was not used to resolve account identity.

AI assistance: Codex created the collaboration documentation and read-only import checker, imported original artifacts, converted the handoff README reading copy, performed static/structural checks, and operated GitHub setup under that authorization. It did not perform new model/feature work or author final report prose. Do not attribute AI-generated code/docs as personally implemented or validated by a student merely because their account owns the repository.

Evidence: initial bootstrap diff and Git history, [setup verification](setup_verification.md), [AI assistance log](ai_assistance.md), and saved prompts. Human review/validation of this kit remains pending. Repository/invitation creation is a coordination action and does not complete the academic experimental assignments.

### 2026-11-18 — automatic session-start guidance (integrated through PR #2)

Human requester: Farzaan Dalwai. Request: avoid repeatedly pasting the starter prompt and task boilerplate. AI assistance: Codex verified automatic `AGENTS.md` instruction discovery against official OpenAI documentation and updated `AGENTS.md`, the README, and `starter_prompt.md` so only a short task/orientation/resume request is needed. Existing context/Git/protocol checks remain required. No experimental artifact changed.

Original branch: `farzaandalwai/automatic-session-start`, PR #1. The startup improvement is retained in `SAS/three-person-layout`; its predecessor PR is superseded by the combined migration PR, and those retained changes merged through PR #2 at the user’s explicit instruction; independent human technical validation is still pending. Evidence: the branch diff, saved prompt, and AI log. Validation: existing setup checker and targeted documentation review; exact results recorded in [AI assistance](ai_assistance.md#2026-11-18--automatic-session-start-guidance). Human review is pending; this entry does not credit a student with personal implementation or completed experimental work.

### 2026-11-18 — three-owner codename workspace migration (integrated through PR #2)

Human requester: SAS / Farzaan Dalwai. User authorization: restructure to the proposed layout for three active contributors and use DELTA/DEVGRU/SAS labels with an explicit identity map. AI assistance: Codex archived originals unchanged, moved working manifest/results, adapted working legacy paths and cleared working notebook execution state, added useful component ownership/handoff/config/report guidance, documented independence/dependencies, and updated static/layout checks. Original authorship and source hashes are preserved; source path adaptations are AI-assisted migration work, not new original baseline authorship.

Evidence: `SAS/three-person-layout` branch/PR diff, [migration record](structure_migration.md), migration manifest, exact saved request, and AI log. Verification and human-review status are recorded there. No new feature/model/evaluator/fixture/report was implemented or executed. DELTA/DEVGRU/SAS future task ownership is not credited as completed work.

### 2026-11-18 — contract field audit and definition freeze

Human requester/authorization: SAS / Farzaan Dalwai, “do it” to the proposed merge-and-freeze next steps. Codex assistance: reviewed/merged PR #2; read pinned primary sources; authored the read-only pilot stockout/eligibility audit and focused tests; specified/locked v1 feature/bundle/prediction/preprocessing/tuning/evaluation rules and updated shared docs. This is AI-assisted audit/definition work under user authorization, not a claim that SAS personally implemented a feature producer/model or that teammates independently approved the contract.

Evidence: `scripts/audit_contract.py`, `docs/contract_audit.json`, `configs/contract.yaml`, `configs/contract.lock.json`, `tests/test_shared_contract.py`, [freeze record](contract_freeze.md), and actual `SAS/freeze-shared-contract` PR/Git integration state. All 18,000 local rows passed source/index consistency; eligible counts 3,693/1,698/1,747; eight layout/contract tests passed. No features/models/scoring/report were produced. Future DELTA/DEVGRU/SAS implementations and individual human validation remain separate pending contributions.

## Future log entries

For each substantive task commit record date, human contributor, bounded task, branch/PR, files/evidence, checks actually run, AI assistance, human validation, integration status, and candidate CRediT roles backed by that work. Record merge/integration separately from unmerged branch progress. Never create fake teammate commits or credit someone merely for owning a planned task.
