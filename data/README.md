# Data acquisition and attribution

## What is present

- `processed/pilot_200_series.csv`: exact inherited 200-series, 18,000-row pilot. The 23 columns are the 19 local source columns plus `day_number`, `split`, `pred_persistence`, and `pred_recent_avg_7`. Forecast columns are artifacts, not approved predictors.
- `manifests/pilot_series_manifest.csv`: 200 unique `(store_id, product_id)` pairs. This is the historical development pilot sampling authority; do not regenerate it. The approved final sample will have a separate 1,000-series manifest, generated inside the final feature bundle.
- `manifests/excluded_series.csv`: one excluded 28-day series `(420, 764)` and its missing dates. These are inherited raw-export exclusion details, not a new raw audit.

The pilot's `hours_sale` and `hours_stock_status` fields contain array-like text, including embedded newlines; use a CSV parser, not physical line counts or unrestricted `eval`. V2 verifies the publisher convention (24 binary entries, 1=stockout, indices [6:22]) against every local record; missing/closed-hour business semantics remain provisional. Historical audits are unchanged. Do not infer subgroup parsing rules from casual string inspection. All otherwise eligible stockout target dates enter the primary comparison.

Keys are `(store_id, product_id, dt)`; dates are ISO `YYYY-MM-DD`. Original split counts are train 12,000, validation 3,000, test 3,000. Baseline history columns intentionally have initial missing values; these are distinct from the inherited claim of no nulls in the 19-column raw export.

## Raw export - verified local copy

The team Drive reference remains [freshretail.csv](https://drive.google.com/file/d/1A0nGSmtUDzAi_AGHYbuoxzNub4yLcubL/view?usp=drivesdk). For this task, DELTA copied OLD `data/freshretail.csv` to NEW `data/raw/freshretail.csv`, without altering OLD. Both files measure 323,577,557 bytes and SHA-256 `6d956f6cab0094e794beb97872d9047d7c49469d35044930f5d8a96a307110b5`. Local byte identity is established; the export extraction procedure and exact upstream lineage remain unverified.

Teammates obtain this exact export or the accepted local bundle from DELTA. Verify hashes before use; never overwrite a different dataset. Raw/generated tables are ignored and must never enter Git. Canonical pilot/manifests/inherited results remain unchanged. Legacy reproduction runners were not executed.

The publisher's [Hugging Face dataset](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K) is a source reference. Fetching its current full training split is not equivalent to recovering this smaller local export. `src/data_preprocessing_DELTA/data_explore.py` is a path-adapted historical downloader that would write to `data/raw/freshretail.csv`; it was inspected, not executed. The original working-directory-relative version is archived. Any future download would need dependencies beyond the minimal imported analysis imports and current metadata verification.

## Recovering any missing small handoff file

All ten requested non-raw artifacts were imported during setup. Use [docs/provenance.md](../docs/provenance.md) and [the import manifest](../docs/handoff/import_manifest.json) for exact canonical Drive links, destinations, reviewed sizes, actual sizes, timestamps, and hashes. Restore original bytes, check the recorded hash, and rerun `python3 scripts/verify_setup.py` from the repository root. Do not generate a replacement sample.

## Attribution and permitted redistribution

Dataset: **FreshRetailNet-50K**, developer **Dingdong-Inc**, [official source/data card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K), [technical report](https://arxiv.org/abs/2505.16319). The [data card's license section](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md#licenseterms-of-use) was inspected on 2026-11-18 and states [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), with [legal terms here](https://creativecommons.org/licenses/by/4.0/legalcode). The license permits sharing/adaptation with attribution, license link, and modification notice. Dataset rights remain with their licensors; this private repository does not impose a replacement license or claim endorsement.

Changes from the published dataset: the team supplied a smaller local CSV export, removed an incomplete series, selected a 200-series pilot with seed 245, and added split/day/baseline columns. Timothy Tran's handoff attributes that preparation, selection, and baselines to him. The original setup imported his files byte-for-byte. The later structure migration preserves every original in `archive/original_pilot/`, keeps working data/evidence byte-identical, and adapts only working code/notebook paths and execution-state presentation as documented in `docs/structure_migration.md`. Full export lineage back to an upstream revision was not independently established; no upstream revision hash is invented. Preserve this attribution when sharing extracts and check any later upstream term changes before acquiring new data.

The small pilot, manifest, exclusions, and baseline artifacts are explicitly retained in Git following that source/license check. The raw export, other data, model binaries, and bulky runs stay ignored. Teammate code has no blanket license assigned by this setup.

## Current ownership and handoff

DELTA owns these shared inputs, the implemented shared feature bundles, and matched baseline outputs. DEVGRU and SAS consume one verified bundle; they must not independently resample or redefine feature eligibility. Bundle layout and unresolved contract decisions are in [interfaces](../docs/interfaces.md). Config metadata in `configs/dataset.yaml` records the current canonical paths.

Current local acquisition and bundles: [DELTA handoff](../docs/DELTA_DATA_HANDOFF.md). Raw copy and final input generation are verified; final scoring is pending.
