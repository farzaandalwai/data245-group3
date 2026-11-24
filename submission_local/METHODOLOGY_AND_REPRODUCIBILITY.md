# Methodology and reproducibility

Use the approved V2 next-day normalized recorded-sales target and identical keyed observations across conditions. All eligible target dates, including stockouts, remain included. Sales-only uses9 past/calendar features; aware adds5 past-stockout features. Target-day stockout is retrospective metadata, never a predictor. Final r2 contains1,000 complete series and46,000/15,000/15,000 train/validation/test rows.

The new verified final run is final-1000-attested-20261124T094349Z. Train-only standardization/fit, development-validation-selected Ridge alphas10/100 and Tree depth5/leaf5 were prospectively frozen. No final-validation reselection, clipping or test tuning; Random Forest excluded by scope. MAE primary; RMSE/bias secondary. Paired whole-store bootstrap pools sampled loss sums/counts,2,000 draws seed245,95% linear percentiles. See the original freeze and manifest in docs/FINAL_SUBMISSION_CHECKLIST.md.

Independent saved-prediction verification already passed. No rerun is needed. Reconciliation only checks existing hashes/document consistency. The former November20 run remains unverified, even though rounded point estimates agree.

DEVGRU/SAS acceptance is recorded through Timothy's November24 project-lead attestation, with their original dates/messages unverified. Historical test exposure, retrospective completeness selection, conditional fixed-model intervals, cross-store/shared-shock dependence and provisional export/normalization/hour semantics remain limitations. Stockout-day Linear/Ridge MAE worsens despite modest aggregate improvement. No latent demand or measured waste effect is claimed.
