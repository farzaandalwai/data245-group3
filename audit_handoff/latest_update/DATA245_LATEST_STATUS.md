# DATA 245 — post-merge incremental status

**2026-11-23, America/Los_Angeles. Audited remote main: `4dffb0d5a463955a5dae4aa059326a403ebc3fdb`.** Baseline: the immediately preceding audit in this directory, which inspected PR tips `91fab8d`, `8a7636b`, `99481e7` before integration. This update rechecks evidence rather than treating that audit as current authority.

**Conclusion: integration is complete; final 1,000-series experiment completion remains NOT VERIFIED; submission is not ready.** No newly available experimental output or revised report was introduced beyond the files already inspected before merging.

## 1. Git state and what actually changed

- Working branch **main**, local HEAD **`c54f9ab1d499e754f77c4a85422445a0614f3850`**. Fetch succeeded. Local main **does not match remote**: it is 14 commits behind, with no local-only commits. It was deliberately left in place; all current-main evidence below was read through Git objects, not a checkout/pull.
- Initial tracked working files and index were clean. Previous audit directory and prompt were untracked; the CSV was ignored by `.gitignore:25` (`*.csv`). Those files were preserved/updated as requested. No source edits, branch switch, stash, index changes, training, installation, push or merge by this audit.
- Authenticated GitHub `Timothytran109` / Timothy Tran matches DELTA. The historical context's current-requester field is stale. Codename responsibilities are not verified personal authorship; `shoddy16` full-name mapping remains unconfirmed.
- GitHub confirms **PR #8 merged** into SAS/development-comparison at **`8b0f9ce`**; **#7 merged** into main at **`0645046`**; DEVGRU merged main into its branch at **`d9065a2`**; **#6 merged** into main at **`4dffb0d`**. All occurred November 23. No open PRs/issues at the check.

Compared with old local main `c54f9ab`, remote main changes **97 files: 78 added, 19 modified, zero deleted**. This integrates the DEVGRU development artifacts, original SAS tree artifacts, harmonized R3 comparison, forest implementation/tests, requirements, verifier/evaluator updates, final-run script and Markdown submission sources.

**Delta from what the previous audit already inspected: four merge commits, zero new file content.** A path/blob comparison of all **229 files** in current main against the three pinned PR trees found that every current file is byte-identical to one previously inspected version. All paths from their union are retained. Thus there are **no newly observed experiments, predictions, model outputs, figures, report versions or slide versions**. The significant improvement is that previously separate code and evidence now coexist on main. Archive/original pilot/manifests/inherited results/V1 history remain unchanged.

## 2. Blocker-by-blocker reassessment

1. **DEVGRU output retrieval — RESOLVED, now merged.** `artifacts/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/` contains the four prediction files, alpha grid scores, metrics and metadata. Original fitted Linear/Ridge/scaler artifacts remain absent.
2. **SAS tree artifact retrieval — RESOLVED, now merged.** `artifacts/SAS/development/original-200-series-20261119/decision_tree/` contains predictions, selection, run manifest and both numeric trees. Inference replay still matches exactly.
3. **Cross-team development packaging/integration — RESOLVED for the existing development comparison.** DEVGRU files, SAS originals and `src/evaluation_SAS/integration.py` now coexist in one main tree. The adapter deliberately normalizes per-condition run IDs in memory; R3's manifest binds the original inputs. The generic/final run envelope is still not an accepted frozen contract, and CLI execution is dependency-blocked here.
4. **Bootstrap consistency — PARTIALLY RESOLVED, unchanged scientifically.** Common development R3 uses the approved row-weighted whole-store method; original DEVGRU series intervals stay labeled separately. Final runner still uses incorrect equal-store weighting.
5. **Dependencies/tests — PARTIALLY RESOLVED.** Requirements and SAS tested versions are now merged; packages remain absent in this environment. All eight merged test modules fail the import probe before any test runs.
6. **Final technical freeze — UNRESOLVED.** `configs/contract.yaml:6,15,16` still has contract_frozen, initial_validation_parameters_frozen and new_model_test_evaluation_allowed all false; version remains 2.0-draft. A PR merge is not evidence of the required recorded technical freeze.
7. **Final 1,000-series completion — NOT VERIFIED.** Claimed run outputs remain absent from remote Git and local disk. Delivered runner cannot pass its committed guard. A private/external run cannot be ruled out.
8. **Final tables/error analysis — PARTIALLY RESOLVED.** Development tables/subgroups/store/series summaries and figures are now merged. Final metrics, error analysis and confidence intervals remain unsupported prose claims.
9. **Documentation — PARTIALLY RESOLVED.** Branch-only status is obsolete, but merged docs still contradict one another about final execution, local data and implementation status.
10. **Report/presentation/submission evidence — PARTIALLY RESOLVED.** Markdown sources are now merged. No PDF/LaTeX/PPTX/DOCX exports, completed individual reports or new human review/submission records were found.

