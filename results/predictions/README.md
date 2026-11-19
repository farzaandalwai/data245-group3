# Prediction handoff location

If a consolidated exchange directory is needed, use `<model>/<feature_set>/<run_id>/` beneath this directory, with a manifest pointing to the authoritative owner-specific run. Avoid independent duplicate copies that can diverge. No prediction producer or new prediction file exists here yet.

Follow `docs/interfaces.md`: unique series/date/model/feature-set/split keys within a run, actual, prediction, and run identifier; eligibility/feature provenance stays separate. Inherited predictions retain their original schema under `results/baselines_DELTA/inherited/`.
