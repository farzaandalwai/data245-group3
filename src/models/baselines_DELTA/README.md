# Baselines - DELTA

Persistence and prior-seven-day mean consume DELTA's approved lag/rolling inputs.
`common_reference` supplies one shared baseline per model. Pure `predictions`
operates on explicitly supplied tables; new `run_development` calls slice to
train/validation before prediction, require the trusted top-level manifest hash,
and reject final-purpose bundles before opening outcome tables.

New immutable runs use the existing SAS `2.0-development-1` manifest, with
source/environment hashes and `test_scored=false`. They are written atomically
outside input directories. Prior all-split baseline files are preserved as
historically exposed development evidence; `scripts.verify_delta_v2` can still
verify their original bytes in memory. No final baseline score is authorized.

See [DELTA handoff](../../../docs/DELTA_DATA_HANDOFF.md) and the
[readiness record](../../../docs/DELTA_DEVGRU_READINESS.md).
