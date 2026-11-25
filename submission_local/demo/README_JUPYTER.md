# DATA 245 Ridge notebook

For a different computer, use [the portable setup guide](../START_HERE.md) and
[requirements-demo.txt](requirements-demo.txt). The temporary paths below are
the original local setup/verification record, not prerequisites on your machine.

Verified November 24, 2026 (America/Los_Angeles). Submission demonstration of the
existing V2 reproduction, source experiment
`final-1000-attested-20261124T094349Z`. No new model training or parameter selection.
Owner/requester: DELTA / Timothytran109. Local checkout: `main` at `b4df926`.

## Launch for class

PowerShell:

```powershell
Set-Location C:\Projects\data245-group3
$py = "$env:LOCALAPPDATA\Temp\data245-ridge-demo-py312\Scripts\python.exe"
& $py -m jupyterlab --ServerApp.root_dir="C:\Projects\data245-group3" --ServerApp.default_url="/lab/tree/submission_local/demo/ml_pipeline.ipynb"
```

Select **DATA245 Ridge Demo (Python 3.12)** if prompted, then **Restart Kernel and
Run All Cells**. Stop the server with Ctrl+C in its terminal when finished.
The notebook discovers the repository from either its root or the demo directory.
The existing environment remains under `%LOCALAPPDATA%\Temp`; the registered
kernel points to this interpreter, so retain that directory for the demonstration.

The notebook has 26 cells, including 13 executable Python cells and the requested
12 teaching sections. It imports `ml_pipeline.py` without executing its CLI.
DELTA's actual feature-function excerpt and specification explain the feature
logic; no separate feature builder is introduced. `pipeline.predict()` applies
the saved scaler exactly once. No cell calls fit, fit_transform or build_model.

## Optional bundle

The default configuration checks both locations automatically:

- `data/processed/feature_bundles/v2-final-1000-r2` beneath the repository.
- `%USERPROFILE%\Downloads\data-20261124T182319Z-1-001\data\processed\feature_bundles\v2-final-1000-r2`.

You can set `DATA_BUNDLE_PATH` in the notebook configuration cell, or set
`DATA245_DEMO_BUNDLE` before starting JupyterLab. A missing bundle skips complete
test evaluation and its plots while retaining the authentic embedded example.
An existing bundle must pass the original script's pinned identity/coverage
checks. `RUN_COMPLETE_TEST_EVALUATION = False` explicitly selects embedded-only use.

Bundle manifest SHA-256:
`52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c`.

## Environment and setup commands

Original environment, unchanged: Python **3.12.10**, NumPy **2.4.3**, pandas
**3.0.1**, scikit-learn **1.9.0**, joblib **1.6.0**, SciPy **1.18.1**, PyYAML
**6.0.3**, threadpoolctl **3.6.0**. All **12 pre-existing package versions** were
compared before and after installation and stayed unchanged.

Added notebook/plot tools: JupyterLab **4.6.6**, ipykernel **7.4.0**, nbclient
**0.11.0**, nbformat **5.11.1**, Matplotlib **3.11.2**, and their dependencies.
`pip check` passed.

Installation used a constraints snapshot of every pre-existing package. These
PowerShell commands document/reproduce the setup in the existing environment:

```powershell
$py = "$env:LOCALAPPDATA\Temp\data245-ridge-demo-py312\Scripts\python.exe"
$setup = "$env:LOCALAPPDATA\Temp\data245-ridge-jupyter-setup"

# Existing pre-install snapshot, retained locally by this task:
Get-Content "$setup\constraints.txt"
& $py -m pip install --only-binary=:all: -c "$setup\constraints.txt" jupyterlab==4.6.6 ipykernel==7.4.0 nbclient==0.11.0 nbformat==5.11.1 matplotlib==3.11.2
& $py -m pip check
& $py -m ipykernel install --user --name data245-ridge-demo-py312 --display-name "DATA245 Ridge Demo (Python 3.12)"
& $py -m jupyter kernelspec list
```

Kernel registration:
`%APPDATA%\jupyter\kernels\data245-ridge-demo-py312\kernel.json`.
Its executable was checked against the matching interpreter above.

## Notebook execution and preservation checks

