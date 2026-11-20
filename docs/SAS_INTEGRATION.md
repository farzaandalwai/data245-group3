# SAS integration: decisions, uncertainty and real-data acceptance

This record supersedes the earlier local-only publication restriction and missing
bundle status in [SAS local handoff](SAS_LOCAL_HANDOFF.md). The user now authorizes
SAS implementation, relevant shared integration metadata/docs, staging/commit/push
of the task branch and a draft PR. No merge, teammates' models or final/test
scoring. Base verified by fetch/history: `d2a323e`, 0 commits ahead/behind at task
start. Previously uncommitted SAS work is retained, not reset or blindly pulled.

## Approved choices and pending verification

The team decision is **no prediction clipping**, including during selection and
evaluation. This changes the original V1 nonnegative-clipping proposal (see the
unchanged [historical selection policy](history/contract_v1/configs/contract.yaml)).
Finite negative forecasts remain valid. SAS emits raw predictions and its tests
cover negative prediction errors. The evaluator can check values/keys/provenance,
but values or metadata alone cannot establish that another producer did not clip.

Linear/ridge must standardize with training-fitted means/scales, reusing those
statistics on validation; Ridge alpha must minimize validation MAE. These remain
**REQUIREMENTS PENDING VERIFICATION**. Their implementation is absent in the
reviewed upstream. Do not infer compliance from manifest declarations; inspect
executable fitting/selection paths and behavioral evidence when supplied. No
DEVGRU implementation is created or modified by this task.

**PROPOSED, awaiting team agreement:** exact validation-MAE ties could prefer
larger Ridge alpha; trees could prefer shallower depth (unlimited last), then
larger minimum leaf size, then canonical parameter order. No near-tie tolerance
has been agreed. SAS's existing deterministic rule remains **first in declared
grid order on an exact tie**, with depths 3/5/8/unlimited and leaf sizes 5/20/50
iterated in that order. It has not been silently replaced by the proposal.

## Development confidence intervals

`mae_difference_intervals.csv` reports the pooled difference
**MAE(stockout-aware) minus MAE(sales-only)** and its 95% paired store-cluster
percentile interval. Negative favors stockout-aware. This sign is opposite the
existing `MAE_reduction` benefit column, which remains clearly named.

For each learned model/split, validate both conditions against the complete
authoritative observation set first. Join matching keys and compute each row's
absolute-error difference. Sort keys/stores deterministically. For S stores draw
S store indices with replacement per replicate using NumPy Generator/PCG64 seed
245, for 2,000 replicates. Every drawn store contributes all its series/dates;
duplicates contribute repeated complete copies. Cluster error sums/row counts
are sufficient statistics for this concatenation. Divide by each draw's total
row count; do not average store means equally. Reset the fixed RNG for each
comparison. Endpoints are 2.5th/97.5th percentiles with linear interpolation.
Reports include S, row count, seed, replicates, confidence level, status and
limitations. Fewer than two stores gives undefined endpoints; equal endpoints
are labeled degenerate. Intervals cover the overall population, not subgroup
intervals or simultaneous inference across models. Baselines have no paired
feature condition and receive no artificial interval.

Only development train/validation splits are allowed. Training intervals are
descriptive. Models stay fixed (no bootstrap refitting or retuning); validation
selection can make validation estimates optimistic. Few clusters can yield
unstable intervals. Independence between stores is assumed; common calendar
shocks/cross-store dependence are not resolved. Sampling completeness is
retrospective, and known historical test exposure remains disclosed. Nominal 95%
coverage is not a guarantee. No sustainability or population-wide gain is claimed.
NumPy API references: [integer sampling](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.integers.html)
and [quantiles](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html).

## Exact development inputs

Broader Drive search found DELTA's shared
[v2-development-200-r2 folder](https://drive.google.com/drive/folders/12_U4DeCfh8UjEoWiAnJJfAg1crDf9Jd6),
outside the previously inspected empty `experiments` folder. Its downloaded
manifest exactly matches the trusted handoff SHA-256
`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`.
All ten files were downloaded through authenticated file references and checked
against the pinned manifest before import into the ignored exact bundle path.
No CSV was regenerated or substituted. Schema, full calendar, sample, common
features, metadata and split coverage passed DELTA's loader: 200 series, 113
stores, 9,200 train / 3,000 validation / 3,000 test observations. Loading validates
the full bundle structurally; learned fitting/prediction/scoring uses only train
and validation. Raw export/final bundle are not needed and are not substituted.

GitHub main/branches, releases and Actions artifacts were also inspected; no
bundle artifact was present there. Bundle bytes remain ignored, not staged.

## Validation and publication

The complete suite passed **61 tests** (35 existing + 26 SAS); setup/original-byte
checks and whitespace checks passed. Five new bootstrap tests check literal
whole-cluster expansion with unequal cluster sizes, row weighting, pairing and
sign, repeatability/order invariance, one-store rejection, degenerate intervals,
and the final/test gates. Integration tests check interval exports and metadata.
Synthetic CLI tree/comparison runs are separately labeled `SYNTHETIC_NOT_RESEARCH`.

Real run `sas-tree-dev-200-bootstrap-r1` fitted 12 candidates per condition on
9,200 training rows and selected settings using 3,000 validation rows. Both chose
depth 5/minimum leaf 5 under the existing deterministic rule. Validation MAE:
sales-only 0.348255, stockout-aware 0.352070. The validation difference was
+0.003814; 95% interval approximately [-0.003332, +0.013629], with **113 stores**
and 2,000 replicates. This is developmental, conditional on validation-selected
settings, and does not establish a clear improvement. No test predictions or
test/final scores were generated. Raw-data feature reconstruction was not
repeated; input acceptance uses exact trusted bundle hashes and loader checks.

Exact input/output/source identities and unrounded metrics are recorded in
[integration evidence](SAS_INTEGRATION_EVIDENCE.json); generated CSV/tree files
remain ignored. The earlier [synthetic-only evidence](SAS_LOCAL_RUN_EVIDENCE.json)
is preserved as a historical snapshot, not relabeled as real evidence.

The task branch is authorized for a draft PR, not merging. Full multi-model comparison still needs DEVGRU's
accepted predictions and behavioral verification. Final test scoring remains
blocked even after this task is published for review.

Publication verified: implementation commit `3e55dd4` is pushed on
`SAS/local-tree-evaluator`. [Draft PR #4](https://github.com/farzaandalwai/data245-group3/pull/4)
is open against main; GitHub readback confirmed draft status and no merge.
The publication receipt is recorded in a documentation-only follow-up commit.
