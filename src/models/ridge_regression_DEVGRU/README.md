# Ridge Regression - DEVGRU

IMPLEMENTED approved extension. NumPy solves an augmented least-squares system
with an unpenalized intercept. Standardization is fitted on training rows only.
Each feature condition uses validation MAE over `[0.01, 0.1, 1, 10, 100]`; exact
ties prefer smaller alpha. Saved development choices are 10 (sales-only) and
100 (stockout-aware), verified against the original selection records and saved
predictions. They are validation choices, not a jointly approved final freeze.

New runs share Linear Regression's SAS-compatible development envelope and
numeric fitted-state exports. Original missing fitted objects remain missing.
The model's bundle prediction API rejects test splits. Final execution remains
blocked pending joint freeze and SAS executor review. No real-model retraining
or final predictions occurred in this task.

See [Linear/development usage](../linear_regression_DEVGRU/README.md), the
[readiness record](../../../docs/DELTA_DEVGRU_READINESS.md) and the
[approved protocol](../../../docs/experiment_protocol.md).
