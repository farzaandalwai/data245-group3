# DEVELOPMENT — SAS Random Forest run `sas-forest-dev-200-r1`

Byte-identical copy of the local run made on 2026-11-20 from DELTA's exact development
r2 bundle (train fit, validation selection; no test rows fitted, predicted or scored).
`SHA256SUMS` covers the six run files; `run_manifest.json` SHA-256
`ba8696f1cc7e780dfee1141be0f4a3e58df547fab98c7e522469e78c92e45bc9` is the identity the
comparison accepts. No fitted forest file was saved (no executable pickle).

Settings are a development proposal (tree grid, seed 245, 200 trees,
`max_features=1.0`), not team-frozen. The manifest records an uncommitted working tree
with per-file source hashes; the code was committed afterwards in `eb93201`.
See [SAS Random Forest](../../../../docs/SAS_RANDOM_FOREST.md).
