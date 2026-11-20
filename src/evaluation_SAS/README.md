# Evaluation, leakage audit, and integration — SAS

Status: implemented and checked on synthetic fixtures plus DELTA’s exact real development bundle. Final comparison remains pending. See [SAS handoff](../../docs/SAS_LOCAL_HANDOFF.md).

`v2.py` consumes standardized predictions plus authoritative observations and retrospective metadata. It rejects missing/extra/duplicate keys, changed actuals/splits, nonfinite predictions, missing feature conditions, mixed run IDs within a model and unexpected models. The caller explicitly lists expected models, so an absent model cannot silently disappear. Row order is irrelevant; no inner join can hide missing observations.

Reports include pooled, per-series and per-store MAE, RMSE, signed bias, mean under/overprediction and under/overprediction rates. Mean magnitudes use all rows as denominator. Both retrospective subgroups are always present; empty groups have n=0/undefined metrics. Relative paired MAE improvement is undefined when the sales-only MAE is zero. Subgroup outputs on development/synthetic inputs are debugging evidence, not the protocol's final test analysis. `bootstrap.py` implements the authorized development-only 95% paired store-cluster percentile interval for MAE(stockout-aware) minus MAE(sales-only), seed 245, 2,000 replicates. Whole stores retain all matched rows; each draw uses its own row denominator. Reports include store count, status and limitations; fewer than two stores gives undefined endpoints. See [integration method](../../docs/SAS_INTEGRATION.md).

`runs.py` verifies trusted bundle identity, protocol/purpose/sample/producer compatibility and artifact hashes. It accepts DELTA's existing V2 baseline run format (bundle hash binds its sample/producer) and the provisional learned-model development envelope below. Baseline test records may be structurally validated; the scoring path receives train/validation rows only. Final bundles and requested test scoring are rejected.

Run `python3 -m scripts.sas_v2 evaluate --help`. Supply one or more `--run` directories and all expected `--models`. Local comparisons under `results/comparisons_SAS/v2/<run_id>/` are immutable and record input manifest hashes, environment/source hashes, coverage and evidence status. No notebook/model internals or scikit-learn imports are required by the evaluation command.

## Provisional development run envelope

Each learned-model run directory contains `predictions.csv` with the exact shared column order and `run_manifest.json`. The latter supplies:

- `prediction_run_version: "2.0-development-1"`, `protocol_version: "2.0"`, `producer_contract_version: "2.0.0"`;
- `purpose`, `bundle_manifest_sha256`, `sample_sha256` matching the trusted input bundle;
- one `run_id`, an explicit `models` list, and `scored_splits` limited to train/validation; each learned model has both feature conditions and one run ID;
- `test_scored: false`, `policy`, `selected_parameters`, `source`, `environment`;
- `artifacts`, mapping local filenames to `{ "sha256": "...", "bytes": 123 }`, including `predictions.csv` and all registered outputs.

The CLI records these fields automatically for SAS. This envelope supports local integration; it does not freeze another owner's model policy or the final exchange contract. The [protocol](../../docs/experiment_protocol.md) and [interfaces](../../docs/interfaces.md) remain authoritative. Predictions and metadata are not proof of the producer's scientific correctness; human review remains required.
