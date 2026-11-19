# Linear regression — DEVGRU

Status: not implemented. Own linear regression under both sales-only and stockout-aware feature conditions. Consume the shared DELTA bundle; fit preprocessing on training only, treat IDs as categories, tune choices on validation, and use the agreed nonnegative prediction rule.

Output: separate versioned predictions/run metadata under `results/linear_regression_DEVGRU/` following `docs/interfaces.md`. Acceptance: common eligible target keys, no future/target predictors, documented preprocessing/tuning, and validation evidence. Model-adapter development may use a clearly labeled schema fixture before the real bundle arrives. Real paired runs require the frozen verified bundle; new test evaluation waits for the protocol/validation freeze.
