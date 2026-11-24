# DEVELOPMENT — harmonized comparison r4 (adds Random Forest and relative MAE)

Same evaluator, bundle, rows and bootstrap as r3: DELTA's exact development r2 bundle,
3,000 matched validation rows / 200 series / 113 stores, 95% whole-store percentile
intervals, 2,000 replicates, seed 245. No model is fitted, retrained, retuned or clipped
here, and no final/test scoring occurred. r3 is preserved unchanged.

Changes from r3:
- Adds the shared SAS Random Forest run (`../random-forest-200-series-20261120/`).
- Adds `relative_MAE_improvement_pct` = 100 × (MAE sales-only − MAE stockout-aware) /
  MAE sales-only per learned model (point estimate only; negative means the stockout-aware
  condition is worse). Undefined for baselines.
- Uses the updated PR #6 pin at DEVGRU's correction commit `1f4e6a4`, where only
  `INVENTORY.md` changed. Two inventory entries (`development_report.md`,
  `run_metadata.json`) still differ from the published bytes; see `input_acceptance.json`.

Every r3 metric and interval is reproduced exactly. All four paired 95% intervals include
zero: no stockout-feature benefit is established. Files follow the r3 layout;
`PACKAGE_SHA256SUMS` includes this README. See
[handoff and commands](../../../../docs/SAS_DEVELOPMENT_COMPARISON.md).
