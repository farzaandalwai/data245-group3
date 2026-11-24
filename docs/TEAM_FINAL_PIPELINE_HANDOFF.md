# Team final pipeline handoff

Run `final-1000-attested-20261124T094349Z`; source base47f531f. Read this after the publication PR is merged and you pull current main. The final experiment already executed once; do not rerun it to prepare a demo or presentation. Git includes the existing implementations plus a PARTIAL small final-evidence mirror. It does not provide data-driven end-to-end reproducibility by itself.

## Fresh clone and environment
```text
git clone https://github.com/farzaandalwai/data245-group3.git
cd data245-group3
```
On an existing clean checkout, fetch/review then pull main after the publication PR is merged; preserve your own edits instead of blindly pulling into dirty work.

Use Python3.12 (the recorded execution used3.12.10). Create a project-local environment:
```text
python -m venv .venv
```
Activate with `.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux; thereafter `python` must resolve to that environment. Install the minimum scientific versions used by the verified final execution:
```text
python -m pip install --only-binary=:all: numpy==2.4.3 pandas==3.0.1 PyYAML==6.0.3 scikit-learn==1.9.0 scipy==1.18.1 joblib==1.6.0 threadpoolctl==3.6.0
python -m pip check
```
Pip resolves transitive dependencies; the run snapshots record the actual environment. Windows/Python3.12 execution was verified; another platform still needs fixture validation. Matplotlib is optional for separate figure exports, not needed for this inspection/demo. Do not install globally or assume the broader macOS requirements file is a verified Windows lock.

## Actual implemented pipeline
Raw `sale_amount`/hourly-stockout records -> DELTA validation and complete-series eligibility -> preserved development manifest or deterministic seeded SHA-256 final sampling -> past-only feature construction and chronological split labels -> baselines and train-only learned models -> keyed shared evaluation -> paired whole-store bootstrap -> immutable saved results.

- DELTA: `scripts/delta_v2.py`, `src/data_preprocessing_DELTA/v2.py`, `src/features_DELTA/v2.py` and `bundle.py`. Validate raw keys/calendar/hourly status, exclude incomplete series, no outcome-stratified selection. Final seed245; full-90-day completeness is retrospective availability selection.
- Features: grouped sales lags1/2/3/7/14 and prior7/14-day means, weekday/weekend. Aware adds prior-day stockout hours and prior7/14-day hour means/day fractions. All rolling histories are shifted before rolling. IDs are keys; target-day stockout is evaluation metadata only.
- Splits are assigned during feature construction, not a shuffled train_test_split: days1?60/61?75/76?90, retained targets day15 onward. Final1,000 series give46,000/15,000/15,000 rows; both conditions have identical keys/actuals/splits.
- Baselines: `src/models/baselines_DELTA/v2.py`: lag1 persistence and previous-seven-day mean.
- DEVGRU: `src/models/linear_regression_DEVGRU/{core,model,development,artifacts}.py`; Ridge in `src/models/ridge_regression_DEVGRU/model.py`. Fit scalers/models on train only; validation selected development Ridge alphas; no refit on validation/test. New development runs support the SAS prediction envelope and numeric fitted-state exports; missing old fitted objects are not reconstructed.
- SAS: `src/models/decision_tree_SAS/v2.py`, optional Forest under `src/models/random_forest_SAS/`; shared evaluation in `src/evaluation_SAS/`. The repaired final path is `scripts/sas_final_evaluation.py` plus `src/evaluation_SAS/final.py`. It uses frozen settings, exact coverage/actual/split checks and transactional new-directory publishing.
- Uncertainty: `src/evaluation_SAS/bootstrap.py` samples entire stores with replacement. Each draw divides total paired loss differences by total sampled rows, not an equal-weight mean of store means. 2,000 draws, PCG64 seed245, linear95% percentiles.

Source and interfaces: `docs/experiment_protocol.md`, `docs/interfaces.md`, `docs/DELTA_DATA_HANDOFF.md`. Frozen settings, source identities and attestation are in `docs/FINAL_FREEZE_20261124T094349Z.json` and the historical settings snapshot below. Code is already part of main; this publication does not change the ML implementation.

## Exact final settings and results
Linear: train-only standardization/OLS. Ridge: standardize; alpha10 sales/100 aware. Tree: squared_error, best splitter, seed245, depth5/leaf5 both conditions. Required baselines: persistence/recent_avg_7. Forest excluded. No clipping or final-validation reselection. MAE primary; RMSE and prediction-minus-actual bias secondary.

Open `docs/final_execution_evidence/final-1000-attested-20261124T094349Z/overall.csv` or `FINAL_VERIFIED_RESULTS.csv` for the eight test groups (15,000 rows each). Ridge-aware is best by MAE0.377191 and RMSE0.618490; bias-0.056262. `mae_difference_intervals.csv` includes validation AND test rows: filter split=test for final presentation. `subgroups.csv` and `per_store.csv` are saved diagnostics, not new model runs.

## Safe inspection and demo commands
From repository root in the environment:
```text
python -m scripts.delta_v2 --help
python -m src.models.linear_regression_DEVGRU.development --help
python -m scripts.sas_v2 --help
python -m scripts.sas_final_evaluation check
```
The last command is configuration-only and SHOULD exit2, ready=false, with main's gates closed. It is a successful safety demonstration, not a setup failure. No real final bundle is opened without --bundle.

Optional synthetic-only demonstration, not executed by this publication task:
```text
python -B -m unittest tests.test_sas_integration tests.test_sas_final -v
```
These tests create temporary toy data/models, not the real final cohort. They need the packages above and tracked Git evidence/history; they do not need raw data or ignored final bundles. The prior targeted check had26 passes. Do not describe fixture outputs as research results.

Verify the small package without fitting/scoring, using standard-library Python:
```text
python -c "from pathlib import Path; import hashlib; p=Path('docs/final_execution_evidence/final-1000-attested-20261124T094349Z'); pairs=[line.split('  ',1) for line in (p/'SHA256SUMS').read_text().splitlines()]; bad=[name for digest,name in pairs if not (p/name).is_file() or hashlib.sha256((p/name).read_bytes()).hexdigest()!=digest]; print('FAIL' if bad else 'PASS',bad); raise SystemExit(bool(bad))"
```
`SHA256SUMS` binds every other file in the prepared small directory, including its inventory; it intentionally does not hash itself. The original run_manifest.json still references predictions/per_series, which are absent from Git. A PASS for this ledger verifies the supplied small mirror, not the unavailable bulk payloads or an independently rerun experiment.

## Safe live demonstration sequence
1. Show source ownership and the split/feature code, without executing data builders.
2. Open `overall.csv` / verified results; show the run ID and manifest.
3. Show corrected test intervals and the stockout-day caveat (presentation guide).
4. Run the small-package checksum command; optionally show configuration-only check blocked.
5. If desired, run the synthetic fixture suite explicitly as a toy demonstration, keeping it separate from research evidence.

Never run `scripts.sas_final_evaluation run`, legacy `scripts.final_evaluation`, real-bundle model training commands or test evaluation for the presentation. Do not copy historical enabled snapshots into active configs or enable gates. The original freeze is historical acceptance of this completed run, not ongoing authorization. Main retains closed gates and proposed active settings; single-use enforcement is not implemented, so closed defaults matter.

## What Git does not supply
- Raw export `data/raw/freshretail.csv`, ignored DELTA bundle directories and final r2 input bundle. Obtain exact trusted identities from DELTA if needed for a separately authorized workflow. They are not needed to read results or run toy tests.
- Original final predictions.csv (76,348,581 bytes) and per_series.csv (3,020,569 bytes). Hashes and exact run ID are in `docs/final_execution_evidence/final-1000-attested-20261124T094349Z/ARCHIVE_INVENTORY.csv`. No shared URL exists yet; obtain from Timothy only after storage/access review and authorized upload.
- Original fitted model objects are not included; do not manufacture them. External report PDFs and presentation PPTX/PDFs are not generated automatically.

For an independently accessible immutable archive, the custodian must preserve the two named original files byte-for-byte, include original run_manifest.json plus ARCHIVE_INVENTORY.csv, record the archive-level hash and approved storage/access/retention policy, upload only after permission, then verify hashes after downloading from a separate teammate account. Publish the actual read-only location only after that verification. No archive upload or URL is claimed here. Raw data and credentials are excluded. A complete package must satisfy both the small ledger and original manifest's two bulk identities.

DEVGRU/SAS approvals are documented by Timothy's November24 lead attestation, not direct teammate messages; original contributor dates are unknown. Historical test exposure, retrospective selection, conditional fixed-model intervals and provisional business semantics remain limitations. The old November20 run remains historically unverified.
