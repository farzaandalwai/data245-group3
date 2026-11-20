# DEVGRU development experiment report

Status: **DEVELOPMENT VALIDATION ONLY; PROVISIONAL WORKING SETTINGS**. These results are not final test evidence and do not claim team-wide technical-contract freeze.

## Run and input

- Run ID prefix: `dev-v2-r2-linear-ridge-standardize-20261119`
- Bundle: `v2-development-200-r2`
- Trusted manifest SHA-256: `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`
- Output root: ignored `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/`
- Preprocessing: standardization fit on training rows only.
- Ridge candidates: `[0.01, 0.1, 1.0, 10.0, 100.0]`; selection used validation MAE with smaller-alpha tie-breaking.
- Prediction postprocessing: none.
- Bootstrap: 2,000 percentile repetitions, whole store-product series, seeds 245 (Linear) and 246 (Ridge).

The development bundle contains 9,200 train, 3,000 validation, and 3,000 test observations. Only the 12,200 train/validation observations were predicted and reported.

## Executed combinations and run IDs

- Linear / `sales_only`: `dev-v2-r2-linear-ridge-standardize-20261119-linear_regression-sales_only`
- Linear / `stockout_aware`: `dev-v2-r2-linear-ridge-standardize-20261119-linear_regression-stockout_aware`
- Ridge / `sales_only`: `dev-v2-r2-linear-ridge-standardize-20261119-ridge_regression-sales_only`
- Ridge / `stockout_aware`: `dev-v2-r2-linear-ridge-standardize-20261119-ridge_regression-stockout_aware`

## Metrics

| Model | Feature set | Split | Rows | MAE | RMSE | Signed bias | Selected alpha |
|---|---|---:|---:|---:|---:|---:|---:|
| Linear | sales_only | train | 9,200 | 0.322844 | 0.504787 | 0.000000 | — |
| Linear | sales_only | validation | 3,000 | 0.334257 | 0.535999 | 0.003913 | — |
| Linear | stockout_aware | train | 9,200 | 0.318679 | 0.500161 | 0.000000 | — |
| Linear | stockout_aware | validation | 3,000 | 0.334190 | 0.532689 | -0.006326 | — |
| Ridge | sales_only | train | 9,200 | 0.322838 | 0.504790 | 0.000000 | 10.0 |
| Ridge | sales_only | validation | 3,000 | 0.334256 | 0.535890 | 0.003791 | 10.0 |
| Ridge | stockout_aware | train | 9,200 | 0.318674 | 0.500269 | 0.000000 | 100.0 |
| Ridge | stockout_aware | validation | 3,000 | 0.334119 | 0.531885 | -0.006927 | 100.0 |

## Ridge selection evidence

Validation MAE candidates were recorded in `ridge_alpha_selection.csv` for both feature conditions. Selected alpha was 10.0 for `sales_only` and 100.0 for `stockout_aware`.

## Paired validation comparison

The difference is defined as `MAE(stockout_aware) - MAE(sales_only)`; negative values favor stockout-aware forecasting.

| Model | MAE sales-only | MAE stockout-aware | Difference | 95% percentile CI | Resampled series |
|---|---:|---:|---:|---:|---:|
| Linear | 0.334257 | 0.334190 | -0.000066 | [-0.002323, 0.002157] | 200 |
| Ridge | 0.334256 | 0.334119 | -0.000137 | [-0.002290, 0.001933] | 200 |

These are development validation results under provisional settings. Both intervals include zero. The bootstrap resampled whole store-product series to preserve within-series dependence; the number of series is adequate for an exploratory development interval but does not establish final uncertainty or generalization.

## Limitations and next steps

The technical contract remains draft. Preprocessing, Ridge tuning budget/grid, postprocessing, validation policy, and uncertainty procedure remain pending team-wide confirmation by Shoury, Timothy, and Farzaan. No development test scoring was performed, the final 1,000-series bundle was not opened, and no final predictions or findings were generated.
