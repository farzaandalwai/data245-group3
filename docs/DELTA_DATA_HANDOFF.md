# DELTA V2 data handoff

2026-11-19. **IMPLEMENTED / VERIFIED operationally** under producer contract `2.0.0`, scientific protocol `2.0`. **PROVISIONAL** for undocumented closed/missing-hour business semantics and exact export lineage. The broader experiment contract remains DRAFT; final test scoring is blocked. DEVGRU/SAS may build consumers now; human acceptance and frozen model/validation choices remain required before final evaluation.

## Authoritative local artifacts

All paths below are repository-relative, local and ignored. They will not arrive through Git. Obtain the exact bundle from DELTA through the team's approved file exchange and verify the manifest hash in [the run evidence](DELTA_V2_RUN_EVIDENCE.json). Do not independently rebuild data definitions.

| Purpose | Bundle directory | Train / validation / test | Series / stores / products |
| --- | --- | --- | --- |
| Development/debugging | `data/processed/feature_bundles/v2-development-200-r2` | 9,200 / 3,000 / 3,000 | 200 / 113 / 113 |
| Final inputs, scoring pending | `data/processed/feature_bundles/v2-final-1000-r2` | 46,000 / 15,000 / 15,000 | 1,000 / 183 / 239 |
| Synthetic test-only fixture | `data/processed/feature_bundles/v2-synthetic-fixture-r2` | 92 / 30 / 30 | 2 / 2 / 1 |

Actual counts equal the protocol expectations; zero additional selected-series quality exclusions. First 14 days are warmup (2,800 development / 14,000 final rows). No target is removed for stockout status. Final inputs are not a completed final experiment.

Each directory contains `observations.csv`, `features_sales_only.csv`, `features_stockout_aware.csv`, `evaluation_metadata.csv`, `sample_manifest.csv`, `eligibility_audit.csv`, `quality_report.json`, `feature_spec.json`, `configuration_snapshot.json`, and `bundle_manifest.json`. Bundles reject overwrite. Snapshots record configuration at generation time; later active metadata records completed run status and does not retroactively change snapshots.

## Loading and joins

From the repository root, using Python 3.12 and `requirements.txt`:

```python
from src.features_DELTA.bundle import load_bundle

tables, manifest = load_bundle(
    "data/processed/feature_bundles/v2-development-200-r2",
    # Supply expected_manifest_sha256 from docs/DELTA_V2_RUN_EVIDENCE.json
)
keys = ["store_id", "product_id", "dt"]
observations = tables["observations"]
features = tables["features_sales_only"]
joined = observations.merge(features, on=keys, validate="one_to_one")
assert len(joined) == len(observations) == len(features)
from src.features_DELTA.v2 import COMMON
train = joined["split"].eq("train")
X_train = joined.loc[train, COMMON]
y_train = joined.loc[train, "actual"]
```

The loader checks hashes, exact schemas, unique keys, full sample/calendar coverage, targets, splits, matched common features and metadata. Pin the top-level manifest hash from trusted handoff evidence: internal hashes alone are not an authenticity signature. Never silently inner-join away missing rows, use row-position joins across independently loaded data, or select all non-target columns as X.

CSV IDs are nonnegative `int64`; `dt` is ISO `YYYY-MM-DD`; actual/history predictors are finite numeric values serialized with 17 significant digits. `weekday` is Monday=0 through Sunday=6; `is_weekend` is Saturday/Sunday=1. No imputation or scaling occurs in the producer. Any learned-model transform must be fit on training only.

## Exact allowlists and timing

Sales only, in order: `sales_lag_1`, `sales_lag_2`, `sales_lag_3`, `sales_lag_7`, `sales_lag_14`, `sales_mean_7`, `sales_mean_14`, `weekday`, `is_weekend`.

Stockout aware: the same nine, then `stockout_hours_lag_1`, `stockout_hours_mean_7`, `stockout_hours_mean_14`, `stockout_day_fraction_7`, `stockout_day_fraction_14`.

Lag k reads t-k. Mean/fraction w reads t-w through t-1. Positive prior count defines a stockout day. All windows are within series and retain stockout history. Earlier observed validation/test days can supply history for later one-day forecasts without refitting. `feature_spec.json` records definitions, order, units, timing and types.

`actual` is the source's normalized recorded `sale_amount` on target date `dt`, with no second shift. Day 15 is 2024-04-11. Train ends 2024-05-26; validation is 2024-05-27 through 2024-06-10; test is 2024-06-11 through 2024-06-25. The protocol is the scientific authority.

Never use IDs, `actual`, raw `sale_amount`, `split`, inherited predictions, `hours_sale`, `hours_stock_status`, target-day stockout metadata or other unapproved source fields as predictors. Retrospective `evaluation_metadata.csv` contains keys, `target_stockout_hours`, and `target_stockout_group`; join only for evaluation after predictions.

