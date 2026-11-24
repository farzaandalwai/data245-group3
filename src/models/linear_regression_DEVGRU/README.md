# Linear Regression - DEVGRU

IMPLEMENTED and saved DEVELOPMENT predictions independently verified. The NumPy
pooled OLS implementation fits training rows only. Explicit 9/14-column feature
allowlists exclude IDs, targets and retrospective stockout metadata. No clipping
or validation refit is applied. Original fitted-model state was not saved and is
not reconstructed by this task.

New development runs use `development.py` and the existing SAS
`2.0-development-1` envelope: root `predictions.csv`, `run_manifest.json`, a common
run ID across conditions, train/validation only, source hashes, selected settings
and environment. Flat per-condition CSVs and inspectable numeric `.model.json`
exports are also retained. `artifacts.model_from_state` restores those new states
without fitting; it checks feature order, dimensions and finite positive scaling.
These exports are not executable pickle files and grant no test-scoring authority.

New runs use SAS's unchanged approved whole-store, pooled-row-weighted validation
bootstrap (seed 245, 2,000 replicates). `_paired_bootstrap` remains a historical
series-method helper for old evidence; it is not used by the new runner.

Run `python -m scripts.verify_devgru` to validate the original saved development
package without fitting. Add `--final-inputs <existing-final-bundle>` for a
read-only compatibility check. It always distinguishes input compatibility from
joint authorization. Final-purpose training/prediction is rejected by the
DEVGRU development runner, and active V2 freeze gates remain false.

See [readiness record](../../../docs/DELTA_DEVGRU_READINESS.md), the
[protocol](../../../docs/experiment_protocol.md), and
[interfaces](../../../docs/interfaces.md). No real model was retrained by the
readiness task. Synthetic tests are not research results.
