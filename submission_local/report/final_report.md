# Does Sold Out Get Mistaken for Unpopular?
## Stockout-Aware Forecasting for Fresh Retail

### Abstract

This project tests whether historical stockout information improves next-day forecasting of normalized recorded sales beyond recent sales history. We compare sales-only and stockout-aware predictors on identical eligible store-product-date keys using Linear Regression, Ridge Regression, and Decision Tree Regression, with persistence and recent seven-day mean baselines. The approved design uses a 14-day past-only history window, chronological train/validation/test splits, validation-only selection, and MAE as the primary metric. In the authorized 1,000-series final run, stockout-aware features slightly improved Linear and Ridge MAE but slightly worsened Decision Tree MAE. Correctly pooled-row paired store-bootstrap intervals exclude zero: below zero for Linear and Ridge, above zero for Tree. Improvements are modest and descriptive because the holdout was previously exposed.

### Research question and scope

The target is normalized recorded `sale_amount` for `(store_id, product_id, dt)`. Recorded sales are not unrestricted latent demand, exact lost sales, revenue, kilograms of waste, or a causal sustainability outcome. The question is predictive: whether historical stockout information adds value for forecasting the recorded-sales quantity.

### Data and experimental design

The development sample contains 200 complete store-product series and the final sample contains 1,000. Features use 14 prior days; the first eligible target is day 15. Train, validation, and test are days 1–60, 61–75, and 76–90. The final bundle contains 46,000 training, 15,000 validation, and 15,000 test rows. All eligible target dates remain in the primary population, including target dates with stockouts.

`sales_only` contains five sales lags, two trailing sales means, weekday, and weekend status. `stockout_aware` adds lagged and trailing stockout-hour and stockout-day-fraction features. All historical predictors precede the target date. Target-day stockout is evaluation metadata only. IDs are join keys, not predictors.

### Models and controls

Linear and Ridge use training-only standardization with deterministic zero-variance handling and an unpenalized Ridge intercept. Ridge selection used validation MAE over `[0.01, 0.1, 1, 10, 100]`; the frozen development choices were alpha 10 for sales-only and 100 for stockout-aware. The Decision Tree used the 12-candidate grid of depths `[3, 5, 8, null]` and leaf sizes `[5, 20, 50]`; the selected final parameters were depth 5 and leaf size 5 for both conditions. No prediction clipping or validation refit was used. Random Forest was explicitly excluded from this frozen final run; this is a scope decision, not a claim that its development tests failed.

### Final results

| Model | Sales-only MAE | Stockout-aware MAE | Difference (aware − sales) | 95% paired store interval |
|---|---:|---:|---:|---:|
| Linear Regression | 0.378509 | 0.377354 | -0.001155 | [-0.002183659272, -0.000134824602] |
| Ridge Regression | 0.378492 | 0.377191 | -0.001301 | [-0.002301963340, -0.000290025655] |
| Decision Tree | 0.396510 | 0.397487 | +0.000977 | [+0.000054234535, +0.001937705144] |

The recent seven-day mean baseline had MAE 0.381992 and persistence had MAE 0.472728. Ridge was the best final model by MAE, narrowly ahead of Linear Regression. Stockout-aware Ridge achieved test MAE 0.377191, RMSE 0.618490 and signed bias -0.056262; it ranked best by MAE and RMSE. Stockout features produced only modest aggregate MAE improvements: Linear 0.305113%, Ridge 0.343760%. Their conditional paired intervals lie below zero; the Tree interval lies above zero, indicating a small worsening. These are not between-model significance tests.

### Subgroups and bias

Stockout-target rows were harder than fully stocked rows for every model. For example, Ridge sales-only MAE was 0.353003 on fully stocked targets and 0.412801 on stockout targets; Ridge stockout-aware MAE was 0.349039 and 0.415083 respectively. Final linear-model signed bias was negative, indicating average underprediction: -0.04490 for Ridge sales-only and -0.05626 for Ridge stockout-aware. The aggregate Linear/Ridge gains are concentrated in fully stocked dates: stockout-day MAE worsens for both. Each model-condition has 8,606 fully stocked and 6,394 stockout test dates. These are descriptive predictive errors, not estimates of lost sales.

### Uncertainty and limitations

Uncertainty uses 2,000 paired whole-store bootstrap replicates across 183 stores with seed 245 and the aware-minus-sales-only MAE direction. Each draw pools loss sums and row counts across sampled complete stores; stores are not equally weighted by their mean losses. This conditions on the selected models and validation choices; it does not include tuning uncertainty and does not establish population representativeness. The historical pilot exposed the project to all-90-day completeness, and inherited baseline test results had previously been seen. The final holdout is therefore not pristine confirmatory evidence. Raw export lineage, normalization coefficient, and missing/closed-hour business semantics remain provisional. The retrospective stockout label indicates recorded stockout hours but does not prove unrestricted availability or quantify unmet demand.

### Conclusion

Under the approved controls, historical stockout features produced small mixed changes in recorded-sales forecasting: modest numerical gains for Linear and Ridge, and a small loss for the tree. Corrected conditional intervals support small aggregate Linear/Ridge improvements and a small Tree deterioration on this historically exposed sample. Stockout-day error worsens for the linear models, so a broad stockout-day or causal advantage is not established. It does show that stockout-aware features can be evaluated reproducibly without target leakage when common keys, splits, predictors, and tuning budgets are enforced.

### Reproducibility appendix

The independently verified new run is `final-1000-attested-20261124T094349Z`, source base `47f531fdf551202662ad334636177fc5d7475163`, executed November 24, 2026 at 01:44 PST. The repaired entry point was `scripts.sas_final_evaluation`; no rerun is needed. Final inputs are v2-final-1000-r2 (manifest SHA-256 `52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c`).

The prospective freeze records Timothy's direct DELTA authorization and his November 24 project-lead attestation that DEVGRU and SAS approved these settings. Their original approval messages/dates were not independently verified; no direct teammate signatures are claimed. This differs from the historically unverified November 20 identity `final-authorized-20261120-r1`; the new outputs are not its recovered files. Matching rounded point estimates do not establish historical execution provenance.

See `docs/FINAL_SUBMISSION_CHECKLIST.md` and `docs/final_execution_evidence/final-1000-attested-20261124T094349Z/PUBLICATION_INVENTORY.csv` for evidence hashes and storage. The prepared Git candidate is a partial evidence mirror only: obtain predictions and per-series diagnostics from the reviewed archive before claiming the entire package is shared. No causal food-waste reduction was measured.
