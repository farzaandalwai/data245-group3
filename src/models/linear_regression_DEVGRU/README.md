# Linear regression — DEVGRU

Status: not implemented. Own linear regression under both sales-only and stockout-aware feature conditions. Consume the shared DELTA bundle; fit preprocessing on training only, exclude IDs from predictors, tune choices on validation, and document preprocessing/prediction policy in the draft technical contract.

Output: separate versioned predictions/run metadata under `results/linear_regression_DEVGRU/` following `docs/interfaces.md`. Acceptance: common eligible target keys, no future/target predictors, documented preprocessing/tuning, and validation evidence. Model-adapter development may use a clearly labeled schema fixture before the real bundle arrives. Real paired runs require the frozen verified bundle; new test evaluation waits for the protocol/validation freeze.

Follow the [approved v2 protocol](../../../docs/experiment_protocol.md) and [draft shared contract](../../../docs/interfaces.md). Real runs use DELTA's same verified development/final bundle and target keys, including otherwise eligible stockout target dates; subgroup labels are evaluation-only. V1 evidence/tests are now separate from active V2 checks; finalize the draft technical interface before implementation. Git ancestry integration remains pending.
