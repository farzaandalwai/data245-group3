# Task: Synchronize DATA 245 Repository Documentation After Group Methodology Approval

Act as a Principal Machine Learning Engineer, ML Research Lead, and Technical Documentation Architect.

You are working in our existing DATA 245 group project repository.

**Your task is to synchronize the repository's Markdown documentation, AI-agent instructions, and corresponding YAML configuration metadata with our newly approved experimental methodology.**

All three active group members have agreed to the decisions below.

This is a **documentation and configuration alignment task only**.

Do not write, modify, execute, retrain, or refactor ML implementation code. Do not migrate datasets, regenerate experimental outputs, modify historical artifacts, or implement new models.

Do not commit, push, merge, or create branches automatically.

---

## 1. FIRST: Inspect the Entire Repository

Before modifying anything, read and understand the current repository.

Inspect:

- `AGENTS.md`
- `README.md`
- `context.md`
- `starter_prompt.md`
- `docs/experiment_protocol.md`
- `docs/interfaces.md`
- `docs/team_responsibilities.md`
- `docs/methodology.md`
- `docs/experiment_log.md`
- `docs/course_requirements.md`
- `docs/contributions.md`
- `docs/ai_assistance.md`
- `configs/dataset.yaml`
- `configs/experiments.yaml`
- `configs/models.yaml`
- All other current Markdown documentation
- Any existing AI-agent instruction files
- The relevant existing source and configuration structure, for verification only

Inspect Git status and recent history so you understand what has already been migrated.

Read `docs/structure_migration.md` and `docs/provenance.md` to understand the historical archive.

The repository currently uses three owner codenames: DELTA, DEVGRU, and SAS.

**Important:** The repository is new. Missing regenerated datasets, feature tables, models, and results are expected. Do not treat missing implementations as documentation defects or attempt to recreate them.

The previous pilot and its results are historical evidence, not results from the redesigned experiment.

---

## 2. NEW GROUP-APPROVED SCIENTIFIC METHODOLOGY

The following decisions have been approved by all three active members.

They supersede conflicting planning assumptions in active repository documentation.

### A. Research question

**Does adding historical stockout information improve next-day fresh-food recorded-sales forecasts compared with using sales history alone?**

The purpose is to measure the incremental predictive value of historical stockout information.

We are NOT estimating unobserved customer demand.

We are NOT conducting causal inference.

We are NOT claiming that stockout features necessarily improve accuracy.

### B. Prediction target

- Dataset: FreshRetailNet-50K.
- Target: next-day normalized recorded `sale_amount`.
- Task: supervised regression.
- Forecast horizon: one day ahead.
- Features must be available before the target date.

Explain clearly that recorded sales can be lower than underlying customer demand when products are unavailable.

### C. Primary evaluation population

**APPROVED CHANGE: Use all eligible target dates for the primary experiment, including dates that experience stockouts.**

Do not exclude a target observation solely because `stock_hour6_22_cnt > 0`.

Eligibility is instead determined by the agreed history, data-quality, and sample requirements.

The prior experiment excluded approximately 43.16% of candidate target observations because of target-day stockouts.

That filter is NO LONGER the intended primary experiment.

Do not describe the old 43.16% exclusion as an active preprocessing requirement.

### D. Secondary evaluation populations

Analyze test performance separately for:

1. Fully stocked target dates.
2. Target dates that experienced stockouts.

These are retrospective evaluation subgroups.

They are NOT different prediction targets or separately trained models unless a future approved protocol explicitly says otherwise.

Target-day stockout information may be used after prediction to label evaluation groups.

It must NEVER enter the prediction feature matrix.

The exact dataset-specific interpretation of stockout-hour counts and hourly array indexing still requires technical verification.

Mark that implementation detail as pending. Do not invent a validated parsing rule.

### E. Dataset strategy

**Approved:**

- Development/debugging pilot: 200 complete store-product series.
- Final experiment: 1,000 complete store-product series.
- Use a fixed, reproducible selection procedure.
- Preserve the historical 200-series sample and its evidence.
- Use the same selected final sample across all model families and feature conditions.

