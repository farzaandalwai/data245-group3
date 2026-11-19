# Active three-person split

This plan follows the user's explicit correction that only DELTA, DEVGRU, and SAS are active, and their subsequent authorization to organize the repo for this split. Identity mapping is in `context.md`. Original five-person assignments remain historical source provenance; they are not current assignments or evidence that the other people did work here. The requested plan is recorded without claiming each member has personally reviewed or completed it.

## DELTA — data, shared features, and baselines

Own `src/data_preprocessing_DELTA/`, `src/features_DELTA/`, `src/models/baselines_DELTA/`, `notebooks/DELTA_data/`, canonical data/manifests, and `results/baselines_DELTA/`.

Existing evidence: inherited preparation/pilot/baseline work, not independently reproduced. Future deliverable: a verified versioned feature bundle for both conditions with identical eligible keys, explicit predictor allowlists, split/filter counts, past-only timing evidence, and separate matched baseline predictions. Preserve the exact pilot/manifest and inherited results. Dataset/feature changes must be coordinated because everyone consumes them.

## DEVGRU — linear models

Own `src/models/linear_regression_DEVGRU/`, `src/models/ridge_regression_DEVGRU/`, `notebooks/DEVGRU_linear_models/`, and matching result directories.

Future deliverable: linear regression and course-approved ridge for both feature conditions, training-only fitted preprocessing, validation-selected settings under matched budgets, standardized predictions, and verification/provenance. Consume DELTA's shared features; do not independently redefine them or silently change eligible rows.

## SAS — tree, evaluation, audit, and integration

Own `src/models/decision_tree_SAS/`, optional `src/models/random_forest_SAS/`, `src/evaluation_SAS/`, `notebooks/SAS_evaluation/`, and matching tree/comparison result directories. Coordinate shared protocol and PR integration.

Future deliverable: paired decision-tree predictions, common metric/key checks, formal timing/leakage audit, error/bias and store-level analysis, justified uncertainty, and integrated comparison. Random forest is optional after core work and course-fit confirmation. Integration ownership does not transfer authorship of teammates' components or authorize writing their individual reports.

## What can happen in parallel

After one shared interface review, DELTA can build the real feature producer while DEVGRU builds linear-model adapters and SAS builds tree/evaluator adapters. Model/evaluator development can use clearly labeled deterministic schema fixtures; fixture scores must never be presented as research results. No fixture or new producer was created by restructuring.

Everyone can commit/push their own branch and open a PR before the others finish. Components exchange versioned input/output files and metadata; do not make someone execute another person's notebook or wait for their full branch to be merged just to develop an adapter.

## Where waiting is required

1. First agree on stable paths, exact data/feature/prediction schemas, target eligibility, timing, and tuning/evaluation rules. The current interface document is a draft, and stockout semantics/indexing/allowlists remain unverified.
2. Real paired model/baseline runs require the same frozen verified DELTA feature bundle and target keys. New model test evaluation also waits for frozen protocol and validation choices. Existing baseline test exposure remains disclosed.
3. Final comparisons require accepted prediction files for the relevant models. Partial validation diagnostics must be labeled partial.

These are necessary scientific handoffs. Ownership separates implementation; it does not remove data dependencies.

## Working rules

Use separate clones and `<codename>/<task>` branches. Keep runtime code, notebooks, and outputs within the component boundary. Coordinate shared `configs/`, requirements, protocol/interface files, and root guidance changes. Update your own owner-status section in `context.md` plus applicable contribution/AI records; short section edits reduce, but cannot eliminate, conflicts. A human integrator preserves all valid updates and merges PRs sequentially. Code ownership is a coordination convention, not an atomic lock or enforced GitHub protection.

Each person owns their own individual report/disclosure and contribution evidence. Folders/log assignments are not completion credit. Future task acceptance must name concrete code/evidence/checks rather than just creating empty directories.
