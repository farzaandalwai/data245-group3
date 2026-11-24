# Final publication and submission checklist

November24, 2026 (America/Los_Angeles). Submission target: tomorrow, November25; confirm the actual Canvas deadline and presentation slot. No new training, scoring, tuning, commit, push, merge or upload was performed during reconciliation.

Run: `final-1000-attested-20261124T094349Z`. Ridge-aware test MAE0.377191, RMSE0.618490, bias-0.056262. Source main47f531f includes PR11/12. Worktree `A:\Projects\DATA 245\data245-group3-final-execution`, branch `DELTA/final-execution-readiness`. Original main remains dfd4c94 with its audit files; other worktrees were preserved.

## Submit tomorrow: priority order
- [ ] Human-review `submission_local/report/final_report.md` and `submission_local/presentation/slides.md`. Use each student's actual contributions and required report/template; do not submit shared prose as independent individual work.
- [ ] Use corrected pooled-row 95% intervals: Linear [-0.002183659272,-0.000134824602], Ridge [-0.002301963340,-0.000290025655], Tree [+0.000054234535,+0.001937705144]. Remove the old final claim that all intervals include zero. Development R3 intervals still include zero and were not changed.
- [ ] Say gains are modest (Ridge0.343760%, Linear0.305113%), while Tree worsens0.246452%. Include that Linear/Ridge stockout-day MAE worsens despite overall improvement; no blanket stockout-day benefit.
- [ ] Retain historical holdout exposure, retrospective full-horizon completeness, descriptive/conditional interpretation and project-lead-attestation provenance. Original teammate dates/messages remain unverified. No causal food-waste or latent-demand finding.
- [ ] Update external report PDFs and slide PPTX/PDFs from these sources, including tables, intervals, conclusion, notes and run identity. No PDF/PPTX/PPT/DOCX/LaTeX exports were found under `A:\Projects\DATA 245` (environments/cache/junctions excluded), nor an automatic export pipeline. Actual external file paths/version state are UNKNOWN. The report PDF submitted to Canvas, presentation PPTX/PDF used in class, and any individual report copies require separate owner review; Markdown edits do not update them automatically.
- [ ] Preview final exported pages/slides; verify references, captions, figures, assignment rubric, individual attribution/GenAI disclosure and filenames. Do not overwrite historical experiment evidence to prepare submissions.

## Evidence and Git inventory
Full inventory: `docs/final_execution_evidence/final-1000-attested-20261124T094349Z/PUBLICATION_INVENTORY.csv` (19 rows), with exact absolute original paths, run ID, original byte sizes/SHA-256, ignore rules and prepared destinations. Inventory SHA-256: `bd978260857cc9d232d4c6517fe240a7e6daa6436bdb62587bec1828dd028113`.

Prepared small Git candidates: seven original result files (overall, subgroups, paired comparisons, intervals, per-store diagnostics, coverage audit, manifest), original log/verification JSON, verified handoff/results copies, approved-settings and enabled-contract snapshots. Original freeze and two authorization texts remain at their original docs paths. All copied originals retain identical bytes. Freeze/source records may contain original local paths; preserve them as provenance, not executable portable commands. The proposed Git package is a PARTIAL mirror; do not describe it as a complete prediction package.

Reviewed staging scope (scoped commit/push/PR authorized November24; merge and bulk upload are not authorized):
- `.gitattributes`, `.gitignore` (narrow exact-byte / small-CSV rules).
- `submission_local/report/final_report.md`, `submission_local/presentation/slides.md`, `submission_local/README_SUBMISSION.md`, `METHODOLOGY_AND_REPRODUCIBILITY.md`, `TECHNICAL_STATUS.md`, `SUBMISSION_BLOCKERS.md`, `EVIDENCE_INDEX.md`, and the corrected tail of `MODEL_COMPARISON.md` (all under submission_local).
- `docs/FINAL_SUBMISSION_CHECKLIST.md`, `docs/FINAL_FREEZE_20261124T094349Z.json`, the two new dated docs/prompts authorization files, and `docs/final_execution_evidence/final-1000-attested-20261124T094349Z/` (only prepared small evidence).

