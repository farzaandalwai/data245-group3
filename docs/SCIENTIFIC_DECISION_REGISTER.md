# Scientific and technical decision register

Register date: 2026-11-20
Status: **DRAFT CONTRACT; NO FINAL-SCORING AUTHORIZATION**

The v2 scientific protocol is approved. The decisions below concern the still-draft shared technical contract and integration workflow. They are not silently frozen by this register.

| Decision | Current implementation/evidence | Proposed options | Responsible agreement | Status | Consequence if unresolved |
|---|---|---|---|---|---|
| Predictor scaling | DEVGRU standardizes using training rows; SAS tree uses no scaling | Standardize Linear/Ridge only; retain tree-native behavior; document whether this is model-specific | Shoury, Farzaan, Timothy | NEEDS TEAM APPROVAL | Final cross-model settings cannot be frozen |
| Ridge grid | `[0.01, 0.1, 1, 10, 100]`; selected by validation MAE | Accept grid or revise before final run; equal condition budgets required | Shoury with team review | NEEDS TEAM APPROVAL | No final Ridge alpha may be selected |
| Tree grid | 12 ordered depth/leaf candidates | Accept provisional SAS grid or jointly revise | Farzaan with team review | NEEDS TEAM APPROVAL | Tree final settings remain provisional |
| Tune budget | Equal per-condition budget within each DEVGRU/SAS family | Freeze candidate count and parameter space per family | All three owners | NEEDS TEAM APPROVAL | Paired comparison may be unfair if budgets differ |
| Selection metric | Validation MAE for DEVGRU and SAS tree | Freeze MAE as sole selection metric; use RMSE/bias descriptively | All three owners | PROPOSED / PROTOCOL-CONSISTENT | Selection policy remains draft |
| Exact tie-breaking | DEVGRU chooses smaller Ridge alpha; SAS chooses first declared grid candidate | Choose one shared policy or document model-family-specific policy | All three owners | NEEDS TEAM APPROVAL | Reproducibility differs across model families |
| Prediction clipping | DEVGRU and SAS preserve finite raw predictions; negative counts are 9 Linear and 6 Ridge | No clipping, or jointly approve identical nonnegative clipping before comparison | All three owners | NEEDS TEAM APPROVAL | Existing validation numbers cannot be reused after clipping |
| Bootstrap cluster unit | DEVGRU evidence resamples 200 store-product series; SAS/shared v2 procedure resamples whole stores | Adopt one shared unit; protocol/SAS currently favors store clusters | Timothy, Farzaan, Shoury | NEEDS TEAM APPROVAL | DEVGRU and SAS intervals are not directly comparable |
| Bootstrap repetitions | 2,000 in DEVGRU and SAS evidence | Retain 2,000 | All three owners | PROPOSED | Uncertainty evidence cannot be standardized |
| Bootstrap CI | Percentile 95%; DEVGRU seeds 245/246 by model, SAS uses seed 245 per comparison | Freeze seed policy, quantile method, and whether seed is per model | All three owners | NEEDS TEAM APPROVAL | Reproduction may differ despite identical predictions |
| Subgroup analysis | SAS joins retrospective target-day groups after prediction; DEVGRU artifacts do not contain subgroup results | Use common evaluator subgroup outputs only after prediction validation | Farzaan with DELTA acceptance | PROPOSED | Secondary claims remain incomplete |
| Multiple comparisons | No multiplicity adjustment is recorded | Descriptive intervals only, or pre-specify a multiplicity policy | All three owners | NEEDS TEAM APPROVAL | Do not call any tiny improvement statistically established |
| Missing/closed-hour semantics | DELTA says business semantics remain provisional; producer checks are operational | Timothy documents accepted semantics/export lineage | Timothy | NEEDS TEAM APPROVAL | Final interpretation and export semantics remain limited |
| Scaling coefficient / normalization | `actual` is normalized recorded `sale_amount`; exact coefficient lineage remains pending | DELTA accepts final normalization/export semantics | Timothy | NEEDS TEAM APPROVAL | Do not describe target as latent demand or food waste |
| Export and handoff semantics | DEVGRU files are valid exchange CSVs but not in the SAS combined-run envelope | Agree manifest/run layout and consumer path | Timothy, Farzaan, Shoury | NEEDS TEAM APPROVAL | Direct integration is blocked |

## Required freeze gate

Before any final-bundle access or test prediction, the team must accept the final bundle/hash, preprocessing rules, model grids and budgets, tie behavior, postprocessing, uncertainty procedure, run manifest shape, and export semantics. `configs/contract.yaml` currently records `contract_frozen: false` and `new_model_test_evaluation_allowed: false`.
