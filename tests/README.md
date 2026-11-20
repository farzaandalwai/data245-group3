# Repository checks

Run `python3 scripts/verify_setup.py` for read-only artifact/schema/manifest/path/ignore checks. Run `python3 -m unittest discover -s tests -v` for migration path/output-safety and configuration/owner consistency checks. The latter uses PyYAML from `requirements.txt` and Python 3.11+ (`tomllib`).

Setup and historical checks do not execute legacy scripts/notebooks or recompute inherited scores. DELTA behavioral tests generate small synthetic features and baseline predictions in temporary locations. SAS behavioral tests fit small synthetic Decision Trees and score fixture predictions only. No real-data learned-model experiment runs as part of the suite. Real artifact reproduction is an explicit separate command below.

## Active V2 versus historical V1

`test_shared_contract.py` validates active V2 registration, draft gates, exact feature sets, samples/populations, day-15 boundary, splits, metric/ownership/tuning safeguards and safe parser/endpoints. It rejects duplicate YAML keys. Helpers in `scripts/audit_contract.py` do not build data/features or implement full eligibility; target-day stockout is absent from the history-only guard. The V2 producer now verifies the operational endpoint convention against every raw row; missing/closed-hour business semantics remain provisional.

`test_historical_contract_v1.py` explicitly loads the unchanged historical audit with repository root, reproduces its read-only report in memory, checks original V1 eligibility and all four original lock entries, and verifies copied bytes/source attribution. V1 assertions never govern active V2. No report is regenerated on disk or scores computed. Copied historical Markdown links use the original source layout and are excluded from current-layout link checks; current navigation and snapshot hashes are checked separately.

## DELTA V2 update - 2026-11-19

`test_delta_v2.py` adds behavioral validation, golden windows, temporal perturbations, sampling, integrity and baseline guards. Historical V1 tests remain unchanged. See [handoff](../docs/DELTA_DATA_HANDOFF.md).

For full local artifact reproduction (requires ignored raw/bundles), run `python -m scripts.verify_delta_v2`. It verifies real CSV byte reproducibility and development baselines without final scoring.

## SAS local consumers - 2026-11-19

`test_sas_v2.py` checks literal golden metrics, signed-bias/under/over denominators,
empty subgroups, zero relative-error denominator, full authoritative key coverage,
missing/extra/duplicate predictions, changed targets/splits, invalid numerics,
retrospective metadata, explicit model/condition coverage, train-only fitting,
identical tuning budgets, deterministic ties, absence of validation refits,
test/metadata perturbation invariance, JSON tree reconstruction, bundle pinning,
provenance/integrity rejection, immutable runs and transactional failure cleanup.
Integration combines SAS tree predictions with DELTA-compatible synthetic
baselines and checks only train/validation rows reach scoring. It never loads real
raw data, fits on final inputs, or produces research findings. Install SAS's
`scikit-learn` dependency from `requirements.txt`; the environment actually tested
is recorded in `requirements-sas-tested.txt`. See [SAS handoff](../docs/SAS_LOCAL_HANDOFF.md).

SAS bootstrap integration adds five tests (61 total; 26 SAS). Literal whole-store resampling checks pooled row weighting, interval direction/percentiles, matched keys, deterministic order/seed, insufficient-store/degenerate results and final/test rejection. Real development validation is a separate explicit CLI run, documented in [SAS integration](../docs/SAS_INTEGRATION.md); unit tests remain synthetic only.