The delivered notebook includes real executed outputs from the repository-root
run, including an actual/predicted scatterplot for every test row and the 15-day
test trace for the embedded example's fixed store/product key. No data were
fabricated, no plots were generated when data were absent, and no raw dataset or
prediction CSV was copied into the demo directory.

Actual nbclient execution results in the named registered kernel:

- Repository root, default configuration, real approved bundle: **PASS**;
  13 code cells, zero errors, 18.53 seconds, one two-panel diagnostic figure.
- Notebook directory, deliberately unavailable external bundle, fitting methods
  patched to raise: **PASS**; all 13 notebook code cells plus one temporary test
  guard cell, zero errors, 10.99 seconds. Only full evaluation/plots skipped.
- Notebook directory, real approved bundle, fitting methods patched to raise:
  **PASS**; all 13 notebook code cells plus the temporary guard, zero errors,
  17.59 seconds, one two-panel diagnostic figure.

The temporary guards also prohibited NumPy least-squares training. They are test
instrumentation outside the delivered notebook. The plot was visually inspected.

Verified embedded example, store 0 / product 122 / 2024-06-11:

- Prediction: **1.241823058952** (displayed to 12 decimals).
- Actual recorded sales: **0.900000000000**.
- Absolute prediction error: **0.341823058952**.

Full test MAE: **0.37719137988468526** over **15,000** rows, matching the saved
full-precision final result with **zero difference**; tolerance was 1e-12.
The authentic embedded row was also matched back to its keyed bundle observation.
The original final-run prediction CSV remains unavailable: aggregate MAE
agreement does **not** prove row-by-row identity. The saved artifact is the
previously verified reproduction, not the missing original fitted model.

JupyterLab smoke test: **PASS**. A local authenticated server served the notebook
page (HTTP 200), exposed the named kernel, created it (HTTP 201), deleted the
test kernel (HTTP 204), and shut down gracefully. No test server was left running.

Both original CLI commands passed without retraining/replacing the existing model:

```powershell
Set-Location C:\Projects\data245-group3
$py = "$env:LOCALAPPDATA\Temp\data245-ridge-demo-py312\Scripts\python.exe"
& $py -B .\submission_local\demo\ml_pipeline.py --demo
& $py -B .\submission_local\demo\ml_pipeline.py --build-model
```

To repeat notebook execution without overwriting the delivered notebook:

```powershell
& $py -m nbconvert --to notebook --execute .\submission_local\demo\ml_pipeline.ipynb --ExecutePreprocessor.kernel_name=data245-ridge-demo-py312 --ExecutePreprocessor.timeout=180 --output ml_pipeline.recheck.ipynb --output-dir "$env:LOCALAPPDATA\Temp\data245-ridge-jupyter-setup"
```

This documented nbconvert recheck was also executed successfully (exit 0), writing
only its temporary output copy.

Detailed setup/execution snapshots and test-only notebooks are local under
`%LOCALAPPDATA%\Temp\data245-ridge-jupyter-setup\`; they are not submission artifacts.

## Preserved files and scope

The original files remain byte-for-byte identical:

- `ml_pipeline.py`: **17,087 bytes**, SHA-256
  `2398245feafd8ddc7fc879e8c458cb3405ca155e56a7467960cceb7d3e47454a`.
- `stockout_aware_ridge.joblib`: **3,810 bytes**, SHA-256
  `50f6f3c8e7dbf6ce6c97508bf7fb0b69ba0ecaee1234ded10cf497bc0d84407c`.

A before/after SHA-256 snapshot of **81 protected files**, including source,
configurations, archival evidence, existing results, final execution evidence,
script and model, passed. Existing unrelated workspace deletions/untracked files
were preserved. Nothing was staged, committed, pushed or published.

New repository files from this task:

- `submission_local/demo/ml_pipeline.ipynb`
- `submission_local/demo/README_JUPYTER.md`
- `docs/prompts/2026-11-24-ridge-jupyter-demo.md` (repository-required request record)

Scientific caveats remain unchanged: historical holdout exposure, retrospective
90-day completeness, limited population representativeness, recorded sales
rather than latent demand, and unresolved upstream export/business semantics.
