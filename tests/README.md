# Repository checks

Run `python3 scripts/verify_setup.py` for read-only artifact/schema/manifest/path/ignore checks. Run `python3 -m unittest discover -s tests -v` for migration path/output-safety and configuration/owner consistency checks. The latter uses PyYAML from `requirements.txt` and Python 3.11+ (`tomllib`).

These checks do not execute legacy scripts or notebook cells, generate features, fit models, or recompute inherited scores. Future timing/leakage/metric tests belong beside the actual implementations when authorized; no unimplemented model is reported as tested.

The later shared-contract tests cover stockout-hour endpoints, safe binary parsing, the day-29/history-first eligibility boundary, reproduction of the recorded read-only pilot audit, locked definition/input hashes, paired allowlists, and disabled test/optional-model gates. They do not test unimplemented features/models or generate scores. See `docs/contract_freeze.md`.
