# DEVGRU Linear/Ridge technical decisions

Status: **PROPOSED / PENDING TEAM AGREEMENT**. This DEVGRU note does not amend the shared protocol, interfaces, YAML metadata, or final-scoring gate.

## Implemented and tested

- Both models consume DELTA's exact ordered `sales_only` and `stockout_aware` allowlists. Predictor matrices never use exclusion-based column discovery; unexpected observation metadata is ignored.
- Bundle joins are keyed, one-to-one, and fail closed on missing, duplicate, extra, or inconsistent keys. Paired conditions must have identical keys, actuals, and splits.
- Constructors require an explicit `none` or `standardize` preprocessing policy. Standardization is fit on training rows only, reused for validation, and safely handles zero-variance columns.
- Model bundle prediction defaults to train and validation rows only. Test prediction requests are rejected; no test authorization mechanism is implemented.
- Linear Regression uses NumPy least squares with an explicit intercept.
- Ridge uses an augmented least-squares system with `sqrt(alpha)` coefficient penalties and an unpenalized intercept, avoiding direct normal-equation solves.
- Prediction exchange validation checks exact schema/order, ISO dates, finite values, recognized labels, nonempty run IDs, unique keys, and key-based correspondence of authoritative keys, actuals, and splits.
- Ridge alpha selection accepts at most 20 unique finite positive numeric candidates, fits each candidate on training rows, scores validation MAE only, and breaks equal-MAE ties by the smaller alpha. It returns candidate-level evidence.
- Synthetic smoke tests are explicitly non-test-only and are not research evidence.

## Proposed, not approved

- Preprocessing: standardize all approved predictors using training-only statistics for both Linear and Ridge, while retaining `none` as an explicit implementation option until the group freezes the choice.
- Ridge grid/budget: `[0.01, 0.1, 1.0, 10.0, 100.0]`, with no more than 20 candidates per feature condition.
- Prediction postprocessing: no clipping by default. Any nonnegative clipping requires approval and must be applied identically before comparison.
- Validation selection/tie policy: smaller alpha on equal validation MAE is implemented locally; shared comparison policy still requires agreement if it affects other model families.
- Dependence-aware uncertainty procedure remains unresolved.

Timothy (DELTA) must accept the producer bundle/interface; Shoury (DEVGRU) must agree to preprocessing, Ridge grid/budget, and postprocessing; Farzaan (SAS) must accept prediction/evaluator checks and the uncertainty procedure. No real development tuning or final scoring is authorized by this note.
