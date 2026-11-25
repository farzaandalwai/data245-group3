# Timothy / DELTA presentation EDA

Purpose: **original-export descriptive EDA only**, in the V2 project context.
These figures are not final-model results and do not change the November 24 experiment.

## Inputs and integrity

- Exact source: `C:\Users\timho\Downloads\data-20261124T182319Z-1-001\data\raw\freshretail.csv` (read only).
- SHA-256: `6d956f6cab0094e794beb97872d9047d7c49469d35044930f5d8a96a307110b5`; 323,577,557 bytes. Identity checked before and after analysis.
- Original export: **1,459,198 rows, 19 columns, 16,214 store-product series**, March 28–June 25, 2024.
- **16,213 complete 90-day series**, one 28-day series (store 420, product 764) with 62 absent dates.
- All 19 source columns checked: **zero missing values**. **Zero duplicate store-product-date keys**.
- Every 24-entry binary `hours_stock_status` vector reconciles with `stock_hour6_22_cnt` at indices [6:22].
- Count means annotated stockout hours in [06:00,22:00), with 1=stockout. Zero annotations do not prove unrestricted availability. Scaling coefficient, original export lineage and undocumented closed/missing-hour semantics remain provisional.
- Raw Figures 2–4 retain the 28 valid records of the incomplete series. They are not restricted to development or final samples.

## 01 — Sales versus stockout hours

`01_sales_vs_stockout_hours.png`: 90 real daily observations for store **196**, product **650**, March 28–June 25, 2024. Teal sales and orange annotated stockout hours use aligned panels with independent, explicit units.

Selection: consider complete series only; on the first 60 training dates require nonzero sales standard deviation and 1–59 positive-stockout dates. Rank the 16,172 qualifying series by SHA-256 of ASCII `eda|245|store_id|product_id`, break ties by numeric keys, choose the minimum. No sales-stockout correlation, apparent relationship, validation/test outcome or model score selects the example. The displayed full calendar includes validation/test dates for descriptive illustration, not tuning. There are **40 positive-stockout dates** in this example.

Presentation: “This is one deterministically selected, complete store-product timeline. Stockout annotations help motivate historical availability features, but this plot does not establish why sales changed.”

Limitation: illustrative, not representative; association cannot establish constrained latent demand or causality. Same-day annotations shown here are not approved model predictors.

## 02 — Distribution of stockout hours

`02_stockout_hours_distribution.png`: integer-centered histogram of daily annotated stockout hours, all 1,459,198 source rows. Vertical axis is percent of source records; all bins 0–16 are retained. **642,027 records (43.9986%)** have positive annotated hours.

Presentation: “Recorded stockout annotations occur on 44.0% of source records. The bars distinguish days with no annotated hours from short and longer annotated periods.”

Limitation: annotations describe the 16-hour operational interval, not exact unmet demand or independently verified business closures.

## 03 — Sales by availability annotation

`03_sales_by_stockout_status.png`: same all-export population, partitioned by zero versus positive annotated hours. Group sizes are **817,171** and **642,027**; medians are **0.700000** and **0.700000** normalized sales, respectively.

Detail uses the pooled sales 99th percentile (**5.800000**) as its axis limit; **13,974** larger values remain in every statistic and in the adjacent full-range view. Detail boxes use Q1/median/Q3, whiskers end at observed values within 1.5 IQR, and individual outlier dots are suppressed. Full-range boxes show observed min/max whiskers and all-data quartiles, on a symmetric-log axis that is linear through sales=1 and logarithmic above it. No values are deleted or winsorized. Original maxima: zero group **27.500000**, positive group **27.000000**.

Presentation: “The two annotation groups have different recorded-sales distributions. This pooled comparison mixes stores, products and dates, so it is descriptive rather than a causal stockout effect.”

## 04 — Daily stockout prevalence

`04_daily_stockout_prevalence.png`: for each of 90 dates, 100 × number of source rows with positive hours / all rows on that date. Denominators vary from **16,213 to 16,214** because the incomplete series remains included where observed. Daily prevalence ranges from **30.2042% (2024-05-24)** to **79.9494% (2024-04-08)**. Dashed reference is the row-weighted all-export prevalence, not a model prediction or fitted trend.

Presentation: “The share with recorded stockout hours changes over the 90-day calendar, between 30.2% and 79.9%. The chart documents that variation without attributing it to a particular cause.”

Limitation: daily pooled percentages do not track a guaranteed constant set of all raw series and do not control for common calendar effects.

## 05 — Validation and separate cohort selection

`05_dataset_validation_and_selection.png`: raw 16,214 series → 16,213 eligible complete series → **separate branches** to 200 development and 1,000 final. One incomplete 28-day series is excluded from complete-series eligibility; there is no exclusion solely for stockout status.

- Development: preserve the inherited canonical 200-series manifest. Historical source uses pandas `sample(n=200, random_state=245)` on complete series; this task verifies manifest identity rather than silently reselection under another environment.
- Final: SHA-256 rank of ASCII `v2|245|integer_store|integer_product`, ascending digest then numeric keys, first 1,000. Membership independently checked against the preserved final r2 manifest.
- Actual cohort overlap: **9 series**; membership is not guaranteed nested or disjoint.
- Split strip: first 14 days warm up history; retained targets give 46 train / 15 validation / 15 test dates per series. This corresponds to final **46,000 / 15,000 / 15,000** rows, distinct from raw-export EDA counts. No target rows or model predictions were regenerated.

Presentation: “We excluded one incomplete series, then used the preserved development cohort and a separately hash-ranked final cohort. Both follow the same chronological design and past-only feature contract.”

Limitation: eligibility based on all 90 dates is retrospective availability selection; neither cohort is claimed representative of the full dataset or wider retail population.

## Reproduce without overwriting

Interpreter used: `C:\Projects\data245-group3\presentation_assets\timothy_eda\.venv\Scripts\python.exe`. Exact installed packages are in `requirements-eda-freeze.txt`.

```powershell
& 'C:\Projects\data245-group3\presentation_assets\timothy_eda\.venv\Scripts\python.exe' -B 'C:\Projects\data245-group3\presentation_assets\timothy_eda\generate_eda.py' --input 'C:\Users\timho\Downloads\data-20261124T182319Z-1-001\data\raw\freshretail.csv' --data-root 'C:\Users\timho\Downloads\data-20261124T182319Z-1-001\data' --output-dir 'C:\Projects\data245-group3\presentation_assets\timothy_eda\regenerated_01'
```

The requested output folder must remain below `presentation_assets/timothy_eda`. The script refuses existing PNGs, README or summary; select a new child directory for a fresh rendering. No hidden download, model import, training, tuning or scoring occurs. Caches and the dedicated environment stay under this presentation-assets directory.

## Files and QA

Five 2560 × 1440 PNGs (16:9), `generate_eda.py`, this README, `eda_summary.json`, `requirements-eda-freeze.txt`, saved task request and workspace preservation evidence. JSON contains exact plotted summaries, input identities, selection rule, cohort hashes and figure hashes. Rendering verifies resolution and all text boundaries; separate visual review is recorded in `qa_report.json`.

Recommended two slides: **01** for feature-engineering motivation and **05** for DELTA validation/cohort/chronology responsibilities. No model-performance or sustainability outcome is inferred.
