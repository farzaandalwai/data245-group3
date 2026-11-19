# Shared contract freeze and stockout-field audit

Date: 2026-11-18 (America/Los_Angeles). Owner/requester: SAS. Scope: merge the reviewed layout and freeze the data/eligibility/feature/prediction/preprocessing/tuning/evaluation definitions so DELTA, DEVGRU, and SAS can implement separately. No feature table, fixture, model, evaluator, or score was produced by this task.

## Integration and authority

At the user's “do it” instruction, PR #2 was reviewed against the unchanged latest main and previously passed checks, then merged as `35bfa71208d0297c72c41f00c104abed9027235b`. No separate teammate approval or human technical validation is claimed. Layout/startup guidance is integrated. The follow-up contract work uses branch `SAS/freeze-shared-contract` from that merged main; its final PR/merge is the integration evidence.

Version **1.0.0** is frozen for implementation in [contract.yaml](../configs/contract.yaml), with [contract.lock.json](../configs/contract.lock.json) recording exact definition/input/audit hashes. [interfaces.md](interfaces.md) is the readable operational guide. Source/local field consistency is verified; producer correctness, train-fitted preprocessing, final experiment-wide leakage checks, model/runtime checks, and validation-selected parameters remain future implementation evidence. The user-authorized definition is not a claim that all teammates have independently reviewed it.

## Primary source support

The [publisher's dataset card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md#data-fields) identifies the daily field as out-of-stock hours and the vector as hourly out-of-stock status. In [publisher code at pinned commit 8af694a](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/exp/data/generate_data.py#L61-L63), daily arrays have 24 entries, the business-hour slice is `[6:22]`, and status 1 marks censored observations. The inspected source blob is `fc56086de90fb075913e8d053b8e0a438dd1d030`. The [publisher's SSA evaluation](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py) also selects rows with zero business-hour stockout count.

Thus the operational interval is 06:00 inclusive through 22:00 exclusive, covering indices 6 through 21 (16 hourly bins). This conclusion is supported by source code and the local consistency check; it is not an independent audit of the underlying warehouse annotation system. No publisher model code was executed or copied into the project.

## Actual local audit

Executed `python3 scripts/audit_contract.py --output docs/contract_audit.json`. The script uses only the standard library, parses bracketed binary vectors without eval, verifies the fixed source hash, compares array/count semantics, checks finite nonnegative actuals and static context consistency, and counts the already planned sequential filters. It does not compute forecasting features or metrics. The complete machine-readable evidence is [contract_audit.json](contract_audit.json).

- Checked all 18,000 pilot rows, 200 fixed series, and 113 stores.
- Every stock vector had 24 binary entries. The observed daily count range was 0–16.
- `sum(hours_stock_status[6:22])` matched the reported daily count on every row (0 mismatches). Including index 22 instead would disagree on 7,682 rows.
- Five source hierarchy/context fields were constant within each series. They remain excluded from the v1 predictor allowlist; this audit does not grant permission to add them.
- Source target values were finite/nonnegative. No target average, error, model performance, or new baseline score was calculated.

Sequential counts, preserving original split boundaries:

- Train: 12,000 original; remove 5,600 dates before day 29; 6,400 remain; remove 2,707 target stockouts; **3,693 eligible**.
- Validation: 3,000 original; no history removals; remove 1,302 target stockouts; **1,698 eligible**.
- Test: 3,000 original; no history removals; remove 1,253 target stockouts; **1,747 eligible**.

Total eligible targets: **7,138**, identical by definition across both feature conditions, core models, and optional history windows. Each split has eligible rows from all 113 stores. Eligible series counts are 198/198/199 for train/validation/test; retain the fixed 200-series manifest and report absent series results as not evaluable. Do not silently remove other evaluation keys because a category has no eligible training rows.

These counts are from the fixed local pilot only. They are not raw-export verification, features, matched baseline metrics, model findings, or a demonstration of improved forecasting. The eligibility policy was supplied before this inspection; no model/test-error feedback was used to choose it.

## Frozen decisions and implementation gates

The canonical YAML fixes exact primary predictors and definitions, population rolling std, source-date cutoffs, serialization/file schemas, categorical/unknown handling, nonnegative predictions, pooled estimators, equal per-condition tuning budgets, validation selection/ties, model ownership, prediction/run metadata, metric aggregation, historical strata, and paired store-clustered uncertainty. Required primary history is 14; 7/28 are optional with shared day-29 eligible keys. Redundant hierarchy predictors and count/proportion duplicates are excluded from the first implementation to keep it simple.

The OLS and decision-tree plans are enabled. Ridge/random forest remain optional and disabled until course fit and an explicit amendment; no unverified course coverage is asserted. New model test evaluation remains blocked until actual validation-selected parameters, code revision, contract and bundle hashes are frozen. This definition freeze does not claim that model parameters have been selected or that a real feature bundle exists.

DELTA's next bounded implementation is the shared bundle and its independent value/timing/key verification. DEVGRU and SAS can implement adapters/evaluator logic against the frozen schemas in parallel, using clearly labeled synthetic fixtures if needed. Real paired runs need DELTA's verified bundle; final evaluation needs accepted predictions. No such implementation was started by this freeze.

## Verification status

Completed checks passed: `python3 scripts/verify_setup.py` verified all ten original hashes/byte counts, unchanged canonical data/evidence, eight Python files, notebook JSON/31 cells and 13 code cells without execution, fixed pilot/manifest/keys/calendars/splits, inherited prediction/metric structures without scoring, 54 current Markdown paths, and ignore/retention rules. `python3 -m unittest discover -s tests -v` passed all eight layout/contract tests. The source audit was reproduced without changing its locked evidence; the lock/input/definition hashes matched. The endpoint tests distinguish hours 5/6/21/22 and day 28/29, and reject malformed/nonbinary vectors. The publisher commit reference was read back as a commit (not merely a branch name). Original data/archive/prediction bytes remain protected; full raw pipeline, notebook execution, package installation, model training/scoring, and teammate-machine validation remain unrun. Prior baseline test exposure and retrospective complete-series selection remain disclosed limitations, as does retrospective stockout-free-target evaluation.

Optional baselines use their explicit DELTA output roots and the `sales_only` label once as a common reference; learned model preprocessing/paired tuning rules do not imply fitting a baseline. The contract keeps the day-29/target-stockout filters separate from historical feature construction. A future validation freeze binds history window as well as model, conditions, chosen parameters and code/contract/bundle hashes, preventing accidental cross-window reuse.
