# Prediction handoff location

If a consolidated exchange directory is needed, use `<model>/<feature_set>/<run_id>/` beneath this directory, with a manifest pointing to the authoritative owner-specific run. Avoid independent duplicate copies that can diverge. No prediction producer or new prediction file exists here yet.

Follow `docs/interfaces.md`: unique series/date/model/feature-set/split keys within a run, actual, prediction, and run identifier; eligibility/feature provenance stays separate. Inherited predictions retain their original schema under `results/baselines_DELTA/inherited/`.

New runs must identify experiment version and development/final sample manifest; never mix the historical 200-series outputs with the pending 1,000-series final experiment. Producer/baseline schema is implemented; learned-model settings and overall experiment freeze remain pending.

## DELTA V2 update - 2026-11-19

V2 baseline exchange schema is implemented with `feature_set=common_reference`; final evaluation remains blocked. See [handoff](../../docs/DELTA_DATA_HANDOFF.md).
