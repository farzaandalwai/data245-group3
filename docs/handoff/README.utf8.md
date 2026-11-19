# DATA 245 Project – Data Preparation and Baseline Handoff

## Project

**Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail**

This README documents the data-preparation and baseline portion completed by **Timothy Tran** and explains how the rest of the team should build on these outputs.

The goal of the full project is to test whether **historical stockout information improves next-day normalized sales forecasting** compared with using recent sales history alone.

The downstream experiment should remain a controlled comparison:

1. Sales-only historical features
2. The same features plus historical stockout-aware features

The target rows, series, train/validation/test periods, models, and evaluation metrics should remain matched between the two conditions.

---

# 1. Timothy's Assigned Responsibility

My assigned portion of the project is:

- Dataset preparation
- Data validation
- Pilot subset construction
- Chronological ordering and splitting
- Simple forecasting baselines
- Baseline evaluation

This portion is complete for the current 200-series pilot.

I did **not** implement the group's Linear Regression, Ridge Regression, Decision Tree, Random Forest, stockout-feature comparison, or final integration/evaluation.

---

# 2. Source Dataset

The local project uses the FreshRetailNet-50K training data.

Local source file:

`data/freshretail.csv`

Verified characteristics of the local CSV:

- 1,459,198 rows
- 19 columns
- Date column: `dt`
- Date range: 2024-03-28 through 2024-06-25
- 90 distinct dates
- 16,214 unique `(store_id, product_id)` series
- 16,213 complete 90-day series
- 1 incomplete 28-day series
- 0 null values
- 0 duplicate `(store_id, product_id, dt)` records

Important:

This local CSV is a subset/export of the broader published FreshRetailNet-50K dataset. Do not describe these local counts as the full published dataset size.

---

# 3. Complete-Series Filtering

The preprocessing pipeline does not define completeness only as `row_count == 90`.

A series is considered complete only if it contains the full expected 90-day calendar from:

`2024-03-28` through `2024-06-25`

The single incomplete series was excluded.

Excluded series:

- `store_id = 420`
- `product_id = 764`
- 28 rows

Details are saved in:

`data/processed/excluded_series.csv`

---

# 4. Pilot Dataset

A reproducible pilot subset was created from the complete-series pool.

Configuration:

- Number of selected series: 200
- Days per series: 90
- Total rows: 18,000
- Random seed: `245`
- Sampling level: store-product series, not individual rows

The selected series are recorded in:

`data/processed/pilot_series_manifest.csv`

The actual pilot dataset is:

`data/processed/pilot_200_series.csv`

This file should be treated as the **shared pilot input for downstream modeling**.

The 200-series dataset is a development and comparison subset of the larger local dataset. It is not the full FreshRetailNet-50K dataset.

---

# 5. Chronological Split

All 200 pilot series use the same chronological split.

## Train

- Days 1–60
- 2024-03-28 through 2024-05-26
- 12,000 rows

## Validation

- Days 61–75
- 2024-05-27 through 2024-06-10
- 3,000 rows

## Test

- Days 76–90
- 2024-06-11 through 2024-06-25
- 3,000 rows

There is no random train/test shuffling.

The split labels already exist in the prepared pilot data.

Downstream models should reuse these split assignments instead of generating new random splits.

---

# 6. Baseline Models

Two simple sales-only forecasting baselines were implemented.

## Persistence baseline

For each store-product series:

`prediction at day t = sale_amount at day t-1`

Prediction column:

`pred_persistence`

## 7-day recent-average baseline

For each store-product series:

`prediction at day t = mean sale_amount from days t-7 through t-1`

Prediction column:

`pred_recent_avg_7`

The target day is excluded from the rolling mean.

Both baselines are calculated independently within each store-product series, so there is no cross-series contamination.

---

# 7. Evaluation Metrics

The baseline models use:

## MAE

`mean(abs(predicted - actual))`

## RMSE

`sqrt(mean((predicted - actual)^2))`

## Signed Forecast Bias

`mean(predicted - actual)`

Interpretation:

- Positive bias = overprediction
- Negative bias = underprediction

Metrics are reported separately for validation and test data.

---

# 8. Baseline Results

| Model | Split | N | MAE | RMSE | Bias |
|---|---|---:|---:|---:|---:|
| Persistence | Validation | 3,000 | 0.417757 | 0.677441 | 0.002357 |
| Persistence | Test | 3,000 | 0.444063 | 0.697380 | -0.002777 |
| 7-day recent average | Validation | 3,000 | 0.337380 | 0.551965 | -0.007276 |
| 7-day recent average | Test | 3,000 | 0.362622 | 0.564407 | -0.051647 |

The 7-day recent-average baseline has lower MAE and RMSE than persistence on both validation and test data.

However, these results **do not answer the main project research question**.

They only establish baseline forecast performance before the group compares sales-only and stockout-aware machine-learning models.

---

# 9. Leakage Prevention in My Portion

The baseline pipeline uses the following safeguards:

