# Development pilot and future final feature bundles — DELTA

`pilot_200_series.csv` is the exact inherited 18,000-row pilot. Do not overwrite it or sample a replacement. Canonical manifest/exclusions are in `data/manifests/`.

Future verified feature bundles belong under `data/processed/feature_bundles/<bundle_id>/`; generated contents are ignored. Their producer must provide common sales-only/stockout-aware target keys, ordered allowlists, input hashes, eligibility/filter provenance, split counts, and acquisition/version instructions. No feature bundle exists yet. See `docs/interfaces.md` before implementation.

The legacy script/notebook writes only to `data/processed/reproduction/`, not this canonical pilot. It has not been executed after migration.

The approved final design uses 1,000 complete series, not yet selected/generated. Keep development and final bundles distinct, with experiment version and sample manifest. Primary 14-day features yield candidate targets from day 15 including all otherwise eligible stockout dates; exact contracts remain draft.
