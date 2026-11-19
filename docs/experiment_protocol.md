# Fixed experiment protocol

Status: documented on 2026-11-18 (America/Los_Angeles); remaining feature/model work is not implemented. The next contract task must resolve the explicitly pending semantics below before modeling. Protocol changes require an explicit, versioned decision and consistent regeneration of affected evidence.

## Question, target, and pilot

Does adding historical stockout information improve next-day **recorded normalized sales** forecasts beyond recent sales history, with everything else held matched? Predict `sale_amount` for each `(store_id, product_id, dt)`. Do not equate this target to unrestricted latent demand, mass, revenue, or food waste.

Reuse `data/manifests/pilot_series_manifest.csv` exactly: 200 complete series selected with seed 245, totaling 18,000 pilot rows across 90 dates. Do not resample, even with the same seed, or substitute the full upstream dataset for the inherited local export.

Fixed boundaries, before history and eligibility filters:

- Train: days 1–60, 2024-03-28 through 2024-05-26, 12,000 rows.
- Validation: days 61–75, 2024-05-27 through 2024-06-10, 3,000 rows.
- Test: days 76–90, 2024-06-11 through 2024-06-25, 3,000 rows.

The inherited raw-export audit reports 1,459,198 rows, 19 columns, 16,214 series, 16,213 complete 90-day series, and one incomplete 28-day series `(420, 764)`, with no nulls or duplicate keys. Those raw counts were not independently reproduced in setup and do not describe the entire published dataset.

## Matched comparison and historical predictors

The primary comparison uses 14 days of recent history. Both conditions use the same model families, common features, eligible target keys, splits, preprocessing choices, and tuning budgets. The intended difference is the addition of historical stockout features.

- Common predictors: sales lags 1 and 7, recent sales mean/standard deviation, known weekday, and categorical context including IDs treated as categories.
- Added stockout predictors: past stockout hours, count/proportion of affected historical days, and last-day availability.
- Planned common context-length comparison: 7/14/28 days. Begin eligible examples on day 29 for all conditions and lengths while keeping the original calendar split boundaries. Context comparisons remain optional later work.
- For target day `t`, all historical predictors must use observations through `t-1` in the same series. Known calendar fields for `t` are allowed. Prior stockout days remain in input history.
- Use an explicit predictor allowlist. Never feed baseline prediction columns, split labels, day/target-derived metadata, or the target itself into models accidentally.
- Target-day actual sales, stock status/hourly sales, realized weather, and unverified future promotion/discount fields are prohibited predictors. Verify any proposed known-in-advance field before allowing it.

Exact feature names, rolling statistics conventions, category handling, and missing-value rules must be agreed and documented in the next contract task; no feature producer exists yet.

## Retrospective target eligibility

Planned primary train, validation, and test targets have zero reported stockout hours during 06:00–22:00. Independently confirm field semantics, interval boundaries, and hourly-array indexing against source documentation and local values before implementing this rule. The publisher's data card describes `stock_hour6_22_cnt` as an out-of-stock-hour count; that description alone does not constitute the project's formal local consistency/indexing audit.

Target-day availability is retrospective eligibility metadata only and must be retained separately from predictors. Do not remove prior stockout days from the input history. Report counts removed by each history, availability, missingness, or other eligibility filter, by split, including overlapping-filter handling. Both feature conditions must use exactly the same final eligible target keys. Resulting eligible row counts remain unknown; setup checked only the inherited split counts.

## Fitting, tuning, and test discipline

- Fit preprocessing on training rows only. Treat IDs as categorical variables, not numeric magnitudes.
- Core models: linear regression and decision-tree regression. Ridge is allowed if covered in the course. Random forest is optional after course-fit confirmation. No CNN/RNN/LSTM/deep learning or unrelated models added to inflate scope.
- Select hyperparameters on validation only, with equal budgets across feature conditions. Freeze features, eligibility, models, metrics, and parameters before new model test evaluation.
- Daily walk-forward features may use prior observed validation/test days. Do not use future data or refit model/preprocessing parameters on those periods.
- Apply nonnegative predictions consistently across all compared models/baselines, document the rule, and preserve prediction provenance.

## Baselines and evaluation

Existing implemented baselines are persistence (yesterday's sales) and the mean of the preceding seven days. Their inherited metrics are in `results/baselines_DELTA/inherited/baseline_metrics.csv`, using all 3,000 rows per evaluation split; these have not been independently reproduced. Recompute them later on **exactly the matched eligible evaluation rows** and save new results separately.

Planned, not implemented: lag-7 same-weekday sales, and a recent mean over stocked historical dates with ordinary historical mean fallback. Define the window and empty-history fallback details before implementation.

For actual `y` and consistently nonnegative prediction `p`, report:

- MAE: mean of `abs(p - y)`.
- RMSE: square root of mean of `(p - y)^2`.
- Signed bias: mean of `p - y` (positive means overprediction).
- Mean underprediction: mean of `max(y - p, 0)` over all evaluated rows.
- Mean overprediction: mean of `max(p - y, 0)` over all evaluated rows.

Report overall, per-series, and store-level results, plus strata with/without historical stockouts using an explicitly agreed historical window. Course-appropriate additional metrics require limitations; avoid undefined percentage errors on zero sales. Use paired store-clustered uncertainty if enough stores exist, documenting the resampling unit and adequacy; daily rows are not independent replicates. No uncertainty estimates have been computed in setup.

The proposal's pilot goal is at least 10% lower MAE from stockout features with no greater mean underprediction. This is a target, not an achieved outcome or a reason to tune on test. Report null and negative findings honestly.

## Disclosed limitations and deviations

1. The inherited pilot required completeness over all 90 days, whereas the proposal intended training-only selection. This is retrospective availability selection and limits generalization; it is not proof of target leakage. Preserve the actual manifest. An optional training-only-selection sensitivity study would need its own explicit version and scope.
2. Original baseline test scores have already been seen. Do not claim a pristine unseen test. Freeze later choices before any new model test evaluation and disclose prior exposure.
3. The full raw-data pipeline and experiment-wide leakage checks have not been independently rerun. Static import checks are narrower evidence. The raw local export is smaller than the published dataset.
4. Stockout-free target evaluation is retrospective and changes the evaluated population. It does not identify latent demand on censored days or establish food-waste reduction.

## Proposed handoff contract — agreement pending

Before modeling, agree on a prediction record with unique `(store_id, product_id, dt, model, feature_set, split)`, plus actual value, prediction, and run identifier. Multiple runs need separate versioned output files/run namespaces so uniqueness remains meaningful. Specify date and ID types and allowed split/feature-set values.

Keep eligible target keys, filter reasons, feature definitions, input hashes, timing provenance, preprocessing/tuning decisions, and run metadata separate from predictor inputs. Retain enough lineage to match predictions to identical targets and explain every exclusion. Imported baseline predictions use their historical schema and have no `feature_set`/run ID; preserve them rather than silently rewriting them to the proposed contract.

No model-output producers or feature/eligibility implementation are authorized by setup. The next bounded technical task is inspection and contract freezing only.

## Workspace ownership update

The user-authorized active team is DELTA (data/shared features/baselines), DEVGRU (linear/ridge), and SAS (tree/evaluation/audit/integration), with identities in `context.md`. This replaces historical task ownership without altering scientific choices or claiming completed work. The requested codename folders/configs are organization only; the handoff schemas remain draft and stockout semantics/eligibility still require verification. See [current responsibilities](team_responsibilities.md) and [interfaces](interfaces.md).
