# Shared project context

Updated: **2026-11-18, America/Los_Angeles**. Keep this concise current state; use files, Git history, issues/PRs, and verification evidence for proof. This is not live shared memory and cannot establish whether other sessions are idle.

## Objective and fixed decisions

Test whether historical stockout features improve next-day recorded normalized `sale_amount` beyond recent sales history with matched models/rows/budgets. Fixed input: the inherited seed-245 manifest of 200 series, 18,000 rows, 2024-03-28 through 2024-06-25. Train days 1–60, validation 61–75, test 76–90. Primary history is 14 days; planned common 7/14/28 comparison begins targets on day 29. Planned targets have zero 06:00–22:00 stockout hours only after semantics/indexing verification. All predictors use through `t-1` except known target-day calendar. Retain stockout history, use a predictor allowlist, fit preprocessing on train, tune on validation, and freeze before new test evaluation. Full [protocol](docs/experiment_protocol.md) is authoritative.

## Setup task and integration state

- Owner/requester: Farzaan Dalwai; authenticated GitHub account verified as `farzaandalwai`.
- Branch: `main`, authorized initial bootstrap exception. This snapshot contains setup/imports only. No experimental task branch, model work, or model result is integrated. Subsequent contributions require distinct task branches and PRs.
- Affected files: root collaboration documents, `docs/`, `data/README.md`, inherited `data/processed/`, `data_prep_pipeline/`, inherited `results/`, `.gitignore`/`.gitattributes`, requirements, PR template, and read-only setup checker.
- Dependencies: supplied setup prompt and accessible Drive artifacts; no raw-data download required. Acceptance: private repository, exactly the two requested write invitations, original-byte imports, all requested collaboration files, static/structural checks, safe initial commit/push and remote readback. Publication evidence is verified against live Git state at handoff; no self-referential commit hash is embedded here.
- Open issues/PRs at bootstrap inspection: none. This is a setup record, not an atomic work claim. Recheck before any new task.

## Current documentation task — pending integration

- Owner/requester: Farzaan Dalwai, authenticated account `farzaandalwai`; branch `farzaandalwai/automatic-session-start`, based on current `origin/main`.
- Task: remove repetitive manual starter-prompt pasting. Make the automatic `AGENTS.md` startup workflow explicit while retaining short human task requests.
- Files: `AGENTS.md`, `README.md`, `starter_prompt.md`, this context, contribution/AI logs, and the saved user request. Dependencies: official OpenAI instruction-discovery documentation and the existing repository rules. No open issues/PRs overlapped at task start.
- Acceptance: no onboarding instruction requires repasting the starter; `AGENTS.md` directs startup context/Git checks; humans can say their task, “get me oriented,” or resume an already recorded task; no new experiments. Check Markdown paths and inherited artifact integrity with the existing setup checker, then publish a small task PR for human integration.
- Status: documentation changes complete on this branch only; not integrated into `main`. `python3 scripts/verify_setup.py` passed, including unchanged original hashes and current Markdown paths. The integrated bootstrap already contains startup-check instructions in `AGENTS.md`; this task removes misleading manual onboarding directions. Human PR review/integration remains pending.

## Verified, inherited, missing, and pending

- Imported unchanged: Timothy's script/notebook/exploration script, original UTF-16 handoff README, exact manifest/pilot/exclusions, baseline predictions/metrics, raw audit. A separate UTF-8 reading copy is documented. All ten requested non-raw artifacts are present. [Provenance](docs/provenance.md) contains sources/timestamps/hashes.
- Verified in setup: readability, byte counts/hashes, Python syntax, notebook JSON/code syntax, schemas, unique keys, fixed manifest/calendar/split consistency, and ignore rules. See [verification](docs/setup_verification.md) for exact executed checks and limits.
- Inherited, not independently reproduced: raw-export audit (1,459,198 rows, 19 columns, 16,214 series; one 28-day `(420, 764)` excluded; no nulls/duplicate keys reported) and four six-decimal baseline score rows on 3,000 validation/test targets each. These are local-export counts and baseline evidence, not the main comparison.
- Missing by design: raw `data/freshretail.csv` (323,577,557 bytes in Drive metadata; not downloaded or hashed). Other unavailable references: original proposal/intermediate report and professor starter code. [Data instructions](data/README.md) explain acquisition.
- Pending: formal stockout-field/indexing audit, matched eligibility/feature/prediction contract, filter counts, features, regression/tree/ridge runs, matched baseline rescoring, formal leakage audit, clustered evaluation, literature verification, individual reports/disclosures, and presentation. No experiment was run by setup.
- Limitations already fixed in the record: all-90-day completeness selection differs from training-only selection intended in the proposal; baseline test scores were already visible. Preserve/disclose both. Sustainability benefits remain unmeasured.

## Team and access

- Timothy Tran: existing preparation/pilot/baselines; reproduction support. Supplied account `timothytran109`.
- Farzaan Dalwai: protocol/integration/formal audit/evaluation and bias analysis, pending beyond setup.
- Shoury Ambarish Parab: planned linear/ridge experiments.
- Denisha Tank: planned decision tree; optional random forest after course-fit check.
- Mansi: planned stockout features; optional context comparisons.

Full-name mapping for `shoddy16` is unconfirmed. Five academic assignments remain intact; only `shoddy16` and `timothytran109` were invited. Both accepted during setup: collaborator/effective-permission readbacks verified write access and `admin: false` for each, with no invitations pending. This is verified repository access, not a claim that their clones or multi-user workflow were tested. Repository: [farzaandalwai/data245-group3](https://github.com/farzaandalwai/data245-group3), private.

GitHub rejected protection configuration with HTTP 403 requiring Pro or public visibility. No visibility/plan change was made. PR review, one approval, no force pushes/deletions, and sequential human integration are **team conventions, not enforced protection**.

## File map and next bounded task

- `README.md`, `AGENTS.md`, `starter_prompt.md`: orientation and safe collaboration workflow.
- `docs/experiment_protocol.md`, `docs/course_requirements.md`: fixed design/deviations and individual deliverables/rubric.
- `docs/provenance.md`, `docs/handoff/`, `data/README.md`: source bytes, attribution, data acquisition.
- `docs/contributions.md`, `docs/ai_assistance.md`, `docs/prompts/`: actual contributions/disclosures.
- `scripts/verify_setup.py`: standard-library read-only integrity/schema checker, not the ML pipeline.

Optional human coordination check: two teammates make separate tiny documentation PRs, merge sequentially, then each session fetches and identifies both preserved updates. Success requires both contributions, accurate shared-state descriptions, and no direct edits to main. This check has not been performed; no teammate work was simulated.

Next technical task to assign explicitly: inspect pilot schema/stockout semantics and freeze the matched eligibility/feature/prediction contract, with no model fitting. Confirm an owner/branch/files/dependencies/acceptance criteria before implementation. Also verify exact deadline/presentation slot in Canvas and confirm remaining GitHub/name mappings when needed. Setup stops here.
