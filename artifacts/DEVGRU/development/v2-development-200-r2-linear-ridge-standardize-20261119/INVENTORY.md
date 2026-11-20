# DEVGRU Original Development Artifact Inventory

Inventory date: 2026-11-20
Repository: `data245-group3`
Observed branch: `DEVGRU/linear-ridge-models`

## Scope and protections

This is an evidence inventory of the existing original development outputs. No prediction, model fitting, tuning, scoring, renaming, deletion, or regeneration was performed. The reserved final 1,000-series bundle was not opened or evaluated.

Original artifact directory:

`runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/`

Development bundle:

`v2-development-200-r2`

Trusted manifest SHA-256:

`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`

The development bundle manifest independently hashed to the trusted value above. The documented verification command passed with `train=9200`, `validation=3000`, and `test=3000` observations.

## Prediction artifacts

All four original prediction files were found. Each has the exact schema:

`store_id,product_id,dt,actual,prediction,model,feature_set,split,run_id`

Each contains 12,200 rows: 9,200 train and 3,000 validation. No file contains test rows. Keys are unique and actuals/predictions are finite.

| Model | Feature set | Relative path | Size (bytes) | SHA-256 | Run ID |
|---|---|---|---:|---|---|
| Linear Regression | `sales_only` | `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/linear_regression/sales_only.predictions.csv` | 1,840,299 | `fd2d1d1f30d2d1870f4b1fdb3ead9d1703ff3ed14d410f91e7de62ef440561d7` | `dev-v2-r2-linear-ridge-standardize-20261119-linear_regression-sales_only` |
| Linear Regression | `stockout_aware` | `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/linear_regression/stockout_aware.predictions.csv` | 1,938,142 | `4af534b8fcd8f150d998da99d925bdc1881cc128b46f9218abf720f37754495c` | `dev-v2-r2-linear-ridge-standardize-20261119-linear_regression-stockout_aware` |
| Ridge Regression | `sales_only` | `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/ridge_regression/sales_only.predictions.csv` | 1,816,003 | `aaf2b9be37f1ab28d2a54db089ed13ee65ef3daa865cdedd72f26336f2b3785a` | `dev-v2-r2-linear-ridge-standardize-20261119-ridge_regression-sales_only` |
| Ridge Regression | `stockout_aware` | `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/ridge_regression/stockout_aware.predictions.csv` | 1,913,754 | `54e1547aa462d15fd3d65e2b242a600eaf43f5dbd0401da8acf57438bad518df` | `dev-v2-r2-linear-ridge-standardize-20261119-ridge_regression-stockout_aware` |

## Supporting artifacts

| Artifact | Size (bytes) | SHA-256 | Finding |
|---|---:|---|---|
| `ridge_alpha_selection.csv` | 404 | `2b5d4b13a699a1ab3ce09b5f8f2a42613d069977fafa15a5b543079352dcbbb8` | Present; 10 candidate records. Selected alpha is 10.0 for `sales_only` and 100.0 for `stockout_aware`. |
| `validation_metrics.csv` | 931 | `7c1032be0b89ad26f5586b266d8aa8e9a6aaf55e9a80e9c1cee90bd69bccbce4` | Present; train and validation metrics for all four combinations. |
| `paired_validation_comparison.csv` | 611 | `63051e6a2bb4d6976f525eeba5e23288d05c3d6c499f910b5f3f598ccf427450` | Present; two paired bootstrap records, 2,000 repetitions and 200 series. |
| `run_metadata.json` | 5,580 | `563c5cbc0e6d31e780d622700c7054aa2dd5e91d2eaa93178837b03726fff713` | Present; enriched with four experiment records, paths, run IDs, metrics, bundle identity, and settings. |
| `development_report.md` | 2,732 | `ef50e38013d7e158351752cc890e74b99726ac831cc706ea0e052eb59ea56b4b` | Present; supporting development report. |

Metadata records standardization, development-validation-only status, no prediction postprocessing, Ridge candidates `[0.01, 0.1, 1.0, 10.0, 100.0]`, and selected alphas of 10.0 and 100.0. It records bootstrap seeds 245 and 246, 2,000 repetitions, and whole store-product series as the resampling unit.

## Requested artifacts not found

- Saved model files: none found. No `.pkl`, `.pickle`, `.joblib`, `.npz`, `.npy`, or other model binary exists under the original run directory.
- Separate bootstrap result file: none found. Bootstrap results are present in `paired_validation_comparison.csv`.
- Separate tuning log/file beyond the alpha-selection CSV: none found. Tuning evidence is present in `ridge_alpha_selection.csv`.
- Separate supporting log or manifest: none found. Bundle identity is recorded in `run_metadata.json`; the authoritative bundle manifest remains in the development bundle directory.

## Repository status and why outputs are absent from shared Git history

Observed Git status was clean apart from the existing warning for the inaccessible `.codex_tmp_verify/tmp8nioeec1` directory. The repository is on `DEVGRU/linear-ridge-models`, tracking its origin branch.

The outputs are not present as tracked repository files because `.gitignore` explicitly ignores `/runs/` and also ignores generated `*.csv` files. The original experiment directory is therefore local/ignored evidence rather than a committed artifact set. This inventory report is itself placed under `runs/DEVGRU/inventory/`, outside the original experiment directory and also ignored by the repository.

## Limitations

## Checksum correction

The original inventory recorded a malformed checksum for `paired_validation_comparison.csv`:

- Previous recorded value: `63051e6a2bb4d6976f525ee5ae23288d05c3d6c499f910b5f3f598ccf427450`
- Independently recalculated source and shared-copy value: `63051e6a2bb4d6976f525eeba5e23288d05c3d6c499f910b5f3f598ccf427450`

The source and shared CSV bytes were not changed. The run metadata and development report checksums independently match their source/shared files; their earlier reported mismatch was caused by comparison against the malformed inventory record, not by modified artifacts.

- The four prediction files and supporting artifacts are locally available and hashable, but are not tracked in the shared repository.
- No saved fitted model objects are available for later reload; reproducing models would require rerunning the development code, which was intentionally not done here.
- The original run directory has no independent manifest or log beyond its metadata/report files.
- This inventory verifies artifact structure and recorded provenance; it does not constitute final-bundle evaluation or final-test scoring.