Additional prior findings remain: original DEVGRU execution lineage is incomplete; forest outputs are documentation-only; business/export/scaling semantics remain provisional; individual authorship/deliverables need evidence. The CRLF-versus-Git-LF inventory mismatch remains fully explained by byte conversion, not changed predictions. No additional source changes were requested or made to resolve these.

## 3. Reverified results and final-experiment evidence

**Verified cohort remains development `v2-development-200-r2`: 200 series / 113 stores; 9,200 train and 3,000 validation rows per learned condition.** Protocol 2.0 / producer 2.0.0; declared manifest SHA `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`. All compared conditions/models/baselines have identical keys, actuals and splits. The exact bundle is still absent locally; canonical pilot and saved predictions support these population checks.

Reran the numerical audit against **origin/main**, rather than trusting previous CSV values. All **79,200 prediction records**, **20 saved metric-summary rows** across three files and **16 subgroup rows** pass the same independent checks. Both baseline formulas match reconstructed past sales. Both saved numeric trees reproduce **12,200 predictions per condition, maximum difference zero**, without fitting.

**Best verified development-validation results (N=3,000):**

- MAE and RMSE: **stockout-aware Ridge — MAE 0.33411891383472503; RMSE 0.531885179271836; signed bias -0.006927125957455808**. Run `dev-v2-r2-linear-ridge-standardize-20261119-ridge_regression-stockout_aware`.
- Smallest absolute signed bias: **sales-only Decision Tree — +0.0006305492456096237**, MAE 0.34825541775779445. Run `sas-tree-dev-200-bootstrap-r1`.
- Baseline validation MAEs: recent_avg_7 **0.3373804761904762**, persistence **0.41775666666666667**; common run `SAS-validation-reference-formulas-20261120`.
- Matched aware MAE improvement: Linear **+0.019857%**, Ridge **+0.041019%**, Tree **-1.095300%**. These are descriptive development comparisons, not final improvements.

R3 saved 95% paired store intervals for aware-minus-sales MAE remain Linear **[-0.002462373,+0.002372520]**, Ridge **[-0.002426988,+0.002148368]**, Tree **[-0.003332124,+0.013629308]**. All include zero. Files, point estimates and implementation were checked; NumPy/PCG64 endpoint regeneration remains blocked. Do not equate an interval including zero with proof that feature effects are absent.

**CSV update:** 14 rows retained: six learned-model train diagnostics and eight validation results including baselines. Metrics/run IDs are unchanged; every artifact ref/commit now points to **origin/main / 4dffb0d**. No historical-test, summary-only forest or unverified final values added.

**Final population:** `docs/DELTA_V2_RUN_EVIDENCE.json` previously records final-input generation for `v2-final-1000-r2`: **46,000 train / 15,000 validation / 15,000 test = 76,000**, 1,000 series / 183 stores / 239 products, trusted manifest `52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c`. That record is unchanged. Neither raw export nor final bundle is here, so actual final-run population/usage cannot be independently established.

