# Approved experiment protocol - v2.0

**APPROVED scientific design: 2026-11-19, America/Los_Angeles.** All three active members agreed to the methodology in the [saved request](prompts/2026-11-19-methodology-alignment.md). This supersedes conflicting v1 assumptions. Approval does not imply implementation, a frozen technical contract, or results.

## Authority and evidence statuses

Scientific authority, in order: this protocol; [interfaces](interfaces.md); [team responsibilities](team_responsibilities.md); `configs/*.yaml` metadata; [context](../context.md); [experiment log](experiment_log.md); other READMEs; historical `archive/` reference. Root [AGENTS.md](../AGENTS.md) governs agent workflow, not a separate methodology. Explicit user instructions govern the task; flag contradictions and record approved amendments rather than silently selecting a conflicting rule. Configs mirror the protocol and cannot approve changes themselves.

- **APPROVED:** scientific decisions below.
- **PROPOSED:** recommendations such as the final sampling seed/algorithm.
- **PENDING VERIFICATION:** exact raw-export lineage and normalization coefficient; undocumented missing/closed-hour business semantics; learned-model environment compatibility on consumer machines.
- **DRAFT CONTRACT:** remaining learned-model preprocessing, prediction policy, tuning grids/settings and uncertainty procedure. DELTA producer schemas/filenames are implemented; see handoff.
- **IMPLEMENTED / VERIFIED operationally:** DELTA producer, development/final feature bundles, final 1,000-series manifest and development baselines; see [handoff](DELTA_DATA_HANDOFF.md).
- **NOT IMPLEMENTED:** learned-model runs, common evaluator and final comparisons.
- **IMPLEMENTED:** requires actual code and supporting checks; documentation alone never qualifies.
- **HISTORICAL:** previous 200-series experiments/results and superseded contract evidence.

Remote V1 validation work from `1939586` and approved V2 methodology are integrated in base `5dcd128`. Exact V1 contract/audit/lock/script/provenance copies are preserved under [historical evidence](history/contract_v1/README.md); their day-29/stockout-free rules are not active. [Active contract metadata](../configs/contract.yaml) registers V2 summaries and remains DRAFT, with no V2 freeze lock. Active tests validate V2; separate historical tests reproduce V1 evidence. V2 now reconciles the publisher hourly convention against the complete local export. Missing/closed-hour business semantics and human acceptance remain outstanding; Git ancestry integration is complete.

## Research question and target

Does adding historical stockout information improve next-day fresh-food recorded-sales forecasts compared with using sales history alone?

Use FreshRetailNet-50K for supervised regression of next-day normalized recorded `sale_amount`, keyed by `(store_id, product_id, dt)` where `dt` is the target date. Recorded sales can be lower than underlying customer demand when products are unavailable. We do not estimate unobserved demand, conduct causal inference, assume accuracy gains, or claim measured sustainability benefits.

## Samples and primary population

Use **200 complete store-product series for development/debugging** and **1,000 complete series for the final experiment**. Preserve the inherited pilot, manifest and evidence unchanged. The final manifest is **GENERATED / VERIFIED operationally** (see handoff); use the same final selection across model families and feature conditions. Keep pilot and final outputs separate and versioned.

Use a fixed reproducible selection procedure. Authorized implemented seed: **245**. DELTA uses deterministic SHA-256 key ranking without outcome-derived strata; measured training-only coverage is in the handoff. Recommended requirements: seek reasonable store/product/historical-stockout coverage; stratify stockout activity using training-period information only; never select/exclude based on validation/test outcomes; document algorithm, completeness/quality rules, source revision, coverage and provenance; save a versioned manifest. Document retrospective availability selection when assessing completeness across 90 days. A 1,000-series sample does not guarantee representativeness.

**Primary population: all eligible target dates, including stockout dates**, across training, validation and testing. Do not exclude an observation solely because `stock_hour6_22_cnt > 0`. Eligibility follows agreed history, sample and quality requirements; implemented producer rules reject invalid required records, exclude incomplete series and never impute missingness; see handoff. Build history before applying the shared target mask, retaining prior stockout days. Log exclusions/counts by split and reason, with documented handling of overlapping filters.

**Secondary test evaluation:** fully stocked target dates and target dates with stockouts, labeled retrospectively after prediction. These are subgroups of the same predictions, not different targets or separately trained models. Target-day stockout metadata stays outside every predictor allowlist. The producer verifies 24 binary entries, 1=stockout and indices [6:22] against publisher code and the full local export. Group labels mean annotated stockout status only; undocumented missing/closed-hour behavior remains provisional.

The superseded stockout-free policy removed approximately **43.16%** of candidate targets in the prior eligibility audit. This is historical filter evidence, not an active preprocessing requirement or a redesigned experiment result.

## Primary predictors and timing

