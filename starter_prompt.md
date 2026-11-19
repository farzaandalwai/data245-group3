# Reusable cross-tool startup prompt

Root [AGENTS.md](AGENTS.md) is the common repository guidance. This optional prompt can be pasted into Codex, Copilot, Claude or another coding assistant; it is not a second protocol.

```text
Handle only my bounded request. Inspect Git status, branch, remotes, recent history,
and fetched origin/main; compare local/shared state and check overlapping issues/PRs.
Do not overwrite or merge unrelated work.
Read AGENTS.md, context.md, docs/experiment_protocol.md, docs/interfaces.md,
docs/team_responsibilities.md and the relevant owner folder README.
Summarize the approved design and actual implementation status; distinguish
approved science, draft contracts, pending verification and historical evidence.
Identify my workstream, owner and dependencies. Flag conflicts or missing technical
decisions before implementation. Follow the common document hierarchy; historical
handoffs and old contracts cannot override the approved protocol.
Make only requested changes; do not start experiments from an orientation request.
My bounded task is: [describe task and constraints].
```

"Get me oriented" requests orientation only. "Continue my task" resumes only an unambiguous recorded task after checking current state. Separate humans use separate clones; concurrent implementation sessions use separate worktrees and task branches under the collaboration rules. Explicit task constraints, including requests for uncommitted current-tree edits, take precedence.