EXCLUDE from staging: live `configs/contract.yaml` and `configs/final_settings.json`, all results/ bulk directories, raw/input data, .venv, other worktrees, junctions, credentials, temporary files and unrelated prior audit prompts. Existing freeze/config changes in this branch predate reconciliation; they are NOT automatically part of a publication commit. The approved settings are instead preserved as exact historical evidence in `final_settings_at_execution.json`.

## Bulk storage: authorization still needed
| Original payload | Bytes | SHA-256 |
| --- | ---: | --- |
| `per_series.csv` | 3020569 | `ac8ee3f4cafcb60fec1c2655545affe9582a749205308153a73a310a84a244e9` |
| `predictions.csv` | 76348581 | `49d08764862627a20bda16eba376d3f5026b007e539525581e5052cb335b1ce5` |

These two original files remain only at `A:\Projects\DATA 245\data245-group3-final-execution\results\final_evaluation\v2\final-1000-attested-20261124T094349Z\`. Predictions are about72.8MiB; per-series diagnostics about2.9MiB. Use a separately reviewed immutable shared archive for both. Git LFS is an alternative only after explicit team adoption; no LFS configuration is assumed or changed. The original manifest binds these hashes; include it in the archive and record the actual shared URL/access policy after authorized upload. No archive URL is invented. No large payload was copied or uploaded here. Raw data and credentials are excluded.

Before publication: approve destination/permissions; verify originals against manifest; upload only authorized files; verify the downloaded package hashes; record the location and retention/access instructions. Current Git ignore rules still reject unreviewed/bulk CSVs. New attributes preserve small original evidence bytes without normalizing historical files.

## Prevent accidental repeat scoring
HIGH risk: current live execution configuration has all three V2 flags true and approved settings. The evaluator refuses an existing destination but accepts a different run ID; it has no single-use consumed-authorization check. Committing enabled gates would authorize repeated new-ID scoring. No one-shot protection is claimed.

To preserve original bytes, this task did NOT change those live files. Captured exact `contract_at_execution.yaml` and `final_settings_at_execution.json` retain the historical authorization state. A separate `contract_for_publication.yaml` is explicitly a DERIVED candidate with all three flags false; it is not historical execution evidence. Main already has false flags and proposed active settings. Keep main's defaults closed by excluding both live execution configs from staging. If an active config must be published later, use the reviewed closed-gate candidate, never the enabled execution copy. Avoid `git add .` or staging the entire worktree.

The freeze remains historical scientific acceptance; it is not an ongoing instruction to execute again. The reconciled README removes runnable scoring commands. A future one-time runtime capability/consumed-run ledger would be separate technical work, not silently introduced here. No preflight/test suite that fits fixture models was run during documentation reconciliation; checks here are hashes, inventory, text consistency and Git scope only.

## Historical evidence boundary
The November20 `final-authorized-20261120-r1` outputs remain historically unverified. Existing text before reconciliation remains available in Git history at91fab8d; original archives, input bundles, result bytes and prior audit handoffs were not edited. New rounded MAEs matching the old report do not recover or establish provenance of the old run. `submission_local/run_manifest_committed_check.json` remains untouched and explicitly identified as a DEVELOPMENT tree manifest, not final evidence.

## Final review before any commit or upload
- [ ] Review the exact path allowlist above, staged diff and default-closed gates; no raw data, secrets, environments or large files.
- [ ] Verify original manifest/settings/freeze hashes and prepared-copy inventory; preserve machine-specific original provenance without treating those paths as portable links.
- [x] Scoped commit/push/PR authorization received November24. Merge and archive upload remain subject to separate review/authorization.
- [ ] Ensure teammates actually receive the reviewed small files and both large payloads. They are not shared merely because present in this local worktree.