## Semantics and sampling limits

The [publisher data dictionary](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md) describes stockout counts and globally scaled daily sales. The [pinned publisher implementation](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/exp/data/generate_data.py) uses 24 hourly entries, indices 6 through 21 and status 1 as stockout. Every local raw record reconciles with this count. `fully_stocked` means zero **annotated** stockout hours in [06:00,22:00); it does not establish unrestricted availability or latent demand. No missing/closed-hour sentinel was observed in required data; undocumented upstream handling remains provisional. The exact scaling coefficient and local export extraction lineage remain unknown.

Final selection ranks complete-series integer keys by SHA-256 of ASCII `v2|245|store_id|product_id`, breaks ties by numeric keys, takes the first 1,000, then serializes in numeric key order. No outcome-based strata or performance selection. Training-only stockout activity quantiles and population coverage are recorded in `quality_report.json`. Hash ranking avoids unstable small store/product strata. Eligibility over all 90 days is retrospective availability selection; coverage does not establish representativeness. The original 200-series manifest is byte-preserved.

## Commands

PowerShell, from repository root (use a fresh bundle/run ID on regeneration):

```powershell
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe scripts/verify_setup.py
.venv/Scripts/python.exe -m scripts.verify_delta_v2
.venv/Scripts/python.exe -m scripts.delta_v2 verify data/processed/feature_bundles/v2-development-200-r2
.venv/Scripts/python.exe -m scripts.delta_v2 verify data/processed/feature_bundles/v2-final-1000-r2
.venv/Scripts/python.exe -m scripts.delta_v2 build --purpose development_debugging --bundle-id v2-development-200-r3
.venv/Scripts/python.exe -m scripts.delta_v2 build --purpose final_experiment --bundle-id v2-final-1000-r3
.venv/Scripts/python.exe -m scripts.delta_v2 build --purpose synthetic_test_only --bundle-id v2-synthetic-fixture-r3
.venv/Scripts/python.exe -m scripts.delta_v2 baselines data/processed/feature_bundles/v2-development-200-r3 --run-id v2-development-baselines-r3
```

Generation needs `data/raw/freshretail.csv`: copy OLD `data/freshretail.csv` without moving/deleting it, or obtain DELTA's byte-identical local export. Verify 323,577,557 bytes and SHA-256 `6d956f6cab0094e794beb97872d9047d7c49469d35044930f5d8a96a307110b5`. Never substitute a fresh upstream download silently. The producer checks this registered identity. Bundle consumers do not need raw data.

## Prediction exchange and next work

Columns: `store_id,product_id,dt,actual,prediction,model,feature_set,split,run_id`. Finite numeric actual/prediction, ISO date, exact authoritative keys/actuals/splits; unique keys per model/condition/run. Learned conditions use `sales_only` and `stockout_aware`. Baselines use `common_reference` once each (`persistence`, `recent_avg_7`); there is no artificial stockout-aware baseline. Baselines are unmodified previous-day and previous-seven-day sales, with no clipping or fitting.

Development baseline predictions, metrics and run manifest: `results/baselines_DELTA/v2/v2-development-baselines-r2/`. Final baseline scoring is rejected by the CLI. SAS retains common evaluator ownership; DELTA's metric helper is limited to its baseline run.

DEVGRU/SAS can implement keyed loaders, train-only transforms, owned model adapters and prediction validation using the synthetic fixture or verified development inputs. Agree tuning budgets, preprocessing/prediction policy and uncertainty procedure, then freeze validation choices and acceptance before final scoring. No learned models were implemented here. No messages were sent to teammates; this shared handoff is the coordination artifact.

Do not mix `archive/original_pilot/`, `docs/history/contract_v1/`, `results/baselines_DELTA/inherited/`, legacy reproduction outputs, or OLD's stocked-only/secondary results into V2 runs. Prior pilot test exposure remains disclosed. Full provenance and checks: [implementation report](DELTA_V2_IMPLEMENTATION_REPORT.md).

Precision reconciliation: 54 canonical pilot sales floats differ from raw by at most 4.44e-16 due to legacy serialization. Development preserves canonical pilot values; final uses raw values. Keys/splits are identical on overlapping series; values agree within explicit 1e-12 tolerances. Each comparison uses one bundle, so model/condition targets are identical. r1 bundles are retained as superseded verification outputs; r2 records this tolerance explicitly and is authoritative.

Tested environment lock: `requirements-v2-tested.txt` (Python 3.12.10). Install with `python -m pip install -r requirements-v2-tested.txt` when exact local package versions are needed.