The final 1,000-series manifest has NOT yet been generated.

**Recommended selection requirements:**

- Use a recorded random seed.
- Seek reasonable representation across stores, products, and historical stockout activity.
- Do not select or exclude series based on validation/test outcomes.
- Use training-period information for stockout-activity stratification.
- Document the selection algorithm and sample coverage.
- Save a versioned manifest and record its provenance.

Unless the existing approved documentation establishes a different seed for final sampling, retain seed 245 as the proposed default and document it explicitly.

Do not claim that 1,000 series statistically guarantees representative results.

The 200-series pilot is for development; the 1,000-series sample is the intended final experiment.

Do not mix pilot and final experimental results.

### F. Historical lookback and features

**Approved primary lookback: 14 days maximum.**

The primary experiment does not require a separate 7/14/28-day lookback comparison.

Those comparisons may remain optional sensitivity analyses, clearly marked as NOT required for the core experiment.

Define the proposed main feature sets as follows.

**Sales-only condition:**

- Sales lag 1 day.
- Sales lag 2 days.
- Sales lag 3 days.
- Sales lag 7 days.
- Sales lag 14 days.
- Previous 7-day mean recorded sales.
- Previous 14-day mean recorded sales.
- Day of week.
- Weekend indicator.

**Stockout-aware condition:**

Every sales-only feature above, PLUS:

- Previous-day stockout hours.
- Previous 7-day mean stockout hours.
- Previous 14-day mean stockout hours.
- Previous 7-day proportion of days with stockouts.
- Previous 14-day proportion of days with stockouts.

Both conditions must use the same observations, targets, and shared predictors.

All historical rolling features must exclude the target date.

Use grouped, chronologically ordered transformations by store-product series.

Do not use current/future sales or stockout values as predictors.

Store and product identifiers are observation keys, not automatically approved model features.

Any additional weather, discount, promotion, holiday, or categorical features require an explicit protocol amendment before being included in the primary comparison.

### G. Chronological splitting

Retain the established 90-day project horizon:

- Days 1–60: training period.
- Days 61–75: validation period.
- Days 76–90: final test period.

With the approved 14-day history, candidate prediction targets begin on day 15.

If the final sample contains exactly 1,000 complete 90-day series and no additional quality exclusions, expected candidate counts are:

- Training: 46,000 observations.
- Validation: 15,000 observations.
- Testing: 15,000 observations.
- Total: 76,000 observations.

These are PROJECTED counts, not verified outputs.

Do not describe them as observed or implemented.

Allow earlier observed dates to provide historical features for later validation/test predictions, while ensuring no future data enters the feature calculations.

Fit preprocessing transformations on training data only.

Tune hyperparameters on validation data only.

Do not use test results to select features, models, parameters, or the sample.

### H. Model scope

**Required core models:**

1. Linear Regression.
2. Decision Tree Regression.

**Approved extensions:**

3. Ridge Regression.
4. Random Forest Regression.

**Required simple baselines:**

- Previous-day recorded sales (persistence).
- Previous 7-day average recorded sales.

Do not describe Ridge or Random Forest as prohibited by the course.

Do not describe optional extensions as already implemented.

Each applicable model family must compare sales-only and stockout-aware conditions using matched data and a documented tuning policy.

The precise tuning grids and model settings must be finalized in the implementation contract. Do not invent completed tuning results.

### I. Evaluation

Primary metric:

- Mean Absolute Error (MAE).

Secondary metrics:

- Root Mean Squared Error (RMSE).
- Signed prediction bias, defined as mean(prediction - actual).

Also report, where practical:

- Relative MAE improvement of stockout-aware versus sales-only.
- Error by fully stocked versus stockout target dates.
- Underprediction and overprediction behavior.
- Appropriate uncertainty analysis, with dependence among observations acknowledged.

Use identical target keys and evaluation populations across feature conditions.

The previous pilot's test results are already known. Preserve them as historical exploratory evidence and do not claim that the same previously examined holdout is a pristine confirmatory evaluation.

