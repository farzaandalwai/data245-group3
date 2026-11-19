# Shared pilot and future feature bundles — DELTA

`pilot_200_series.csv` is the exact inherited 18,000-row pilot. Do not overwrite it or sample a replacement. Canonical manifest/exclusions are in `data/manifests/`.

Future verified feature bundles belong under `data/processed/feature_bundles/<bundle_id>/`; generated contents are ignored. Their producer must provide common sales-only/stockout-aware target keys, ordered allowlists, input hashes, eligibility/filter provenance, split counts, and acquisition/version instructions. No feature bundle exists yet. See `docs/interfaces.md` before implementation.

The legacy script/notebook writes only to `data/processed/reproduction/`, not this canonical pilot. It has not been executed after migration.
