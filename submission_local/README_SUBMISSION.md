# DATA 245 Group 3 Submission Package

This package contains the verified final-evaluation evidence for **Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail**.

## Contents

- `report/final_report.md` — research report source.
- `presentation/slides.md` — slide-by-slide presentation and speaker notes.
- `METHODOLOGY_AND_REPRODUCIBILITY.md` — protocol and reproduction notes.
- `TECHNICAL_STATUS.md` — execution status and checks.
- `MODEL_COMPARISON.md` — development comparison evidence.
- `../results/final_evaluation/v2/final-authorized-20261120-r1/` — final predictions, metrics, subgroup results, paired intervals, per-store summaries, and manifest.

## Reproduction

Use Python 3.12.10 with the existing environment, then run:

```powershell
.\.venv\Scripts\python.exe -m scripts.verify_delta_v2
.\.venv\Scripts\python.exe -m scripts.sas_final_preflight
.\.venv\Scripts\python.exe -m scripts.final_evaluation --bundle data/processed/feature_bundles/v2-final-1000-r2 --output results/final_evaluation/v2/final-authorized-20261120-r1 --run-id final-authorized-20261120-r1
```

The final run ID already exists in this workspace; the evaluator refuses to overwrite it. Reproduce into a new run ID for a fresh run.

The raw dataset is intentionally not copied into this package. Raw lineage, normalization, missing/closed-hour semantics, retrospective completeness selection, and historical holdout exposure remain limitations.
