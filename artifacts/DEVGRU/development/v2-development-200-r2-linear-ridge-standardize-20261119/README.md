# DEVGRU Original Development Experiment Artifacts

This directory contains the original DEVGRU 200-series development experiment artifacts copied byte-for-byte from the local run directory. It is a development evidence package, not a final experiment package.

- Bundle ID: `v2-development-200-r2`
- Trusted manifest SHA-256: `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`
- Prediction coverage: train and validation only
- Each prediction CSV: 9,200 train rows and 3,000 validation rows
- Test predictions: zero
- Ridge alpha: `10.0` for `sales_only`; `100.0` for `stockout_aware`
- Bootstrap results: validation-stage paired comparisons only
- Serialized model files: none were saved

The package includes the original four prediction CSVs, Ridge alpha-selection evidence, validation metrics, paired validation bootstrap comparison, run metadata, development report, and the source inventory as `INVENTORY.md`.

These artifacts do not authorize evaluation of the reserved final 1,000-series bundle, final test scoring, or generation of final predictions.
