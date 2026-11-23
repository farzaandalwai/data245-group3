# ORIGINAL SAS DEVELOPMENT evidence

Sixteen files under `decision_tree/` and `comparison/` are byte-identical copies
of the original real 200-series development run. They were not regenerated.
All hashes match the previously published `docs/SAS_INTEGRATION_EVIDENCE.json`.
The original ignored `results/` directories remain untouched. These are
train/validation artifacts; no test predictions or final-test evidence.

`decision_tree/` contains both-condition predictions (24,400 rows total),
train/validation metrics, selected parameters/all candidate scores, numeric
selected-tree JSON exports, bootstrap interval summaries and run/coverage metadata.
`comparison/` contains the original validation-only comparison, subgroup,
series/store and paired interval outputs with its original manifest.

`ORIGINALS_MANIFEST.json` records each original path and checksum. `SHA256SUMS`
also covers this package's new explanatory files. From this directory:

```sh
shasum -a 256 -c SHA256SUMS
```

The new comparison reader additionally reconstructs the original train/validation
predictions from saved numeric trees without fitting. No pickle/joblib objects
or per-replicate bootstrap draw arrays were saved originally; these are not
claimed as recovered. The seed/settings and summaries are present, and intervals
can be recomputed from original predictions in a separate output directory.

See [reproduction and integration handoff](../../../../docs/SAS_DEVELOPMENT_COMPARISON.md).
