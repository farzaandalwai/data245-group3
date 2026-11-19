Act as a senior Git integration engineer and machine learning research engineer.

We are reconciling our approved DATA 245 V2 methodology with the remote V1 contract and validation work.

The repository is currently on `main`. Our V2 documentation changes have been committed locally, and the remote changes have been fetched/merged or are awaiting conflict resolution.

**Your task is to complete the semantic reconciliation, not merely make Git conflicts disappear.**

First inspect the actual Git state and existing merge status. Do not assume the merge succeeded.

## Approved V2 methodology

- Target: next-day normalized recorded `sale_amount`.
- Primary cohort: all otherwise eligible target dates, including stockout days.
- Secondary evaluation: fully stocked versus stockout target dates.
- Development sample: 200 complete series.
- Final sample: 1,000 complete series, not yet generated.
- Maximum primary lookback: 14 days.
- First candidate target: day 15.
- Splits: days 1–60 train, 61–75 validation, 76–90 test.
- Sales-only: sales lags 1/2/3/7/14, prior 7/14-day sales means, weekday, weekend.
- Stockout-aware: identical shared features plus previous-day stockout hours, prior 7/14-day stockout-hour means, and prior 7/14-day stockout-day proportions.
- Store/product IDs: observation keys, not approved model predictors.
- Core models: Linear Regression and Decision Tree.
- Extensions: Ridge and Random Forest.
- Baselines: persistence and prior 7-day mean.
- Metrics: MAE, RMSE, signed prediction bias.
- Ownership: DELTA data/features/baselines, DEVGRU linear/Ridge, SAS trees/evaluation.

These decisions are approved and must not be silently replaced with V1 assumptions.

## Reconciliation requirements

1. Preserve the useful remote safe binary parser, endpoint checks, source references, provenance, matching-key checks, and validation safeguards.
2. Preserve the V1 contract, stockout audit, and four-entry integrity lock as clearly labeled historical artifacts.
3. Do not treat the historical V1 integrity lock as the active V2 scientific authority.
4. Update active contract registration in `pyproject.toml` where needed.
5. Ensure `docs/experiment_protocol.md`, `docs/interfaces.md`, `configs/*.yaml`, `AGENTS.md`, and `context.md` agree.
6. Update `test_shared_contract.py` so active tests validate the V2 methodology instead of enforcing the obsolete V1 target filter, 28-day history, or disabled extensions.
7. Preserve historical V1 reproduction tests separately where appropriate.
8. Review `scripts/audit_contract.py`. Do not reuse its V1 eligibility assumptions as active V2 rules.
9. Keep technical details that remain unresolved explicitly labeled DRAFT or PENDING VERIFICATION.
10. Do not claim that final datasets, feature bundles, or model experiments have already been generated.

Run all applicable static checks, YAML consistency checks, and contract tests.

If the merge is still unresolved, resolve conflicts carefully and stage the reconciled files, but do not finalize a merge commit without reporting the resolved changes.

Do not run ML training or preprocessing, alter original experimental evidence, reset Git history, force-push, or push to GitHub.

## Final output

Report:

1. Files changed.
2. Conflicts resolved.
3. Remote V1 functionality preserved.
4. Superseded active assumptions removed.
5. Test results.
6. Remaining unresolved technical decisions.
7. Whether the repository is ready for a normal push to `main`.

Keep the response concise and prioritize token efficiency.