Primary maximum lookback: **14 days**. Transform within each chronologically ordered store-product series. For target date `t`, historical predictors use dates strictly before `t`; previous `w`-day means/proportions use `t-w` through `t-1`. Known target-date calendar features are allowed. Earlier observed validation/test dates may supply history for later predictions without parameter refitting.

| Condition | Approved conceptual predictors |
| --- | --- |
| `sales_only` | Sales lags 1, 2, 3, 7, 14; previous 7-day and 14-day mean recorded sales; day of week; weekend indicator |
| `stockout_aware` | Every sales-only predictor plus previous-day stockout hours; previous 7-day and 14-day mean stockout hours; previous 7-day and 14-day proportion of days with stockouts |

Both conditions share identical keys, actuals, splits and common predictors. Use explicit finalized allowlists. Store/product IDs are keys, not automatically approved predictors. Current/future sales or stockouts, baseline predictions and split labels cannot be predictors. Additional weather, discount, promotion, holiday or categorical predictors require an explicit protocol amendment. Optional 7/14/28-day sensitivity comparisons are not required core work and must not delay primary targets to day 29; any sensitivity population needs a documented comparison policy.

## Chronological splits and fitting

Retain the 90-day project horizon:

| Split | Days | Established calendar | Projected final candidate targets |
| --- | --- | --- | ---: |
| Train | 1 to 60 | 2024-03-28 to 2024-05-26 | 46,000 |
| Validation | 61 to 75 | 2024-05-27 to 2024-06-10 | 15,000 |
| Test | 76 to 90 | 2024-06-11 to 2024-06-25 | 15,000 |

With 14 prior days, candidate targets start on **day 15**. These expected counts were **VERIFIED** by DELTA generation for 1,000 complete series with no additional quality exclusions: **76,000 total** (handoff records artifact identities). Inherited pilot source counts 12,000/3,000/3,000 describe rows before history eligibility, not final observations.

Fit preprocessing on training only; tune on validation only. Document equal per-condition tuning budgets/policy within each applicable model family. Freeze actual validation selections, source/bundle/contract revisions and parameters before new test evaluation. Never use test results to select sample, features, models or parameters. Do not refit preprocessing/models on validation/test without an approved amendment. Exact preprocessing, settings and prediction postprocessing (including any nonnegative clipping) remain contract decisions; apply agreed rules consistently and preserve provenance.

## Models and baselines

- **Required core:** Linear Regression (DEVGRU), Decision Tree Regression (SAS).
- **Approved extensions:** Ridge Regression (DEVGRU), optional Random Forest Regression (SAS). These are not prohibited or awaiting course-fit approval in this design; implementation remains pending.
- **Required baselines:** previous-day recorded sales (`persistence`), preceding 7-day mean recorded sales (`recent_avg_7`), owned by DELTA.

Each applicable learned model compares both feature conditions on matched observations under a documented tuning policy. Baselines use the same evaluation population as common references. Precise grids/settings must be finalized in the implementation contract; no selected settings or gains are claimed. Other historical baseline ideas are outside required core work. No deep learning or scope inflation.

## Evaluation

For actual `y` and prediction `p`, primary metric is **MAE = mean(abs(p-y))**. Secondary metrics: **RMSE = sqrt(mean((p-y)^2))** and **signed bias = mean(p-y)**; positive bias means overprediction.

Where practical, report relative MAE improvement `100 * (MAE_sales_only - MAE_stockout_aware) / MAE_sales_only` (undefined for zero denominator), test subgroup errors for stocked/stockout target dates, and under/overprediction behavior. Mean underprediction is `mean(max(y-p,0))`; mean overprediction is `mean(max(p-y,0))`, each over all evaluated rows. Report denominators and empty groups honestly. Series/store summaries can supplement the overall comparison.

Use identical evaluation keys and actuals across conditions, model families and baselines. Provide appropriate paired uncertainty where practical, acknowledging dependence within stores/series and across dates; resampling units, adequacy and settings remain draft. Daily rows are not independent replicates. Report null or worse performance honestly.

## Central pipeline, limitations and implementation gate

DELTA is the authoritative data/feature producer. DEVGRU and SAS consume approved versioned outputs; model owners must not independently redefine targets, samples, eligibility, history, splits, shared evaluation keys or metrics. All predictions follow one group-approved schema; see [interfaces](interfaces.md). All three share scientific decisions, final integration, review and submissions; ownership is not contribution credit.

The historical pilot used all-90-day completeness rather than the earlier training-only intention. Disclose retrospective availability selection and document the final algorithm. Baseline test results have already been seen: the examined holdout is not pristine confirmatory evidence, including when reused within a larger sample. Raw export lineage and undocumented business semantics remain pending; Python 3.12 and DELTA producer/leakage checks are verified as documented in the handoff. Historical scores are not final v2 results. Consumers may implement against the verified producer interface; final evaluation still requires human bundle acceptance and frozen validation choices.