### J. Team responsibilities

The active three-person ownership structure is:

**DELTA — Timothy Tran**

- Centralized dataset and data contract.
- Raw-data validation.
- Data preparation and pilot/final sample selection.
- Chronological splits.
- Shared sales and historical stockout feature engineering.
- Shared feature datasets and manifests.
- Persistence and 7-day-average baselines.
- Data provenance and preprocessing validation.

**DEVGRU — Shoury**

- Linear Regression.
- Ridge Regression extension.
- Model-specific training and tuning.
- Standardized model prediction outputs.

**SAS — Farzaan Dalwai**

- Decision Tree Regression.
- Optional Random Forest.
- Shared evaluation and model comparison.
- Leakage and integration checks.
- Evaluation figures and result summaries.

The three owners share responsibility for scientific decisions, final integration, review, and final submissions.

Historical five-person assignments must remain intact in archival and attribution materials but must not be presented as current assignments.

Do not infer actual contribution credit from assigned folder ownership.

### K. Single centralized data pipeline

DELTA owns the authoritative data producer.

DEVGRU and SAS consume its approved outputs.

No model owner should independently redefine:

- Target construction.
- Sample selection.
- Target eligibility.
- Historical feature windows.
- Train/validation/test boundaries.
- Shared evaluation keys.
- Shared evaluation metrics.

All model outputs must follow one standardized prediction schema approved by the group.

---

## 3. ESTABLISH A SINGLE SOURCE OF TRUTH FOR ALL LLMS

This is a high-priority requirement.

All three teammates use AI coding assistants extensively. Different assistants must not invent separate methodologies.

Establish the following documentation hierarchy:

1. `docs/experiment_protocol.md` — authoritative approved scientific methodology.
2. `docs/interfaces.md` — shared feature, target, split, and prediction contracts.
3. `docs/team_responsibilities.md` — active implementation ownership.
4. `configs/*.yaml` — machine-readable representations of approved experiment settings.
5. `context.md` — concise current project state and handoff summary.
6. `docs/experiment_log.md` — dated decisions and experiment history.
7. Other READMEs — navigation and workstream-specific guidance.
8. `archive/` — historical reference only, NEVER current protocol authority.

Follow existing repository-level instructions and make any ambiguity in precedence explicit.

Do not copy the entire scientific protocol into multiple files.

Instead, use short summaries with links to authoritative documents.

### Update AGENTS.md

Make `AGENTS.md` the concise, cross-tool agent guidance.

It should instruct any AI assistant to:

- Read the current project context and approved scientific protocol before proposing changes.
- Read the relevant interfaces and workstream README.
- Respect the active DELTA/DEVGRU/SAS ownership map.
- Distinguish APPROVED, PROPOSED, PENDING, IMPLEMENTED, and HISTORICAL decisions.
- Never treat unimplemented documentation as executable functionality.
- Never treat the historical pilot's results as new final-experiment results.
- Never silently change the target, sample, features, cohort rules, or splits.
- Never use target-day stockout status as an input predictor.
- Preserve matching observation keys across models.
- Follow train-only preprocessing, validation-only tuning, and test-isolation rules.
- Never edit archival evidence when making active project changes.
- Avoid changing another owner's workstream without appropriate coordination.
- Clearly identify which experiment version a generated artifact belongs to.
- Update documentation and the experiment log when an approved scientific decision changes.
- Flag contradictions rather than choosing a conflicting rule silently.

Keep the instructions concise and operational.

### Update context.md

Make it a reliable project-resumption document for any LLM starting a fresh session.

Include:

- Project goal.
- Current three-person ownership.
- Approved scientific decisions.
- Current implementation status.
- What is historical versus new.
- Main source-of-truth file paths.
- Pending technical implementation and verification tasks.
- Next cross-team dependencies.

Remove stale claims that the repository migration has not merged, if Git confirms it has merged.

### Update starter_prompt.md

Create a concise, reusable startup prompt that team members can paste into Codex, Copilot, or another LLM.

It should instruct the assistant to:

