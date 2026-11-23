# DEVGRU PR #6 provenance and evidence audit

Audit date: 2026-11-20
Scope: original DEVGRU development evidence and the uploaded PR #6 branch
Status: **PASS WITH LIMITATIONS**

## Repository and revision facts

- Current audit branch: `DEVGRU/development-artifacts`
- Evidence branch: `origin/DEVGRU/development-artifacts`
- Evidence packaging commit: `044fac1a9ed0fae52179df25946a5a994f2826b5`
- Current `origin/main`: `c54f9ab1d499e754f77c4a85422445a0614f3850`, merging PR #5
- DEVGRU implementation commit: `aabb56f9dc9c04170f6a1dfda8329faf968d9990`
- Recorded experiment source revision: `d2a323eb2358d6d94f01d2c6fc73c32c00756618`

The evidence branch contains the packaging commit and is not an ancestor of current `origin/main`; no automatic merge was performed. The available Git history confirms the branch and commit relationship, but the GitHub PR #6 page/API was not available through the local command-line tools, so PR open/draft metadata remains **NEEDS TEAM VERIFICATION**.

The recorded experiment revision is the old pre-PR5 base. It is not replaced with the current main or packaging revision. Because the implementation was not committed at that recorded revision, the exact dirty working-tree source used to produce the predictions cannot be established from the available metadata. Provenance is therefore **PARTIALLY ESTABLISHED**, not fabricated as a full source snapshot.

These revisions have distinct meanings:

1. `d2a323e`: revision recorded by the original experiment runner.
2. `043a9d...a7c7`: trusted DELTA development-bundle manifest SHA-256.
3. `044fac1`: later packaging commit for the shared evidence branch.
4. `c54f9ab`: current main after merged PR #5.

## Artifact checksum audit

Source directory: `runs/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/`
Shared directory: `artifacts/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119/`

| Artifact | Source SHA-256 | Shared SHA-256 | Inventory status |
|---|---|---|---|
| `development_report.md` | `ef50e38013d7e158351752cc890e74b99726ac831cc706ea0e052eb59ea56b4b` | same | PASS; inventory correct |
| `paired_validation_comparison.csv` | `63051e6a2bb4d6976f525eeba5e23288d05c3d6c499f910b5f3f598ccf427450` | same | **FAIL corrected**; inventory had malformed `...6f525ee5ae...` |
| `ridge_alpha_selection.csv` | `2b5d4b13a699a1ab3ce09b5f8f2a42613d069977fafa15a5b543079352dcbbb8` | same | PASS; inventory correct |
| `run_metadata.json` | `563c5cbc0e6d31e780d622700c7054aa2dd5e91d2eaa93178837b03726fff713` | same | PASS; inventory correct |
| `validation_metrics.csv` | `7c1032be0b89ad26f5586b266d8aa8e9a6aaf55e9a80e9c1cee90bd69bccbce4` | same | PASS; inventory correct |
| `linear_regression/sales_only.predictions.csv` | `fd2d1d1f30d2d1870f4b1fdb3ead9d1703ff3ed14d410f91e7de62ef440561d7` | same | PASS; inventory correct |
| `linear_regression/stockout_aware.predictions.csv` | `4af534b8fcd8f150d998da99d925bdc1881cc128b46f9218abf720f37754495c` | same | PASS; inventory correct |
| `ridge_regression/sales_only.predictions.csv` | `aaf2b9be37f1ab28d2a54db089ed13ee65ef3daa865cdedd72f26336f2b3785a` | same | PASS; inventory correct |
| `ridge_regression/stockout_aware.predictions.csv` | `54e1547aa462d15fd3d65e2b242a600eaf43f5dbd0401da8acf57438bad518df` | same | PASS; inventory correct |

The shared `INVENTORY.md` was corrected for only the malformed paired-bootstrap checksum. Original experiment files and prediction values were not changed. The ignored original inventory under `runs/` remains preserved as historical evidence.

## Prediction integrity

All four files have the exact exchange schema:

`store_id,product_id,dt,actual,prediction,model,feature_set,split,run_id`

Each has 12,200 rows: 9,200 train, 3,000 validation, and zero test rows. Keys are unique, labels and run IDs match `run_metadata.json`, values are finite, and the bundle identity is `v2-development-200-r2` with trusted manifest SHA-256 `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`.

Independent validation metrics from the original predictions match the stored records. Negative forecasts were not clipped: Linear has 9 negative predictions across its two files and Ridge has 6 across its two files. This is consistent with the documented provisional no-clipping policy.

## Missing artifacts and limitations

- No serialized fitted model files were saved. None were recreated.
- No separate tuning log or bootstrap file exists beyond `ridge_alpha_selection.csv` and `paired_validation_comparison.csv`.
- The exact dirty working-tree source corresponding to recorded revision `d2a323e` is unavailable; reproducibility is based on preserved predictions, metadata, implementation code, bundle identity, and independent calculations.
- The original DEVGRU bootstrap resamples whole store-product series, while the current shared protocol/SAS implementation specifies paired whole-store cluster intervals. The DEVGRU intervals remain valid records of the original development run but are not automatically interchangeable with the shared SAS uncertainty procedure.

## Stale documentation identified

The two DEVGRU-owned model READMEs were corrected in this audit because they still said Linear/Ridge were not implemented. Shared or SAS-owned stale statements were not rewritten:

- `configs/models.yaml` still registers Linear/Ridge as `not_implemented`; this is shared contract metadata and requires team coordination.
- `docs/experiment_protocol.md`, `docs/interfaces.md`, `context.md`, and `README.md` retain historical/pending language that predates the merged DEVGRU implementation; these are shared records and should be updated only through an agreed status/documentation change.
- `docs/SAS_INTEGRATION.md` still says Linear/Ridge implementation is absent or pending verification; Farzaan should update the SAS-owned integration record after accepting the DEVGRU evidence and run-envelope decision.
- `src/evaluation_SAS/README.md` and SAS handoff material describe the evaluator as awaiting accepted DEVGRU predictions; that remains partly accurate because the current four-file DEVGRU package does not yet match the SAS manifest-backed combined-run envelope.

## Conclusion

- Artifact authenticity: **PASS** after inventory checksum correction.
- Prediction integrity: **PASS** for development train/validation evidence.
- Source provenance: **PASS WITH LIMITATIONS**.
- Serialized-model availability: **FAIL / NOT AVAILABLE**, accurately documented.
- Final/test evidence: **BLOCKED** by the technical-contract freeze and task restrictions.
