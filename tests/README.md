# Repository checks

Run `python3 scripts/verify_setup.py` for read-only artifact/schema/manifest/path/ignore checks. Run `python3 -m unittest discover -s tests -v` for migration path/output-safety and configuration/owner consistency checks. The latter uses PyYAML from `requirements.txt` and Python 3.11+ (`tomllib`).

These checks do not execute legacy scripts or notebook cells, generate features, fit models, or recompute inherited scores. Future timing/leakage/metric tests belong beside the actual implementations when authorized; no unimplemented model is reported as tested.
