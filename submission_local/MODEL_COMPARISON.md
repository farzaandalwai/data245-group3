# Development Model Comparison

This is a local summary of existing harmonized R3 development evidence. It is not a new experiment and is not final-test evidence.

| Model | Condition/reference | Validation rows | MAE | RMSE | Signed bias |
|---|---|---:|---:|---:|---:|
| Linear Regression | sales_only | 3,000 | 0.334257 | 0.535999 | 0.003913 |
| Linear Regression | stockout_aware | 3,000 | 0.334190 | 0.532689 | -0.006327 |
| Ridge Regression | sales_only | 3,000 | 0.334256 | 0.535890 | 0.003791 |
| Ridge Regression | stockout_aware | 3,000 | 0.334119 | 0.531885 | -0.006927 |
| Decision Tree | sales_only | 3,000 | 0.348255 | 0.576482 | 0.000631 |
| Decision Tree | stockout_aware | 3,000 | 0.352070 | 0.587695 | -0.011598 |
| Persistence | common reference | 3,000 | 0.417757 | 0.677441 | 0.002357 |
| Previous 7-day mean | common reference | 3,000 | 0.337380 | 0.551965 | -0.007276 |

Paired validation differences (stockout-aware minus sales-only) are Linear `-0.000066`, 95% CI `[-0.002462, 0.002373]`; Ridge `-0.000137`, 95% CI `[-0.002427, 0.002148]`; and Decision Tree `+0.003814`, 95% CI `[-0.003332, 0.013629]`. Each interval includes zero. The harmonized package used 2,000 paired whole-store bootstrap replicates with seed 245. These are validation-stage comparisons, not independent final confirmation.

The R3 package reports five model/reference entries. The separate Random Forest report is documentation-only in this worktree because generated artifacts are absent; its reported numbers are not treated as verified here. Interpretation is limited to recorded normalized sales forecasting, not causal effects, latent demand, lost sales, food-waste quantities, or sustainability outcomes.
