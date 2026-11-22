# Does Sold Out Get Mistaken for Unpopular?
## Stockout-Aware Forecasting for Fresh Retail

### Abstract

This project tests whether historical stockout information improves next-day forecasting of normalized recorded sales beyond recent sales history. We compare sales-only and stockout-aware predictors on identical eligible store-product-date keys using Linear Regression, Ridge Regression, and Decision Tree Regression, with persistence and recent seven-day mean baselines. The approved design uses a 14-day past-only history window, chronological train/validation/test splits, validation-only selection, and MAE as the primary metric. In the authorized 1,000-series final run, stockout-aware features slightly improved Linear and Ridge MAE but slightly worsened Decision Tree MAE. All paired store-bootstrap intervals included zero, so the results do not establish a reliable improvement.

### Research question and scope

The target is normalized recorded `sale_amount` for `(store_id, product_id, dt)`. Recorded sales are not unrestricted latent demand, exact lost sales, revenue, kilograms of waste, or a causal sustainability outcome. The question is predictive: whether historical stockout information adds value for forecasting the recorded-sales quantity.

### Data and experimental design

The development sample contains 200 complete store-product series and the final sample contains 1,000. Features use 14 prior days; the first eligible target is day 15. Train, validation, and test are days 1–60, 61–75, and 76–90. The final bundle contains 46,000 training, 15,000 validation, and 15,000 test rows. All eligible target dates remain in the primary population, including target dates with stockouts.

`sales_only` contains five sales lags, two trailing sales means, weekday, and weekend status. `stockout_aware` adds lagged and trailing stockout-hour and stockout-day-fraction features. All historical predictors precede the target date. Target-day stockout is evaluation metadata only. IDs are join keys, not predictors.

### Models and controls

Linear and Ridge use training-only standardization with deterministic zero-variance handling and an unpenalized Ridge intercept. Ridge selection used validation MAE over `[0.01, 0.1, 1, 10, 100]`; the frozen development choices were alpha 10 for sales-only and 100 for stockout-aware. The Decision Tree used the 12-candidate grid of depths `[3, 5, 8, null]` and leaf sizes `[5, 20, 50]`; the selected final parameters were depth 5 and leaf size 5 for both conditions. No prediction clipping or validation refit was used. Random Forest was not retained as a required result because its optional test suite was runtime-inconclusive.

### Final results

| Model | Sales-only MAE | Stockout-aware MAE | Difference (aware − sales) | 95% paired store interval |
|---|---:|---:|---:|---:|
| Linear Regression | 0.378509 | 0.377354 | -0.001155 | [-0.001987, 0.000583] |
| Ridge Regression | 0.378492 | 0.377191 | -0.001301 | [-0.002138, 0.000420] |
| Decision Tree | 0.396510 | 0.397487 | +0.000977 | [-0.000110, 0.002185] |

The recent seven-day mean baseline had MAE 0.381992 and persistence had MAE 0.472728. Ridge was the best final model by MAE, narrowly ahead of Linear Regression. The stockout-aware condition improved the two linear models by approximately 0.31% and 0.34% relative MAE, but both intervals included zero. It worsened the tree by approximately 0.25%, also without a decisive interval.

### Subgroups and bias

Stockout-target rows were harder than fully stocked rows for every model. For example, Ridge sales-only MAE was 0.353003 on fully stocked targets and 0.412801 on stockout targets; Ridge stockout-aware MAE was 0.349039 and 0.415083 respectively. Final linear-model signed bias was negative, indicating average underprediction: -0.04490 for Ridge sales-only and -0.05626 for Ridge stockout-aware. These are descriptive predictive errors, not estimates of lost sales.

### Uncertainty and limitations

Uncertainty uses 2,000 paired store-cluster bootstrap replicates with seed 245 and the aware-minus-sales-only MAE direction. This conditions on the selected models and validation choices; it does not include tuning uncertainty and does not establish population representativeness. The historical pilot exposed the project to all-90-day completeness, and inherited baseline test results had previously been seen. The final holdout is therefore not pristine confirmatory evidence. Raw export lineage, normalization coefficient, and missing/closed-hour business semantics remain provisional. The retrospective stockout label indicates recorded stockout hours but does not prove unrestricted availability or quantify unmet demand.

### Conclusion

Under the approved controls, historical stockout features produced small mixed changes in recorded-sales forecasting: modest numerical gains for Linear and Ridge, and a small loss for the tree. Because all paired intervals included zero and the target is recorded sales rather than latent demand, the defensible conclusion is that this experiment does not provide clear evidence of a general stockout-aware forecasting advantage. It does show that stockout-aware features can be evaluated reproducibly without target leakage when common keys, splits, predictors, and tuning budgets are enforced.

### Reproducibility appendix

The final run is `results/final_evaluation/v2/final-authorized-20261120-r1/`. Its manifest records the bundle hash, frozen parameters, source revision, environment, output hashes, and limitations. The final evaluator is `scripts/final_evaluation.py`; the DELTA integrity verifier is `scripts/verify_delta_v2.py`.
