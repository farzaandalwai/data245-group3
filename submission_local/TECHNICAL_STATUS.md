# Local Technical Status

Date: 2026-11-20. Worktree: `data245-execution` (detached HEAD), HEAD `99481e7c12a813c18446b4ba588fcc3dce969d1c`.

This is a local execution assessment only. No commit, push, pull, merge, rebase, branch creation, remote change, final-bundle access, final/test scoring, or experiment rerun was performed. Existing evidence was inspected without modification.

## Environment and evidence

- `.venv/Scripts/python.exe` is Python 3.12.10; verified imports are numpy 2.5.5, pandas 3.1.1, scikit-learn 1.9.1, and PyYAML 6.0.3. No packages were installed.
- `scripts/verify_setup.py`: PASS. It validated syntax, notebooks, pilot schemas, inherited baseline schemas/coverage/actuals, Markdown links, and ignore/retention rules; it did not fit or score models.
- The R3 harmonized package exists at `artifacts/SAS/development/harmonized-200-series-20261120-r3/` with validation comparison tables, audits, intervals, predictions, figures, README, and `PACKAGE_SHA256SUMS`.
- Original Decision Tree evidence exists at `artifacts/SAS/development/original-200-series-20261119/decision_tree/`; predictions have the canonical schema, 18,400 train rows, 6,000 validation rows, and zero test rows.
- Inherited DELTA baselines exist under `results/baselines_DELTA/inherited/`.
- DEVGRU development run and local DELTA r2 bundles are present. RF generated artifacts remain absent and the optional RF suite was runtime-inconclusive.

## Existing results reused

Existing R3 validation evidence reports MAE: Linear sales-only 0.334257, Linear stockout-aware 0.334190, Ridge sales-only 0.334256, Ridge stockout-aware 0.334119, Decision Tree sales-only 0.348255, Decision Tree stockout-aware 0.352070, persistence 0.417757, and previous-7-day mean 0.337380. Paired intervals include zero. These are not newly generated results.

## Checks and blockers

- `python -m scripts.verify_delta_v2`: PASS; raw identity, three bundles, sample selection, 10 rebuilt CSV hashes, source snapshots, and two baseline hashes.
- `pytest` DEVGRU regression tests: PASS, 11 tests and 17 subtests; added verifier hash test also passed.
- Decision Tree development run: PASS, new run `sas-tree-development-20261120-r2`.
- Final preflight: PASS, exit code 0, no final data opened by the preflight.
- Final authorized run: PASS, `results/final_evaluation/v2/final-authorized-20261120-r1`.
- `git diff --check`: PASS.

Status: **DEVELOPMENT AND FINAL RUN COMPLETE WITH DISCLOSED LIMITATIONS**. Random Forest remains optional and was not retained.
