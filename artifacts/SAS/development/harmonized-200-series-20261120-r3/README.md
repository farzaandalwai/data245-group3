# DEVELOPMENT — harmonized comparison, not original run outputs

This separate evaluation consumes original SAS/DEVGRU predictions and DELTA's
exact development r2 bundle. It does not fit, retrain, retune or clip a model.
Original files are preserved. Five model families use identical 3,000 validation
rows / 113 stores. No final/test scoring occurred.

- `development_comparison.csv`: concise metrics, row/store counts and paired MAE
  differences/95% intervals (baseline intervals are undefined, not zero).
- `mae_difference_intervals.csv`: pooled aware-minus-sales differences, 2,000
  whole-store bootstrap replicates, seed 245; negative favors stockout-aware.
- `subgroups.csv`: retrospective fully-stocked/stockout subgroup errors/counts;
  subgroup intervals are not implied by the overall intervals.
- `per_series.csv`, `per_store.csv`, `paired_comparisons.csv`, `overall.csv`:
  detailed development summaries.
- `validation_baseline_predictions.csv`: newly materialized validation-only
  DELTA lag-1/mean-7 references from the exact accepted bundle, not a replacement
  for DELTA's original baseline run files (unavailable locally).
- `input_acceptance.json`: exact input pins, original-inventory discrepancies,
  in-memory run-ID mapping, original series-bootstrap reproduction and limitations.
- `comparison_manifest.json`: protocol/bundle/input commit, evaluator source and
  generated artifact hashes. `PACKAGE_SHA256SUMS` additionally includes this README.
- PNG/SVG figures: labeled DEVELOPMENT point estimates and paired intervals.

All three paired 95% intervals include zero. Small Linear/Ridge point improvements
and worse tree point performance are developmental, conditional on validation
selection, and do not establish a stockout-feature benefit or final finding.
See [handoff and commands](../../../../docs/SAS_DEVELOPMENT_COMPARISON.md).
