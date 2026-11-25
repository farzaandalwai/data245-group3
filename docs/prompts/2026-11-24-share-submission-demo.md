# Authorized submission package sharing

User request, November 24, 2026 (America/Los_Angeles):

> can you push everything in my submission_local? my teammate needs it cuz he's running the presentation on his computer

Authenticated requester: DELTA / Timothytran109. This request explicitly
authorizes the scoped commit/push needed to share the submission package,
superseding earlier local-only/no-publication restrictions for this task.
No merge or direct teammate message is authorized.

Owner: DELTA. Branch: `DELTA/share-submission-demo` from fetched main `dc5c10c`.
Implementation uses isolated worktree `C:/Projects/data245-submission-share`;
the original checkout and its branch are left intact. At task start all meaningful
submission files except the ignored fitted model were already on origin/main.
Notebook checkpoint caches remain ignored; no user files are deleted.

Files/dependencies: include the exact verified 3,810-byte joblib with a narrow
ignore exception; preserve its and the script's bytes on checkout; add pinned
demo dependencies and a fresh-computer setup guide; update entry-point docs and
required context/contribution/AI records. Existing experiment code/configs,
archives, reports/results and original model mathematics are unchanged.

Acceptance: inspect all submission contents and notebook outputs for credentials,
private datasets and unnecessary large payloads; retain the existing authentic
demo observation/aggregate plots; verify copied model/script hashes; run embedded
CLI and notebook inference in the isolated checkout without fitting or an external
bundle; inspect staged paths/diff; publish a task branch and draft PR, then read
back the remote commit/model bytes. No new training, tuning or final evaluation.