- Each series is sorted by `store_id`, `product_id`, and `dt`
- Persistence only uses the previous day's sales
- The 7-day average only uses prior days
- The target day is excluded from rolling calculations
- Train, validation, and test sets are chronological
- No random train/test split is used
- Sampling is reproducible with seed 245
- Every pilot series uses the same calendar boundaries

This should not be described as the project's formal leakage audit.

Formal experiment-wide leakage checking and integration are assigned to Farzaan.

---

# 10. Files in This Handoff

## Code

### `prepare_and_baselines.py`

Reproducible script version of the data-preparation and baseline pipeline.

### `prepare_and_baselines.ipynb`

Readable notebook version showing the methodology, checks, outputs, and baseline results.

The script and notebook implement the same core workflow.

---

## Processed Data

### `pilot_200_series.csv`

Primary downstream modeling input.

Contains the 200 selected complete series and chronological split assignments.

### `pilot_series_manifest.csv`

Exact `(store_id, product_id)` pairs selected using random seed 245.

### `excluded_series.csv`

Documents the incomplete series removed before pilot sampling.

---

## Results

### `baseline_predictions.csv`

Row-level persistence and 7-day recent-average predictions.

### `baseline_metrics.csv`

Summary MAE, RMSE, and signed bias values.

### `data_audit.txt`

Validation summary for the local source data.

---

# 11. Important Rules for Downstream Modeling

The following should remain fixed unless the group explicitly agrees to change the experimental design.

## Keep fixed

- The same 200 pilot series
- The same selected rows
- The same chronological split
- The same target variable
- The same evaluation periods
- The same metric definitions

## For the controlled comparison

The sales-only and stockout-aware models should use:

- identical target rows
- identical train/validation/test periods
- identical model families
- identical evaluation metrics

The only intended difference should be the addition of historical stockout-related features.

If one condition drops different rows than the other, the comparison may no longer isolate the value of stockout information.

---

# 12. Recommended Downstream Feature Design

The project design discussed so far uses recent historical sales as the base feature set.

Possible sales-only features include:

- previous-day sales
- recent lagged sales
- recent rolling sales averages
- calendar features known before the forecast date

The stockout-aware version should add historical availability information such as:

- previous-day stockout-hour count
- recent average stockout hours
- proportion of recent days with any stockout

Only historical information should be used.

Do not use target-day stockout information as a predictor.

---

# 13. Team Responsibility Handoff

## Timothy Tran

Completed:

- Dataset preparation
- Pilot selection
- Baselines
- Baseline metrics

## Mansi

Next work:

- Stockout-related feature engineering
- Historical availability comparisons

Mansi should begin from:

`pilot_200_series.csv`

and preserve the existing rows and split labels.

## Shoury Ambarish Parab

Next work:

- Linear Regression
- Regularized linear models such as Ridge

Models should be run on matched sales-only and stockout-aware feature sets.

## Denisha Tank

Next work:

- Decision Tree Regression
- Random Forest extension

Models should use the same split and matched feature tables.

## Farzaan Dalwai

Next work:

- Experiment integration
- Chronological evaluation
- Formal leakage checks
- Error and bias analysis
- Final comparison across model families

---

# 14. Instructions for Codex / AI Coding Agents

If using Codex or another coding assistant for the next stages, provide it this README and tell it to treat the existing prepared pilot as the source of truth.

The agent should:

1. Inspect the current schema before making changes.
2. Preserve the 200 selected series.
3. Preserve the existing split labels.
4. Never use future observations to construct historical features.
5. Never use target-day stockout information as an input unless the experiment is explicitly redesigned.
6. Build sales-only and stockout-aware feature tables from the same eligible rows.
7. Avoid changing Timothy's preparation files unless a verified bug is found.
8. Save new outputs separately rather than overwriting the baseline outputs.
9. Document all feature definitions.
10. Report any assumption or inconsistency before changing the experiment design.

---

# 15. Recommended Output Organization for the Remaining Team

Suggested structure:

```text
data/
    processed/
        pilot_200_series.csv
        pilot_series_manifest.csv
        excluded_series.csv

features/
    sales_only_features.csv
    stockout_aware_features.csv

models/
    linear_regression/
    ridge/
    decision_tree/
    random_forest/

results/
    baseline_predictions.csv
    baseline_metrics.csv
    linear_results.csv
    tree_results.csv
    final_comparison.csv
```

Exact folder names can change, but outputs from different members should not overwrite one another.

---

# 16. What Not to Change Without Discussion

Do not casually change:

- random seed 245
- the 200 selected series
- train/validation/test dates
- target definition
- bias formula
- baseline definitions
- row eligibility between comparison groups

If the team decides to change any of these, document the change and regenerate all affected results consistently.

---

# 17. Current Project Status

Timothy's data-preparation and baseline portion is complete for the current pilot.

The next major technical question is:

**Do matched forecasting models perform better when historical stockout information is added to recent sales history?**

The downstream feature engineering, regression/tree modeling, and final integrated evaluation should build directly from the prepared pilot dataset in this handoff.
