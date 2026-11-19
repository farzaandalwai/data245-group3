# Starting or resuming work

**You do not need to paste this file into every chat.** Clone the repository once into your own folder, open that folder as the project in Codex, and send a short task request. Each human uses a separate clone; concurrent sessions on one computer use separate worktrees.

Codex loads the root [AGENTS.md](AGENTS.md) as project guidance. That file directs it to inspect Git state, fetch origin, read the latest shared/local context, verify identity, and check for overlapping work at the start of a task. See the [official OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) for instruction discovery. `starter_prompt.md` has no special automatic-loading role.

## What to type

- First session or no assigned task: **“Get me oriented.”** Codex should summarize completed/pending work and suggest a bounded task without starting remaining experiments.
- Returning to an existing task: **“Continue my task.”** Codex should inspect current state and resume only when the recorded owner/branch/task is unambiguous. Otherwise it should help clarify the next task.
- Starting new work: state the bounded task in an ordinary sentence, such as **“Review the documented eligibility contract and list unresolved decisions; do not implement it yet.”**

The repository rules supply the repeated collaboration/protocol instructions. The short human message supplies the task. Previously agreed tasks can be recovered from the current chat and recorded branch/context/issue state; an academic role alone is not authorization to run every remaining experiment.

## Optional fallback

If a session appears to have missed the project guidance, first confirm that the actual clone is open as the project, then start a new chat there. You can also send this short diagnostic request:

```text
Show which AGENTS.md instructions apply, read the latest shared context,
and get me oriented. Do not change files or run experiments.
```

No additional hook, scheduled automation, or service is needed for this workflow. Automatic instruction loading supplies guidance when Codex starts work; it does not synchronize uncommitted changes, merge PRs, or start tasks without a message.
