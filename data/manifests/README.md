# Fixed manifest and exclusions — DELTA

`pilot_series_manifest.csv` contains the exact inherited 200 selected pairs; `excluded_series.csv` records the original incomplete series. Their bytes/checksums match the archived handoff. Relocation did not resample or change data.

Do not regenerate these canonical files. The legacy reproduction runner uses the separate ignored `data/manifests/reproduction/` directory. Future eligibility keys and filter provenance belong to a versioned feature bundle rather than replacing the original sampling manifest.