**Final outputs:** `results/final_evaluation/v2/final-authorized-20261120-r1/` is still absent. No final predictions.csv, metrics.csv, paired_intervals.csv, subgroups.csv, per_store.csv or run_manifest.json exists in current Git/local disk. Reported final Ridge MAE **0.377191** and other final values remain **REPORT ONLY / NOT VERIFIED**, excluded from the results CSV. There is no verified final winner.

**Final configuration:** new script still hardcodes development-selected Ridge alpha **10/100**, tree depth **5** / minimum leaf **5** for both conditions, training-only linear standardization, seed 245 and no clipping. These settings and selection records are inspected, but do not prove a final run or pre-test freeze occurred. Forest `sas-forest-dev-200-r1` remains summary-only; neither its predictions nor saved selection/manifest became available.

## 4. Scientific validity and report/slides

Unchanged past-only features, explicit 9/+5 allowlists, chronological splitting, train-only preprocessing and validation-only selection remain supported by code/available development evidence. No test-based tuning was found in those records. Decisions in an unpreserved external final run cannot be verified. Historical test exposure and retrospective complete-series selection remain limitations; recorded sales are not latent demand. No measured waste reduction, causal effect or inventory-policy improvement is established.

Two final-run defects remain in `scripts/final_evaluation.py`:

- **Lines 103–105:** equally average within-store MAE differences in bootstrap draws. Approved method pools loss sums and divides by each draw's total row count. With unequal store sizes, its row-weighted point estimate and store-weighted interval describe different estimands.
- **Lines 117–119:** read legacy V1 `configs/contract.lock.json`, rather than authoritative V2 gates. Its two required flags are false. Executing the exact guard alone again raises `Frozen contract gates are not enabled` before data access. Active YAML preflight gates are also false. The entire final runner was not executed.

Newest report/slides are **unchanged** from audited commit `91fab8d`, now in `4dffb0d`: `submission_local/report/final_report.md` (46 lines), `submission_local/presentation/slides.md` (12 sections). Their intended methodology and caution about recorded sales/test exposure align, but they are **not technically substantiated as a final-results submission**:

- Report lines **6,22–46** and slides **7–9,11–12** assert final results/subgroups/uncertainty/reproducibility without the cited artifacts. The final bootstrap claim also omits the weighting defect.
- `submission_local/TECHNICAL_STATUS.md:25–29` and `SUBMISSION_BLOCKERS.md:5–6` say final/preflight PASS. This conflicts with committed gates and `docs/FINAL_SCORING_READINESS.md` (BLOCKED).
- `submission_local/METHODOLOGY_AND_REPRODUCIBILITY.md:25` says no fitting/prediction/scoring occurred; its absent-DEVGRU-predictions statement is stale now that those CSVs are tracked on main.
- R3 development tables/figures and `submission_local/MODEL_COMPARISON.md` remain correctly labeled development, not final. Figure hashes pass; no new final figures or rendered-layout assessment.
- `docs/SAS_RANDOM_FOREST.md:31–33` still wrongly describes the 7-day mean as better than its documented forest MAEs. No forest numerical claim has been independently promoted to verified.

Supplied `docs/course_requirements.md` / `docs/COURSEWORK_DELIVERABLES_TRACKER.md` still do not establish completed individual IEEE reports/PDFs, LaTeX, literature, lessons, CRediT/GenAI/rubric appendices or delivered presentation. Original course rubric and Canvas records remain unavailable; verify those requirements directly rather than treating the checklist as independent rubric verification.

## 5. Checks actually performed now