1. Inspect the repository and Git state.
2. Read `AGENTS.md`, `context.md`, `docs/experiment_protocol.md`, and `docs/interfaces.md`.
3. Read the relevant owner folder README.
4. Summarize the current approved design and implementation status.
5. Identify the requested workstream and its dependencies.
6. Highlight conflicts or missing decisions before implementing changes.
7. Avoid making unrelated changes.

### Tool-specific instructions

Inspect whether the repository already contains:

- `.github/copilot-instructions.md`
- `CLAUDE.md`
- Other AI-assistant guidance files.

If GitHub Copilot instructions are absent, create a short `.github/copilot-instructions.md` that points to the common project protocol and ownership documents.

If Claude-specific instructions already exist, align them with the same hierarchy.

Do not create unnecessary duplicate full-length policies for every assistant.

The goal is compatibility across tools, not maintaining separate methodologies.

---

## 4. UPDATE THE RELEVANT ACTIVE DOCUMENTATION

Revise the necessary active Markdown files so they consistently represent the newly approved methodology.

Prioritize:

- Root `README.md`
- `AGENTS.md`
- `context.md`
- `starter_prompt.md`
- `docs/experiment_protocol.md`
- `docs/interfaces.md`
- `docs/team_responsibilities.md`
- `docs/methodology.md`
- `docs/experiment_log.md`
- `src/data_preprocessing_DELTA/README.md`
- `src/features_DELTA/README.md`
- `src/models/baselines_DELTA/README.md`
- `src/models/linear_regression_DEVGRU/README.md`
- `src/models/ridge_regression_DEVGRU/README.md`
- `src/models/decision_tree_SAS/README.md`
- `src/models/random_forest_SAS/README.md`
- `src/evaluation_SAS/README.md`
- Relevant data, notebook, and result README files.

Do not rewrite files that are already accurate.

Use small, targeted updates.

Do not alter archival, original handoff, or historical prompt contents.

If a historical document contains superseded assumptions, preserve the original and add a current reference from an active document rather than rewriting history.

### Required protocol statuses

Clearly distinguish:

- **APPROVED:** The group-approved scientific decisions listed in this task.
- **PENDING VERIFICATION:** Raw-data provenance, precise stockout-hour semantics/indexing, exact generated sample, environment compatibility.
- **DRAFT CONTRACT:** Any technical schema not yet fully specified and validated.
- **NOT IMPLEMENTED:** New feature bundles, 1,000-series sample, final model runs, and final evaluation.
- **HISTORICAL:** Previous 200-series experiments and their results.

The scientific design is approved. This does not mean every technical implementation detail has been finalized.

---

## 5. SYNCHRONIZE YAML CONFIGURATIONS

Update only the necessary metadata in:

- `configs/dataset.yaml`
- `configs/experiments.yaml`
- `configs/models.yaml`

These configurations must agree with `docs/experiment_protocol.md`.

Represent:

- Recorded-sales target.
- 200-series development pilot.
- 1,000-series final sample.
- Seed and reproducible selection requirements.
- 14-day primary historical lookback.
- Chronological split boundaries.
- All eligible target dates as the primary evaluation.
- Fully stocked and stockout target dates as secondary evaluation groups.
- The approved feature-condition design.
- Required baselines.
- Core and extension models.
- Primary and secondary metrics.
- Pending semantic verification.
- Protocol approval versus technical-contract completion.

Do not leave an active field that still makes `stock_hour6_22_cnt == 0` a required PRIMARY eligibility condition.

Preserve compatibility with existing configuration structure where possible.

Do not invent runtime support for configuration fields that no source code currently consumes.

Do not set an implementation or technical-contract freeze flag to TRUE merely because the scientific methodology has been approved.

If a new field is required, document its meaning clearly and identify whether it is metadata-only.

---

## 6. DEFINE THE SHARED DATA AND PREDICTION CONTRACT

Update `docs/interfaces.md`.

Specify the minimum agreed conceptual requirements for the shared datasets.

At minimum, every modeling observation needs:

