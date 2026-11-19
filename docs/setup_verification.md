# Setup verification

Date: 2026-11-18 (America/Los_Angeles). This is setup/import evidence only.

## GitHub checks

- Authenticated identity verified with `gh api user`: `farzaandalwai`. Initial sandbox network errors did not reflect the actual credential status; network-enabled authenticated calls succeeded.
- The current directory was empty, with no Git repository/remotes. The target personal repository returned 404 before creation. It was created as private with description `DATA 245 — Group 3: Stockout-Aware Forecasting`, then read back with `private: true`.
- Canonical URL: [https://github.com/farzaandalwai/data245-group3](https://github.com/farzaandalwai/data245-group3).
- `gh api users/shoddy16` and `gh api users/timothytran109` validated both accounts. Pending invitations and existing collaborators were inspected first. Exactly these two accounts received `permission=push` invitations; initial readback reported both pending with `write`. Both accepted during setup. Subsequent collaborator and individual `/permission` readbacks verified `shoddy16` and `Timothytran109` with `role_name: write`, `push: true`, and `admin: false`; pending invitation readback was empty. Owner `farzaandalwai` retains owner/admin rights.
- `gh issue list` and `gh pr list` returned no open issues or PRs; `git fetch origin` succeeded against the empty new repository.
- Attempted `PUT /repos/farzaandalwai/data245-group3/branches/main/protection` with PR review, one approval, stale-review dismissal, admin enforcement, force pushes disabled, and deletions disabled. GitHub returned HTTP 403: “Upgrade to GitHub Pro or make this repository public to enable this feature.” This is an external plan limitation, not an approval rejection. No plan or visibility change was made. Review/approval/no-force-push rules are team conventions and are not enforced protection.
- Initial commit/push and remote tree/ref readback are the final bootstrap steps. Use the live commands below to check publication; Git history is the commit evidence. No multi-user coordination check has been performed.

## Original bootstrap local import checks

The checker is `python3 scripts/verify_setup.py`, using the standard library. Python version at setup: 3.14.2. The checker does not import `pandas`/`numpy` or the original scripts, execute cells, train, regenerate data/predictions, or recompute metric values.

Its scope is original-byte SHA-256/size comparisons; UTF-16 BOM and UTF-8 text-equivalence checks; Python AST parsing; notebook JSON/cell shape and code AST parsing; exact CSV schemas; manifest and excluded-series consistency; unique pilot keys; complete 90-day calendars; day/split boundaries/counts; inherited prediction key coverage/actual-value alignment; metric row/schema checks; current Markdown readability/local paths; and representative Git ignore rules. It does not verify complete notebook schema conformance with an external validator.

Original checksum values were computed after import and verify local integrity against those acquired bytes. No independent historical checksums were supplied. Raw audit claims remain inherited because the 324 MB raw export was intentionally not downloaded.

First completed run succeeded with this output:

```text
PASS: ten original file hashes/byte counts and README encoding conversion
PASS: 3 Python files parsed; notebook JSON/31 cells, 13 code cells parsed without execution
PASS: pilot schema, unique keys, exact manifest/calendar and splits {'train': 12000, 'validation': 3000, 'test': 3000}
PASS: inherited prediction/metric schemas, coverage and actuals (scores not recomputed)
PASS: 14 current Markdown files/paths and Git ignore/retention rules
SETUP CHECKS PASSED. No raw pipeline, notebook cells, features, fitting, or scoring executed.
```

Package installation and full pipeline/model runtime remain unverified.

All 32 staged files were inspected individually for path, byte count, and equality of staged/local bytes; all ten imported original blobs also matched their recorded SHA-256. `.gitattributes` preserves their bytes across Git line-ending settings. The initial generic whitespace check flagged inherited CRLF endings. The CRLF-aware `git -c core.whitespace=cr-at-eol diff --cached --check` passed without changing original artifacts. The exact saved setup prompt also matched the user-supplied file. A targeted credential/private-key/expiring-download-reference scan found none in the saved files.

## Live publication/access checks

Run from the repository root after setup:

```sh
git status --short --branch
git remote -v
git fetch origin
git rev-parse main origin/main
gh repo view farzaandalwai/data245-group3 --json url,isPrivate,defaultBranchRef
gh api repos/farzaandalwai/data245-group3/invitations
gh api repos/farzaandalwai/data245-group3/collaborators
```

Invitations are time-sensitive: recheck before claiming accepted access. A teammate must accept before verified private-repository access. The clone/open/starter-prompt workflow and optional two-human documentation PR exercise have not been executed on teammates' machines.

No new experiment, final report, presentation, disclosure certificate, literature survey, leaderboard rank, or measured sustainability finding is setup evidence.

## Later structure migration

The bootstrap results above are historical checks on the initial layout. The current archive/canonical paths, extended ignore checks, and YAML/TOML/output-safety regression checks are documented in [structure_migration.md](structure_migration.md). The raw destination is now `data/raw/freshretail.csv`. No original checksum or inherited result was changed by the migration, and no legacy producer/notebook was run.
