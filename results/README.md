# Inherited baseline evidence

`baseline_metrics.csv`, `baseline_predictions.csv`, and `data_audit.txt` were imported unchanged from Timothy Tran's handoff. They are not new runs. Source links, byte counts, times, and SHA-256 hashes are in [provenance](../docs/provenance.md).

Metrics have four rows: two models (`persistence`, `recent_avg_7`) across validation and test. Each row reports 3,000 observations. Predictions have 12,000 rows, unique by `(model, store_id, product_id, dt, split)`, using `sale_amount` as actual and `prediction` as forecast. The inherited schema predates the proposed feature-set/run contract and is intentionally preserved.

Setup checks schemas, key coverage, split counts, and agreement of prediction actuals with the imported pilot. It does not regenerate predictions or recompute metric values. The raw audit's counts remain inherited because the raw CSV was not downloaded or run.

Future matched eligible evaluations must use a separate versioned run destination, with acquisition instructions/hashes for bulky outputs. Never overwrite these originals with a new run. Other generated results are ignored by default; deliberately review any exception before committing it.
