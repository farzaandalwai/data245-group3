# Run the presentation demo on another computer

Use a full checkout of this repository. The notebook imports the existing `src/`
code, so downloading only `submission_local` is insufficient. No private dataset
is needed for the authentic embedded prediction. The saved model is included.

## Windows PowerShell

Install **Python 3.12.10** first. The notebook verifies this exact Python version
and the scientific versions used to save the model. Open PowerShell and run:

```powershell
git clone --branch DELTA/share-submission-demo https://github.com/farzaandalwai/data245-group3.git
Set-Location data245-group3
py -3.12 -m venv .\submission_local\demo\.venv
$py = (Resolve-Path .\submission_local\demo\.venv\Scripts\python.exe).Path
& $py -m pip install --only-binary=:all: -r .\submission_local\demo\requirements-demo.txt
& $py -m pip check
& $py -m ipykernel install --user --name data245-ridge-demo-py312 --display-name "DATA245 Ridge Demo (Python 3.12)"
& $py -B .\submission_local\demo\ml_pipeline.py --demo
& $py -m jupyterlab --ServerApp.root_dir="$PWD" --ServerApp.default_url="/lab/tree/submission_local/demo/ml_pipeline.ipynb"
```

If you already cloned the project, fetch and check out
`origin/DELTA/share-submission-demo` in a clean checkout, preserving any local
work. Do not overwrite or reset your own edits. No merge into main is required
to use this shared branch.

In JupyterLab, select **DATA245 Ridge Demo (Python 3.12)** and choose **Restart
Kernel and Run All Cells**. The new `.venv` is local and ignored by Git; no
activation script or copied Windows environment is necessary. Reopen PowerShell
later by setting `$py` to the same resolved executable before the launch command.

## macOS / Linux

With Python **3.12.10** installed, use the same full checkout and pinned packages:

```bash
git clone --branch DELTA/share-submission-demo https://github.com/farzaandalwai/data245-group3.git
cd data245-group3
python3.12 -m venv submission_local/demo/.venv
submission_local/demo/.venv/bin/python -m pip install --only-binary=:all: -r submission_local/demo/requirements-demo.txt
submission_local/demo/.venv/bin/python -m pip check
submission_local/demo/.venv/bin/python -m ipykernel install --user --name data245-ridge-demo-py312 --display-name "DATA245 Ridge Demo (Python 3.12)"
submission_local/demo/.venv/bin/python -B submission_local/demo/ml_pipeline.py --demo
submission_local/demo/.venv/bin/python -m jupyterlab --ServerApp.root_dir="$PWD" --ServerApp.default_url="/lab/tree/submission_local/demo/ml_pipeline.ipynb"
```

Windows execution is verified. These are equivalent macOS/Linux commands;
platform-specific package installation and execution still need local verification.

## What to show

- `presentation/slides.md`: presentation source and speaker notes.
- `demo/ml_pipeline.ipynb`: executable walkthrough, explanations and saved plots.
- `demo/ml_pipeline.py --demo`: a quick saved-model inference check.
- `report/final_report.md`: report source. Existing exported PDF/PPTX files are
  separate; this repository contains the Markdown sources.

Expected embedded result: prediction **1.241823058952**, actual **0.9**, absolute
error **0.341823058952**. This does not retrain the model.

Without the optional approved `v2-final-1000-r2` bundle, Run All still completes
the example and skips only complete test evaluation and its plots. The committed
notebook retains previously executed plots. To recompute all 15,000 test rows,
obtain the exact approved bundle separately and set `DATA_BUNDLE_PATH` in its
configuration cell. No raw dataset or final prediction CSV is shipped here.

The saved reproduction's verified test MAE is **0.37719137988468526**. Matching
aggregate MAE does not establish row-by-row identity to the missing original
final-run prediction CSV. The model is the verified reproduction, not a recovered
original fitted object. Do not rerun model training or the final evaluator to
prepare the presentation.

## Integrity and previous verification

The unchanged script is 17,087 bytes, SHA-256
`2398245feafd8ddc7fc879e8c458cb3405ca155e56a7467960cceb7d3e47454a`.
The unchanged model is 3,810 bytes, SHA-256
`50f6f3c8e7dbf6ce6c97508bf7fb0b69ba0ecaee1234ded10cf497bc0d84407c`.
The notebook checks these hashes before use. Git attributes preserve these exact
bytes on new Windows checkouts. All 14 features and the fitted training-only
scaler remain inside the artifact.

See [the original local verification record](demo/README_JUPYTER.md) for the
earlier environment and execution checks. Its temporary paths describe Timothy's
machine; use the fresh-computer setup above on your own computer.
