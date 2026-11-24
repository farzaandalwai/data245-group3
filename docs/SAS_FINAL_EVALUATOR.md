# SAS final-evaluator repair — 2026-11-24 (NOT READY FOR FINAL SCORING)

Owner: SAS / Farzaan Dalwai. Branch `SAS/final-evaluator-repair` from `main` `18d21d5`.
Requested by DELTA (Tim) review and PR #10's dependency list. **Status: IMPLEMENTED and
synthetic-tested; BLOCKED.** No real final or test scoring was run, no approval flag was
changed, no team approval is claimed, and no original evidence was edited.

## Why a repair was needed
`scripts/final_evaluation.py` (added in Shoury's commit `91fab8d`, merged with PR #6) has
four problems:
1. **Wrong gate:** it reads the historical V1 lock `configs/contract.lock.json`, not the V2
   flags in `configs/contract.yaml` or `scripts/sas_final_preflight.py`.
2. **Wrong bootstrap weighting:** it averages per-store mean differences (each store weighted
   equally), so its intervals do not match its pooled-row point estimate or the approved
   pooled-row store bootstrap.
3. **Unapproved hardcoded settings:** Ridge alpha 10/100 and Tree depth 5 / leaf 5 are the
   200-series development selections, never jointly frozen; Random Forest is excluded.
4. **No shared checks / unsafe writes:** no exact key, actual and split validation beyond a row
   count, and outputs are written directly into the destination.

That script is **left byte-for-byte unchanged**, because `submission_local/` cites it for a
claimed Nov 20 final run (`results/final_evaluation/v2/final-authorized-20261120-r1/`). Those
outputs are not in Git, the V2 gates were closed, and no freeze was recorded. Its results are
unverified and are not used here. A test asserts the legacy file still matches `91fab8d`.

## What the repair provides
- `src/evaluation_SAS/final.py`, the single reviewed final path:
  - **V2 gates:** all three `configs/contract.yaml` flags, plus `configs/final_settings.json`
    with `approved: true`, status `APPROVED`, recorded DELTA/DEVGRU/SAS approvals and a freeze
    record. The bundle manifest hash and purpose must also match the settings. These are
    checked from configuration and the manifest header **before any outcome CSV is opened**.
  - **Shared checks:** `validate_predictions` (exact keys, actuals and splits for every
    model/condition, all three splits) and `validate_metadata`, plus the shared metrics.
  - **Pooled-row paired store bootstrap:** the same core as development, factored out of
    `src/evaluation_SAS/bootstrap.py` with no behaviour change (95%, 2,000 replicates, seed 245,
    pooled row denominator). A test proves it equals the development function and differs from
    a store-mean average when store sizes differ.
  - **Frozen settings file:** models are fitted on train only with the file's settings; there is
    no final tuning. Clipping, changed uncertainty settings and dropped required models are all
    rejected.
  - **Optional Random Forest:** included only when `random_forest.enabled` is true.
  - **Safe output:** transactional publish into a new directory, overwrite refused, with
    artifact hashes, settings hash, source and environment recorded in the manifest.
- `scripts/sas_final_evaluation.py`: `check` (configuration only) and `run` (blocked until
  approved). `scripts/sas_final_preflight.py` now names this as the entry point and adds the
  settings gates.
- `configs/final_settings.json`: **PROPOSED_NOT_APPROVED** (`approved: false`, no approvals, no
  freeze record). Its values are the recorded development selections, labeled as proposals.

## Checks actually run (synthetic only)
- `python3 -m unittest discover -s tests`: **114 passed** (11 new in `tests/test_sas_final.py`;
  one preflight assertion updated for the new blockers).
- `python3 scripts/verify_setup.py`: passed.
- `python3 -m scripts.sas_final_preflight` and `python3 -m scripts.sas_final_evaluation check`:
  both exit **2 (blocked)**: three contract flags, settings not approved, approvals missing,
  freeze record missing.
- The real final bundle was not downloaded or opened.

## Remaining blockers (team, not SAS code)
1. A joint freeze: confirm or change the proposed settings, decide on Random Forest, tie rules,
   and whether to re-select on the final validation split (this evaluator does not), then record
   the approvals and freeze record in the settings file.
2. Flip the V2 contract flags only after that freeze, in a reviewed change.
3. Decide how to handle the claimed Nov 20 run: share its output folder for audit and disclose
   that the final test split was already scored once, before the freeze.
4. Human review of this PR. Then run `python3 -m scripts.sas_final_evaluation run --bundle
   data/processed/feature_bundles/v2-final-1000-r2 --output results/final_evaluation/v2/<new-id>
   --run-id <new-id>` exactly once.
