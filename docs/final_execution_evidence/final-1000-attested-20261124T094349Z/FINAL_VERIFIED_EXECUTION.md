# Verified final execution — new prospective run
Status: **EXECUTED ONCE AND INDEPENDENTLY VERIFIED**. Run `final-1000-attested-20261124T094349Z`.
This is a new descriptive final evaluation, not recovery or retrospective authorization of the missing November 20 run.

## Authorization and freeze
Timothy Tran, authenticated as Timothytran109, explicitly authorized the exact final settings and provided a project-lead attestation dated 2026-11-24 that he had received DEVGRU/Shoury and SAS/Farzaan approval. Original teammate messages were unavailable. Their original approval dates remain unknown; no direct teammate signatures or independently verified original dates are claimed.

GitHub API confirmed DEVGRU PRs #5/#6 were authored by shoddy16 and SAS PR #11 by farzaandalwai. This establishes the project role/account association; public profiles did not provide full-name validation, and no independent full-name claim is made. DELTA's authenticated identity is Timothytran109.

Evidence: `A:\Projects\DATA 245\data245-group3-final-execution\docs\prompts\2026-11-24-project-lead-final-approval-attestation.txt` and the original request saved alongside it as `2026-11-24-final-freeze-execution-request.txt`.
Settings approval entries explicitly label DEVGRU/SAS `date` as project_lead_attestation_date, attested_by=Timothytran109, and contributor_original_approval_date=null. DELTA is direct_user_authorization.

The actual schema requires codename/GitHub/date entries and a freeze reference; it does not require original contributor dates or direct messages. Repository governance requires joint scientific acceptance but specifies no exclusive evidence medium. Timothy's explicit instruction accepts the accurately labeled lead-attestation mechanism. This interpretation is recorded in the freeze; no validator was changed or bypassed.

Freeze: `A:\Projects\DATA 245\data245-group3-final-execution\docs\FINAL_FREEZE_20261124T094349Z.json`.
Freeze SHA-256: `3ea15e5c990b52c169ba1da3f419fe74158b5439b742f216e7577814d8481e27`.
Prospectively recorded 2026-11-24 09:43:49 UTC, before execution.
Approved settings SHA-256: `e2c76bd8686b8434d1ed84f3b86fc10856e4a7b0a3efb8b322b29adb54e48479`.
The settings reference the freeze by path; the freeze hashes settings. Neither hashes itself, avoiding circular identities.

The three active V2 contract flags were enabled locally only after the genuine attestation and freeze were recorded. The V1 lock was neither used nor modified.

## Git, environment and settings
Source base: `47f531fdf551202662ad334636177fc5d7475163`, containing merged PR11 and PR12.
Branch/worktree: `DELTA/final-execution-readiness` / `A:\Projects\DATA 245\data245-group3-final-execution`.
Freeze/configuration edits remain uncommitted. The run manifest correctly records dirty=true. Exact source-file hashes are recorded in the freeze; consumer source/environment hashes are also registered in the run manifest. No executable source was modified for this run. Other worktrees and existing uncommitted changes were preserved.

Python 3.12.10; NumPy2.4.3, pandas3.0.1, sklearn1.9.0, SciPy1.18.1, PyYAML6.0.3, joblib1.6.0, threadpoolctl3.6.0. Existing interpreter:
`A:\Projects\DATA 245\data245-group3\.venv\sas-final-tests\Scripts\python.exe`.
pip check passed; no packages were installed for this execution task.

Final inputs: `A:\Projects\DATA 245\data245-group3\data\processed\feature_bundles\v2-final-1000-r2`.
Manifest SHA-256 `52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c`;
sample SHA-256 `830d30a1249f609ad3c95c37032d2e7b7f0d5671fc7ad8864ad8b5e31d1356e7`.
Bundle hash inventory, schemas and counts were verified before execution and again after execution; immutable inputs were not changed.
1,000 series; 46,000/15,000/15,000 train/validation/test rows; 9/14 ordered sales/aware predictors.

Frozen settings:
- Linear: train-only standardization and OLS; no validation refit.
- Ridge: train-only standardization; alpha10 sales / alpha100 aware.
- Tree: squared_error, best splitter, seed245, depth5/leaf5 both conditions.
- Persistence and previous-seven-day mean baselines; Random Forest excluded.
- Fit=train; no final-validation reselection or test tuning; no clipping.
- MAE primary; RMSE and signed prediction−actual bias secondary.
- 95% paired whole-store percentile bootstrap; pooled-row denominator; 2,000 PCG64 replicates seed245, linear quantiles.
Parameters were checked against saved DEVGRU run_metadata.json and SAS original-tree run_manifest.json, without reproducing development experiments.

## Checks and actual execution
Before enabling the real gates: **26/26 targeted tests passed** (15 integration, 11 final; 0 failures/errors/skips). This includes byte-preserving Windows checkouts, V2 blocking, pooled-row weighting and synthetic transactional output.
After freeze/gate recording and before scoring:
- `scripts.sas_final_preflight`: exit0, ready=true, blockers=[], final_data_opened=false.
- `scripts.sas_final_evaluation check --bundle <absolute-final-input-path>`: exit0, ready=true, blockers=[], final_data_opened=false.

Only the repaired `scripts.sas_final_evaluation run` entry point was used.
Started 2026-11-24 09:44:07.945996 UTC; finished 09:44:23.097470 UTC; exit0.
Exactly one real execution attempt; no retries, development-model retraining or post-test selection.
New destination was verified absent. Historical `final-authorized-20261120-r1` was neither overwritten nor relabeled.