- Successful fetch, authenticated identity, PR/issue/merge ancestry review, local-vs-remote comparison and full path/blob comparison against all three prior audit trees.
- **39 merged Python files parse** via AST. Import probe of the **eight merged test modules** is blocked (five need numpy first, three need yaml first); **zero unit tests executed or passed in this follow-up**. This probes fetched test source in memory, not a local checkout of new main.
- Required installed packages remain absent: numpy, pandas, scikit-learn, PyYAML, matplotlib, scipy, pytest, IPython. No dependencies installed. Prior setup PASS / historical suite-success records are not new merged-main runtime successes.
- Standard-library prediction/metric/subgroup/formula checks and numeric-tree replay described above all pass on current remote artifacts.
- Original SAS checksum file **18 entries pass** and harmonized package **16 entries pass**, against Git blob bytes. DEVGRU prediction/metric hashes match prior evidence. Metadata/report CRLF hashes still differ from LF blobs by the previously verified representation conversion only.
- Exact final-guard prefix blocks as above; no final-data loading, new test scoring, model training or full raw/bundle reproduction. Bootstrap endpoint reproduction remains blocked.
- Tracked source/index remain unchanged. Updated handoff CSV schema/counts/metric values and artifact commits are separately validated; existing ignore rules preserved.

## 6. Remaining work and readiness

**Resolved by merging:** branch-only availability, missing combined main snapshot, and development adapter/artifact integration. Previously resolved retrieval blockers now have main-branch evidence. **No scientific final-result blocker was resolved by these merges.**

Before submission, in dependency order:

1. Recover the exact claimed final run and its accepted input/freeze/source/environment record. If unavailable, retract unsupported completion/results claims. Preserve original bytes and disclose prior test exposure.
2. Resolve the V2 freeze and correct/review final gate authority and pooled-row bootstrap; reverify recovered predictions, actual sample counts, subgroup metrics and CIs. Any future evaluation is separate authorized work; no rerun was performed here.
3. Prepare dependencies/exact bundles in an approved environment and execute the merged validation suite; retain actual logs. Metric recomputation is not reproduction of original model fitting.
4. Reconcile report/slides/status/methodology and verify individual deliverables, human contribution/disclosure records, rubric, export/access/file-size and presentation/submission evidence.

Local main can later be advanced safely after preserving/rechecking local files; it was not synchronized during this audit. Responsibility areas remain DELTA data, DEVGRU linear/ridge, SAS evaluation/tree, team acceptance/coursework; these are not new assignments or authorship claims. Optional forest recovery or extra sensitivity studies should not delay required evidence.

## 7. Evidence paths and handoff

All scientific evidence references in this report refer to **remote commit 4dffb0d**, not the still-old local checkout. Main locations:

- `artifacts/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/` — four predictions, validation_metrics.csv, ridge_alpha_selection.csv, run_metadata.json.
- `artifacts/SAS/development/original-200-series-20261119/decision_tree/` — predictions.csv, selection.json, numeric trees, run_manifest.json.
- `artifacts/SAS/development/harmonized-200-series-20261120-r3/` — overall.csv, subgroups.csv, paired_comparisons.csv, mae_difference_intervals.csv, validation_baseline_predictions.csv, comparison_manifest.json, figures/checksums.
- `src/evaluation_SAS/integration.py`, `bootstrap.py`; `scripts/final_evaluation.py`, `sas_final_preflight.py`; active `configs/contract.yaml` and legacy `configs/contract.lock.json`.
- `docs/DELTA_DATA_HANDOFF.md`, `docs/DELTA_V2_RUN_EVIDENCE.json`, protocol/interfaces/ownership and course checklist; `submission_local/` report/slides/status/methodology.

Use `git show 4dffb0d:<path>` while local main remains behind. Companion `DATA245_LATEST_RESULTS.csv` contains full run IDs/paths/current commit and explicit verification scope. The earlier audit's scientific conclusions were retained only after matching blobs and rerunning available numerical checks.

Audit-only changes: two requested handoff updates plus mandatory `docs/prompts/2026-11-23-post-merge-update-audit.md`. Previous prompt preserved. CSV remains locally ignored by the existing rule; nothing staged or published.
