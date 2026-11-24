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

Paired whole-store bootstrap across 183 stores, pooled-row weighting, 2,000 replicates, seed245. Aware-minus-sales MAE 95% intervals: Linear [-0.002183659272,-0.000134824602]; Ridge [-0.002301963340,-0.000290025655]; Tree [+0.000054234535,+0.001937705144]. These conditional intervals exclude zero; the historically exposed evaluation remains descriptive.

## Slide 9 — Subgroups and bias

Stockout-target rows have higher error. The modest aggregate Linear/Ridge gains come from fully stocked dates; stockout-day MAE worsens for both. Ridge stockout-day MAE: 0.412801 sales-only to 0.415083 aware. Linear models underpredict on average. These patterns describe recorded-sales forecasting and do not quantify unmet demand.

## Slide 10 — Limitations

Historical holdout exposure, retrospective complete-series selection, provisional export and hour semantics, and unverified normalization lineage. DEVGRU/SAS acceptance is documented through Timothy's November24 project-lead attestation; original contributor dates/messages remain unverified. The holdout is not pristine confirmatory evidence.

## Slide 11 — Conclusion

Ridge-aware is best by test MAE (0.377191) and RMSE (0.618490). Stockout features give only modest aggregate gains: Ridge 0.343760%, Linear 0.305113%; Tree worsens 0.246452%. Conditional intervals exclude zero, but no pristine-holdout or causal food-waste claim is warranted.

## Slide 12 — Reproducibility and questions

New verified run: `final-1000-attested-20261124T094349Z`, November24 2026, source47f531f, repaired `scripts.sas_final_evaluation`. See `docs/FINAL_SUBMISSION_CHECKLIST.md` for preserved evidence and separate bulk storage. The November20 run remains historically unverified; these are not recovered November20 outputs. Do not rerun scoring.

Likely question: “Did you estimate lost sales?” Answer: No. The target is normalized recorded sales; latent demand and waste reduction were not measured.