Original output directory: `A:\Projects\DATA 245\data245-group3-final-execution\results\final_evaluation\v2\final-1000-attested-20261124T094349Z`.
Execution log:
`A:\Projects\DATA 245\data245-group3-final-execution\audit_handoff\final_execution\final-1000-attested-20261124T094349Z.log`.
The log captures command, timestamps, freeze identity, stdout/stderr and exit status. Original outputs were published transactionally and then read only.

## Independent verification from saved predictions — no refitting
All checks passed:
- 608,000 saved prediction rows: eight required model/condition/baseline groups, each with 76,000 exact input keys, actuals and split labels.
- Exactly 15,000 test rows per group; 183 test stores; no missing, extra or duplicate keys.
- All eight manifest-registered artifact byte sizes/SHA-256s verified; manifest settings, source, bundle, sample and environment identities matched the freeze/current files.
- Independent NumPy arithmetic reproduced MAE, RMSE, bias, mean under/overprediction and under/overprediction rates.
- Compared all columns in overall16, subgroups32, per_store2,928 and per_series16,000 rows (validation plus test), tolerance 1e-12.
- Independently paired conditions and recomputed MAE differences and relative improvements.
- Independently sampled complete stores with replacement from per-store loss sums/counts and reproduced all six validation/test interval endpoints. Stores contribute 15–240 rows; each draw uses its total row count, not equal weighting of store means.
- Retrospective test subgroup counts per group: fully_stocked8,606 + stockout6,394 =15,000. All subgroup metrics and coverage verified.

Predictions: 76,348,581 bytes; SHA-256 `49d08764862627a20bda16eba376d3f5026b007e539525581e5052cb335b1ce5`.
Run manifest SHA-256: `d596a1c5c84687bbb51480a69fa948a64b5815ff428dbd86e045fd87878e0730`.
Detailed check results are preserved in the local independent-verification JSON beside the execution log.

## Verified TEST results
N=15,000 each. Bias=prediction−actual. Full precision, run identity and source paths are in FINAL_VERIFIED_RESULTS.csv. Rankings are descriptive, not tests of differences between model families.

| MAE rank | Model | Condition | MAE | RMSE | Signed bias |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | ridge_regression | stockout_aware | 0.377191379885 | 0.618489608113 | -0.056261948151 |
| 2 | linear_regression | stockout_aware | 0.377354098799 | 0.618750038450 | -0.056463224406 |
| 3 | ridge_regression | sales_only | 0.378492485954 | 0.621292181447 | -0.044902793776 |
| 4 | linear_regression | sales_only | 0.378508977381 | 0.621318720445 | -0.044918036381 |
| 5 | recent_avg_7 | common_reference | 0.381991904762 | 0.632547244881 | -0.045068285714 |
| 6 | decision_tree | sales_only | 0.396510253756 | 0.679157468893 | -0.063417848488 |
| 7 | decision_tree | stockout_aware | 0.397487460648 | 0.680494020294 | -0.065409346116 |
| 8 | persistence | common_reference | 0.472728000000 | 0.786389894815 | -0.001726666667 |

**Stockout-aware Ridge has the lowest MAE and RMSE.** Persistence has the smallest absolute bias, with much worse MAE/RMSE.

### Paired TEST differences
Negative MAE difference favors stockout-aware. Relative improvement=100×(sales MAE−aware MAE)/sales MAE.

| Model | Aware−sales MAE | 95% lower | 95% upper | Relative MAE improvement |
| --- | ---: | ---: | ---: | ---: |
| linear_regression | -0.001154878581 | -0.002183659272 | -0.000134824602 | 0.305113% |
| ridge_regression | -0.001301106070 | -0.002301963340 | -0.000290025655 | 0.343760% |
| decision_tree | 0.000977206891 | 0.000054234535 | 0.001937705144 | -0.246452% |

Linear and Ridge show small overall MAE improvements; their corrected conditional intervals exclude zero below. Tree worsens; its interval excludes zero above. This is fixed-model, historically exposed-sample descriptive evidence, not pristine confirmatory inference or causal proof.
The aggregate improvement does not hold uniformly across subgroups: both linear models improve fully-stocked-date MAE while stockout-date MAE becomes worse. Include this qualification in the report.

## Comparison with existing claims
New point estimates round to the report's 0.377354 Linear-aware, 0.377191 Ridge-aware, 0.397487 Tree-aware, 0.381992 seven-day and 0.472728 persistence. This numerical consistency does **not** establish when/how the missing historical run occurred.

The old report gives intervals Linear[-0.001987,0.000583], Ridge[-0.002138,0.000420], Tree[-0.000110,0.002185], all spanning zero. They do not match the correctly pooled-row intervals above. Replace those intervals and the associated “all intervals include zero” conclusion for this newly identified run. Preserve the old claims as unverified historical evidence, not silently corrected original outputs.

## Limitations and remaining submission work
Retrospective 90-day completeness selection, earlier development/test exposure (including nine development/final series overlaps), unavailable original contributor approval messages/dates and the unverified historical run remain disclosed. Approval evidence is a lead attestation, not independently obtained direct teammate signatures. Intervals condition on frozen models/settings, assume independent stores, omit shared shocks, selection/refitting uncertainty and multiplicity adjustment. Target is normalized observed sales, not latent demand or measured food waste.

No further scoring or test-based tuning is needed. Next:
1. Update reports/slides to cite this new run and corrected intervals, subgroup caveat, bias and descriptive interpretation.
2. Human-review the local freeze/configuration/attestation record and original evidence package. Obtain separate publication authorization before commit/push/merge or artifact sharing.
3. Preserve this worktree/output/logs; bulk outputs are ignored by Git and are not automatically available to teammates. Share via a reviewed artifact package/archive with hashes; never include raw data or credentials.
4. Complete individual contribution statements and submission formatting without invented authorship or sustainability claims.

No commit, push or merge was performed.
