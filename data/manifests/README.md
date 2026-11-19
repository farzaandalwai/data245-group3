# Fixed manifest and exclusions — DELTA

`pilot_series_manifest.csv` contains the exact inherited 200 selected pairs; `excluded_series.csv` records the original incomplete series. Their bytes/checksums match the archived handoff. Relocation did not resample or change data.

Do not regenerate these canonical files. The legacy reproduction runner uses the separate ignored `data/manifests/reproduction/` directory. Future eligibility keys and filter provenance belong to a versioned feature bundle rather than replacing the original sampling manifest.

The separate final 1,000-series manifest is GENERATED inside the immutable r2 final bundle. DELTA uses authorized seed 245 and SHA-256 key ranking without outcome-derived strata. Training-only coverage and source provenance are documented in the handoff. Historical manifests remain unchanged.

## DELTA V2 update - 2026-11-19

The final manifest is inside the final feature bundle, separate from historical manifests. See [handoff](../../docs/DELTA_DATA_HANDOFF.md).
