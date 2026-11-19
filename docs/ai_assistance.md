# AI assistance disclosure

## 2026-11-18 — setup and import

- Tool: Codex desktop coding agent. Model family exposed by this session: GPT-6. Exact model variant/version: **unknown**. Do not infer a precise release identifier.
- Exact supplied setup instruction: [docs/prompts/DATA245_Codex_Setup_Prompt.md](prompts/DATA245_Codex_Setup_Prompt.md), copied byte-for-byte. This is the supplied prompt, not earlier unseen conversations.
- Exact substantive follow-up authorization: [docs/prompts/2026-11-18-setup-authorization.md](prompts/2026-11-18-setup-authorization.md). The earlier attachment message had a blank request; the agent first read it and asked for scope, then proceeded after this explicit authorization.
- Assistance scope: repository creation, the two authorized write invitations, import/migration of ten team artifacts, README encoding conversion, documentation/protocol/course checklist, Git ignore/dependency/PR files, and a standard-library read-only structural checker. No feature producer, trained model, full pipeline execution, new final finding, or individual report was produced.
- Tools used: shell/Git, authenticated `gh`, Google Drive connector for source discovery/fetch, system `curl` for materializing connector file references, Python standard library for inspection/integrity checks, web browsing for upstream dataset/license verification, and file patching. A Node fetch and Python HTTPS download failed due to network/TLS certificate-store issues; system-trusted `curl` succeeded without disabling TLS verification. Initial sandboxed `gh` access failed; approved network execution verified the real account. No credentials or expiring file URLs are saved in the repository.
- Skills used: Google Drive for discovery/import and create-rule guidance adapted to the explicitly requested root `AGENTS.md`. Spreadsheet guidance was consulted while scoping CSV inspection; no workbook was authored. The work remained a repository setup with structural CSV checks.
- Validation actually performed by the agent: inspect original code/notebook cells, compare downloaded byte counts, hash originals, syntax/JSON parsing, CSV schema/key/calendar/manifest/split consistency, and Git ignore/staging/publication readbacks as detailed in [setup verification](setup_verification.md). No independent raw-data or metric reproduction is claimed.
- Human validation: setup was authorized by the user, but human review of generated files, academic claims, and the future experiment contract is **pending**. Authorization is not recorded as completed technical review.

Imported Timothy Tran artifacts retain their original authorship. His earlier AI use, prompts, and model versions are unknown to this session and must not be inferred. The setup prompt's prior preparation/review statements remain source claims at their stated status.

## 2026-11-18 — automatic session-start guidance

- Tool/model: Codex desktop, GPT-6 family; exact model variant/version unknown. Skills: OpenAI Docs for current product behavior; previously read create-rule guidance for the compact repository instruction update.
- Exact prompt: [2026-11-18-automatic-session-start.md](prompts/2026-11-18-automatic-session-start.md).
- Scope: remove repeated manual starter-prompt pasting from onboarding, state that `AGENTS.md` supplies startup guidance, and support short orientation/task/resume requests. Source checked: [official OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md). No hook or scheduled automation was added.
- Validation: `python3 scripts/verify_setup.py` passed (ten original hashes/byte counts and encoding conversion; Python/notebook parsing; pilot schema/manifest/keys/calendar/splits; inherited prediction/metric structure; 14 current Markdown files/paths; ignore rules). The task diff was reviewed for documentation scope. No new tests or experiments were run; imported source/data/result files are unchanged.
- Branch/integration: `farzaandalwai/automatic-session-start`, not merged into `main`; human PR review/integration and human validation remain pending.

## Required future updates

For every substantive AI-assisted change, add date, actual tool/model if exposed (unknown otherwise), exact prompt or saved repo-relative prompt path, relevant assignment item and assistance scope, changed artifacts, checks, human validation, and branch/PR/integration state. Each student's final disclosure must reflect their own use and answer the assignment's similar-solutions/GenAI questions. No SJSU disclosure certificate was created or submitted here.
