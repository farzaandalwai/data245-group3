# Presentation: Stockout-Aware Forecasting for Fresh Retail

## Slide 1 — Title

Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail.

Speaker note: We study recorded-sales prediction, not latent demand recovery.

## Slide 2 — Motivation and question

When a product is unavailable, low recorded sales may reflect stockout rather than low interest. Does adding past stockout history improve next-day recorded-sales forecasts beyond recent sales history?

## Slide 3 — Data and target

Fresh retail store-product-date observations; normalized recorded `sale_amount`; 200 development and 1,000 final complete series; 14-day history; day 15 onward eligible.

## Slide 4 — Two feature conditions

Sales-only: sales lags, rolling sales means, weekday, weekend. Stockout-aware: the same nine predictors plus lagged/rolling stockout hours and day fractions. Target-day stockout is evaluation metadata only.

## Slide 5 — Experimental controls

Train days 1–60, validation days 61–75, test days 76–90. Training-only preprocessing, validation-only selection, matched keys and actuals, no clipping, no test-based decisions.

## Slide 6 — Models and baselines

Linear Regression, Ridge Regression, Decision Tree; persistence and prior-seven-day mean baselines. Random Forest was optional and not retained in the final required comparison.

## Slide 7 — Final MAE

Linear: 0.378509 → 0.377354. Ridge: 0.378492 → 0.377191. Tree: 0.396510 → 0.397487. Lower is better.

## Slide 8 — Uncertainty

Paired store bootstrap, 2,000 replicates, seed 245. All aware-minus-sales-only intervals include zero. The evidence does not support a clear general improvement.

## Slide 9 — Subgroups and bias

Stockout-target rows have higher error. Linear models underpredict on average. These patterns describe recorded-sales forecasting and do not quantify unmet demand.

## Slide 10 — Limitations

Historical holdout exposure, retrospective complete-series selection, provisional export and hour semantics, and unverified normalization lineage. The holdout is not pristine confirmatory evidence.

## Slide 11 — Conclusion

Stockout-aware features produced small mixed changes: gains for linear models and a small tree loss, all statistically uncertain. The main contribution is a leakage-safe, reproducible comparison.

## Slide 12 — Reproducibility and questions

Point to `results/final_evaluation/v2/final-authorized-20261120-r1/`, `scripts/final_evaluation.py`, and `submission_local/README_SUBMISSION.md`.

Likely question: “Did you estimate lost sales?” Answer: No. The target is normalized recorded sales; latent demand and waste reduction were not measured.
