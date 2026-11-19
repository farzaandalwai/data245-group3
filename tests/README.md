# Repository checks

Run `python3 scripts/verify_setup.py` for read-only artifact/schema/manifest/path/ignore checks. Run `python3 -m unittest discover -s tests -v` for migration path/output-safety and configuration/owner consistency checks. The latter uses PyYAML from `requirements.txt` and Python 3.11+ (`tomllib`).

These checks do not execute legacy scripts or notebook cells, generate features, fit models, or recompute inherited scores. Future timing/leakage/metric tests belong beside the actual implementations when authorized; no unimplemented model is reported as tested.

## Active V2 versus historical V1

`test_shared_contract.py` validates active V2 registration, draft gates, exact feature sets, samples/populations, day-15 boundary, splits, metric/ownership/tuning safeguards and safe parser/endpoints. It rejects duplicate YAML keys. Helpers in `scripts/audit_contract.py` do not build data/features or implement full eligibility; target-day stockout is absent from the history-only guard. Endpoints preserve historical semantics pending producer verification.

`test_historical_contract_v1.py` explicitly loads the unchanged historical audit with repository root, reproduces its read-only report in memory, checks original V1 eligibility and all four original lock entries, and verifies copied bytes/source attribution. V1 assertions never govern active V2. No report is regenerated on disk or scores computed. Copied historical Markdown links use the original source layout and are excluded from current-layout link checks; current navigation and snapshot hashes are checked separately.