- Store identifier.
- Product identifier.
- Target date.
- Target recorded sales.
- Chronological split.
- Sales-only predictor set.
- Historical stockout predictor set.
- Stable observation key.

The evaluation system also needs retrospective target-day stockout information to define the stocked/stockout subgroups.

This subgroup metadata must be kept OUT of the predictive feature allowlists.

Document that:

- Sales-only and stockout-aware conditions must share identical observation keys and target values.
- Different model families must use compatible train/validation/test observations.
- Baseline predictions use the same evaluation population.
- Model outputs identify the model, feature condition, split, observation key, actual target, and prediction.
- Runs should record experiment version, sample manifest, features, hyperparameters, random seed, and source revision.
- The evaluator must check missing keys, duplicate keys, split inconsistencies, and target mismatches.

Use existing field names where the repository has already established them.

If exact filenames or schemas are not agreed, label them DRAFT rather than inventing approval.

Do not create or regenerate feature tables as part of this task.

---

## 7. RECORD THE DECISION PROPERLY

Add a dated, versioned decision entry to `docs/experiment_log.md`, using the current repository date.

Record:

- The three-member agreement.
- The change from stockout-free primary targets to all eligible primary targets.
- Secondary stocked/stockout subgroup evaluation.
- 200-series development and 1,000-series final design.
- 14-day primary feature window.
- Core models and extensions.
- DELTA's ownership of centralized data and features.
- Shared interfaces and fair model comparisons.
- Outstanding technical validation tasks.
- The fact that implementation and final results are pending.

If useful, add one concise decision record under `docs/decisions/`, linked from the experiment log.

Do not claim that new experiments have been executed or that performance has improved.

---

## 8. CONSISTENCY AUDIT AFTER EDITING

After making the documentation updates, scan the entire active repository for outdated or conflicting statements.

Check especially for:

- Claims that the primary experiment excludes stockout target days.
- Claims that target-day stockout information is a model feature.
- References to 200 series as the final sample.
- References to 1,000 series as an already generated dataset.
- References to 7/14/28 comparisons as required primary experiments.
- Five-person assignments presented as current ownership.
- Ridge and Random Forest presented as prohibited models.
- Inconsistent chronological split boundaries.
- Conflicting prediction targets.
- Inconsistent definitions of bias.
- References to nonexistent implemented models or feature bundles.
- Stale claims that the already-merged migration is still pending.
- Conflicting instructions among AI-agent guidance files.
- Statements that old pilot results are final results from the redesigned experiment.

Historical archives may retain their original statements. Do not flag historical text as an active contradiction when it is clearly identified as historical.

Do not remove legitimate limitations or uncertainty merely to make the documentation appear consistent.

Run lightweight, read-only verification where appropriate, including Markdown link/path checks, YAML parsing, and existing static repository tests.

Do not run model training or data preprocessing.

---

## 9. OUTPUT REQUIREMENTS

Make the documentation edits directly in the current working tree.

Do not commit or push.

At the end, provide:

### A. Files changed

List every modified or newly created file and explain why it changed.

### B. Approved methodology summary

Summarize the finalized research question, target, cohort strategy, dataset sizes, feature sets, model scope, evaluation, and ownership.

### C. Cross-LLM consistency

Explain how Codex, Copilot, and other coding assistants will find the same authoritative instructions.

### D. Remaining technical decisions

List only genuinely unresolved matters, distinguishing implementation details from already approved research decisions.

### E. Validation results

Report which checks passed, failed, or were unavailable.

### F. Git diff summary

Show the changed-file summary and verify that no ML source code, datasets, historical archives, or generated results were modified.

### G. Final status

Answer:

**Is the repository now documentation-aligned with the approved DATA 245 experimental design, and can DELTA, DEVGRU, and SAS begin implementing against the same scientific protocol?**

Be precise. Do not claim full implementation readiness if technical interface details remain in draft.

**FINAL CONSTRAINT: This task updates documentation, AI guidance, and YAML metadata only. No ML implementation, training, dataset migration, experiment execution, commits, or pushes.**