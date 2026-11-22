# Submission Blockers

## Final scoring completed with limitations

- The frozen contract and final-scoring preflight passed before the authorized run.
- Final predictions and metrics are in `results/final_evaluation/v2/final-authorized-20261120-r1/`.
- Random Forest was not retained because its optional test suite remained runtime-inconclusive.
- Historical pilot/holdout exposure is documented, so the final holdout is not pristine confirmatory evidence.

## BLOCKED: executable verification

- The current `.venv` imports `numpy 2.5.5`, `pandas 3.1.1`, `scikit-learn 1.9.1`, and `PyYAML 6.0.3`.
- Serialized fitted model binaries are not retained; predictions, manifests, metrics, and frozen configuration are retained.

## NEEDS TEAM APPROVAL

Agreement is still needed on final model grids and matched budgets, preprocessing/standardization and feature-order freeze, tie rules, clipping, bootstrap resampling unit/repetitions/seed/interval method, subgroup and multiple-comparison handling, missing/closed-hour semantics, scaling coefficient, export/business semantics, and final handoff. DELTA must accept the final bundle and business/export semantics.

## Evidence and coursework limitations

- The R3 checksum file validates committed blob bytes, while some current checkout text/CSV bytes differ due to line endings/encoding and assume-unchanged state. Originals were not altered.
- DEVGRU and RF serialized model files are not available here; they must not be fabricated.
- Individual IEEE-template reports/PDFs, LaTeX sources, rubric appendices, literature survey, lessons learned, GenAI disclosures, CRediT records, presentation, and human review records are not present as completed submissions in this execution copy.
