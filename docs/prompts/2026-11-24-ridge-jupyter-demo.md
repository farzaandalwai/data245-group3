# Authorized Ridge notebook and Jupyter setup

User request received November 24, 2026 (America/Los_Angeles).
Owner/requester: DELTA / Timothytran109, authenticated against the context map.
Checkout: `main` at `b4df926`; fetched `origin/main` matches. Local work only;
no staging, commit, push, PR or publication. Existing unrelated edits stay intact.

## Scope recorded before implementation

Create `submission_local/demo/ml_pipeline.ipynb`, set up JupyterLab/ipykernel/
nbclient in the existing Python 3.12 matching environment, register
`DATA245 Ridge Demo (Python 3.12)`, and document exact setup/launch/check commands
in `submission_local/demo/README_JUPYTER.md`. This file preserves the substantive
request as required by AGENTS.md. Environment/setup/test scratch files stay in
the user's temporary directory. Keep the original script and joblib byte-identical.

Dependencies: existing `ml_pipeline.py` and its import-safe functions; trusted
3,810-byte joblib dictionary with fitted StandardScaler -> Ridge pipeline;
DELTA's feature source/specification and optional hash-pinned final r2 bundle;
approved V2 protocol, frozen final settings and published execution evidence.
New work is a submission demonstration of an existing reproduction, not a new
experiment or independent final result.

## Requested behavior and acceptance

- Inspect and record the existing Python/package versions. Prefer adding
  JupyterLab, ipykernel and nbclient to the matching temporary Python 3.12
  environment without changing NumPy, pandas, scikit-learn or joblib.
- Register the named kernel, start/check JupyterLab, and verify the kernel works.
- Produce a real, polished executable notebook with separate Markdown/code cells:
  overview/research question; imports/environment/paths; dataset/chronological
  splits; sales lags/rolling features; grouped shift-before-rolling leakage
  prevention; sales-only nine vs stockout-aware fourteen features; saved model
  and fitted scaler; authentic embedded prediction; readable result DataFrame;
  optional complete test evaluation; actual/predicted and MAE visualizations;
  results, limitations and conclusion.
- Reuse existing functions and the actual joblib structure, with one source of
  truth for feature engineering and inference. Do not double-scale, shell out
  to the CLI as the notebook implementation, or implement simplified features.
  Original script changes are permitted only if essential and import-safe;
  prefer retaining its exact bytes and CLI behavior.
- Run All must work without raw data, CLI arguments or edited Windows paths.
  Include optional DATA_BUNDLE_PATH configuration. When the external bundle is
  absent, skip only full evaluation/its plots with an informative message.
  Do not retrain by default, fabricate data or overwrite frozen outputs.
- Execute end to end in the registered kernel with nbclient/equivalent. Check
  both repository-root and notebook-directory working directories, with and
  without the external feature bundle. Verify prediction approximately
  1.241823058952, actual 0.9 and absolute error approximately 0.341823058952.
- If the approved bundle exists, recompute test MAE and compare within floating
  point tolerance with 0.37719137988468526. Keep the distinction between aggregate
  MAE agreement and unverified row-by-row identity to the missing original CSV.
- Test original CLI --demo and --build-model without replacing or retraining the
  existing artifact. Confirm hashes, fitted alpha=100, 14-feature ordering,
  training-only scaler and 46,000 fitted training rows remain unchanged.
- Deliver notebook/kernel, launch commands, execution results, changed files and
  pass/fail status. Do not stage, commit or publish anything.

Existing matching interpreter:
`%LOCALAPPDATA%\Temp\data245-ridge-demo-py312\Scripts\python.exe`.
Optional bundle:
`%USERPROFILE%\Downloads\data-20261124T182319Z-1-001\data\processed\feature_bundles\v2-final-1000-r2`.

Original preserved SHA-256:
- `ml_pipeline.py`: `2398245feafd8ddc7fc879e8c458cb3405ca155e56a7467960cceb7d3e47454a`
- `stockout_aware_ridge.joblib`: `50f6f3c8e7dbf6ce6c97508bf7fb0b69ba0ecaee1234ded10cf497bc0d84407c`
