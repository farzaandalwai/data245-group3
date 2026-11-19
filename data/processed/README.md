# Development pilot and V2 feature bundles — DELTA

`pilot_200_series.csv` is the exact inherited 18,000-row pilot. Do not overwrite it or sample a replacement. Canonical manifest/exclusions are in `data/manifests/`.

Verified operational V2 bundles live under `data/processed/feature_bundles/<bundle_id>/`; generated contents are ignored. The producer supplies matched target keys, ordered allowlists, hashes, eligibility provenance and split counts. See the handoff below for authoritative r2 paths and provisional business semantics.

The legacy script/notebook writes only to `data/processed/reproduction/`, not this canonical pilot. It has not been executed after migration.

The approved 1,000-series final input bundle is generated. Development/final purposes and manifests remain distinct. Primary 14-day features retain all eligible dates from day 15, including stockouts. Producer schemas are implemented; the broader model/evaluation freeze remains pending.

## DELTA V2 update - 2026-11-19

V2 immutable development/final/synthetic bundles now exist under `feature_bundles/`; canonical pilot bytes are unchanged. See [handoff](../../docs/DELTA_DATA_HANDOFF.md).
