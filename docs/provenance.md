# Import provenance

Imported on 2026-11-18 (America/Los_Angeles). UTC timestamps below come from the actual imports. Sources were resolved from current accessible Drive folder listings before download. All ten non-raw requested files were acquired; the raw CSV was intentionally not downloaded.

Primary source: [team Drive folder](https://drive.google.com/drive/folders/1_saUNK4VOT7vpbSjiCw2XKIOpWa3IkHy). The handoff README states that Timothy Tran completed the preparation/pilot/baseline work. That stated authorship is retained for the imported handoff; Drive ownership is not treated as proof of authorship. This is an import, not a new execution or independent reproduction.

The Drive root has a `processed/` folder. It was initially mapped to `data/processed/` to preserve the handoff layout. That original relative layout is now preserved inside `archive/original_pilot/`; canonical working manifest/results and adapted code paths follow the migration record. The original README is archived instead of replacing the project root README.

## Original files — initial import destinations

The headings and `Local destination` values below record the initial bootstrap layout. After the authorized structure migration, all ten source originals are under `archive/original_pilot/`. Their current archive/working paths are listed per entry and in the import manifest; initial import time/size/hash/author facts remain unchanged.

### docs/handoff/README.original.md

- Source: [README.md](https://drive.google.com/file/d/1s4QCLKaMtMlyQXNMzqNr-SqGCCaN7hJm/view?usp=drivesdk).
- Drive ID: `1s4QCLKaMtMlyQXNMzqNr-SqGCCaN7hJm`; MIME: `text/markdown`.
- Local destination: `docs/handoff/README.original.md`.
- Current preserved original: `archive/original_pilot/README.md`.
- Current working destination: `docs/handoff/README.original.md` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:46.976603+00:00`.
- Bytes: 23414; reviewed expected and current folder metadata both matched.
- SHA-256: `203e60646d0bba620b1586eb558c0dcc67f00b05ff1f0c192985c3749b61f4c3`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### results/data_audit.txt

- Source: [data_audit.txt](https://drive.google.com/file/d/1X-GjOXS9qZOzuS4indgQHoxVFLhuNzgB/view?usp=drivesdk).
- Drive ID: `1X-GjOXS9qZOzuS4indgQHoxVFLhuNzgB`; MIME: `text/plain`.
- Local destination: `results/data_audit.txt`.
- Current preserved original: `archive/original_pilot/results/data_audit.txt`.
- Current working destination: `results/baselines_DELTA/inherited/data_audit.txt` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.130525+00:00`.
- Bytes: 1554; reviewed expected and current folder metadata both matched.
- SHA-256: `f125d8d216659cda8aef7e62360b86002bdada9fdd82bba54a55bb78791a6495`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### results/baseline_metrics.csv

- Source: [baseline_metrics.csv](https://drive.google.com/file/d/1KXGtfJJaczk2IyAW4FO0bOvWwQjGCvZZ/view?usp=drivesdk).
- Drive ID: `1KXGtfJJaczk2IyAW4FO0bOvWwQjGCvZZ`; MIME: `text/csv`.
- Local destination: `results/baseline_metrics.csv`.
- Current preserved original: `archive/original_pilot/results/baseline_metrics.csv`.
- Current working destination: `results/baselines_DELTA/inherited/baseline_metrics.csv` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.211040+00:00`.
- Bytes: 259; reviewed expected and current folder metadata both matched.
- SHA-256: `e753a6971d6a0c92ecc6c295696ad76fcc05ae7403283be936ee15e05d212d20`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### results/baseline_predictions.csv

- Source: [baseline_predictions.csv](https://drive.google.com/file/d/1TNVSGdXWIK6ZlooaLg8fuZWXyfUqN5aP/view?usp=drivesdk).
- Drive ID: `1TNVSGdXWIK6ZlooaLg8fuZWXyfUqN5aP`; MIME: `text/csv`.
- Local destination: `results/baseline_predictions.csv`.
- Current preserved original: `archive/original_pilot/results/baseline_predictions.csv`.
- Current working destination: `results/baselines_DELTA/inherited/baseline_predictions.csv` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.382452+00:00`.
- Bytes: 697664; reviewed expected and current folder metadata both matched.
- SHA-256: `347161e45c49cd64d5cddfa24b35a5ee620b564ed5e9070a73036fba2afa73b1`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data/processed/pilot_200_series.csv

- Source: [pilot_200_series.csv](https://drive.google.com/file/d/18tq2qwOTpe4ViAQ_KowK0zsl9aZAw1RS/view?usp=drivesdk).
- Drive ID: `18tq2qwOTpe4ViAQ_KowK0zsl9aZAw1RS`; MIME: `text/csv`.
- Local destination: `data/processed/pilot_200_series.csv`.
- Current preserved original: `archive/original_pilot/data/processed/pilot_200_series.csv`.
- Current working destination: `data/processed/pilot_200_series.csv` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.795789+00:00`.
- Bytes: 4530605; reviewed expected and current folder metadata both matched.
- SHA-256: `de303b3f079b0258f15cbbcde14ab0d5e8a4bfb1f24756eb6b277e1bc7c8311f`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data/processed/pilot_series_manifest.csv

- Source: [pilot_series_manifest.csv](https://drive.google.com/file/d/1vxeoaH9ztGB9O3krxgCyaaue7xIByO47/view?usp=drivesdk).
- Drive ID: `1vxeoaH9ztGB9O3krxgCyaaue7xIByO47`; MIME: `text/csv`.
- Local destination: `data/processed/pilot_series_manifest.csv`.
- Current preserved original: `archive/original_pilot/data/processed/pilot_series_manifest.csv`.
- Current working destination: `data/manifests/pilot_series_manifest.csv` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.883106+00:00`.
- Bytes: 1738; reviewed expected and current folder metadata both matched.
- SHA-256: `8b7a5377c95e56e63ad5143cc8dc8a38ecc35032f64e2cfbbb8ae66d25519a42`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data/processed/excluded_series.csv

- Source: [excluded_series.csv](https://drive.google.com/file/d/11HF5MPpiqHXId2tPmAz_q6Rzu950utbe/view?usp=drivesdk).
- Drive ID: `11HF5MPpiqHXId2tPmAz_q6Rzu950utbe`; MIME: `text/csv`.
- Local destination: `data/processed/excluded_series.csv`.
- Current preserved original: `archive/original_pilot/data/processed/excluded_series.csv`.
- Current working destination: `data/manifests/excluded_series.csv` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:47.951084+00:00`.
- Bytes: 775; reviewed expected and current folder metadata both matched.
- SHA-256: `75b3b3787d4ca0ba8dd12c926ebc6aafc5f0628f3c831c543335ed1d312d3d81`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data_prep_pipeline/prepare_and_baselines.ipynb

- Source: [prepare_and_baselines.ipynb](https://drive.google.com/file/d/1UCl-qTyEnL8PFfnVH6kmFTXeiqbSX4kr/view?usp=drivesdk).
- Drive ID: `1UCl-qTyEnL8PFfnVH6kmFTXeiqbSX4kr`; MIME: `application/octet-stream`.
- Local destination: `data_prep_pipeline/prepare_and_baselines.ipynb`.
- Current preserved original: `archive/original_pilot/data_prep_pipeline/prepare_and_baselines.ipynb`.
- Current working destination: `notebooks/DELTA_data/prepare_and_baselines.ipynb` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:48.043375+00:00`.
- Bytes: 51210; reviewed expected and current folder metadata both matched.
- SHA-256: `04494a70255aab7ff9d69eb8e8a21c89c60a6a364b53d26b25396380f442d071`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data_prep_pipeline/prepare_and_baselines.py

- Source: [prepare_and_baselines.py](https://drive.google.com/file/d/1jXMsK0fI0s2ofzvJmgX9Kdt20HAzpUwa/view?usp=drivesdk).
- Drive ID: `1jXMsK0fI0s2ofzvJmgX9Kdt20HAzpUwa`; MIME: `text/x-python`.
- Local destination: `data_prep_pipeline/prepare_and_baselines.py`.
- Current preserved original: `archive/original_pilot/data_prep_pipeline/prepare_and_baselines.py`.
- Current working destination: `src/data_preprocessing_DELTA/prepare_and_baselines.py` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:48.118357+00:00`.
- Bytes: 7958; reviewed expected and current folder metadata both matched.
- SHA-256: `5afb9a400f25b40a4bb0dbfdbdf501641541180adf8c953039871359d0e8857c`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

### data_prep_pipeline/data_explore.py

- Source: [data_explore.py](https://drive.google.com/file/d/1mnInCx3wX1WN8-G0xIMimQssWbgYiRbW/view?usp=drivesdk).
- Drive ID: `1mnInCx3wX1WN8-G0xIMimQssWbgYiRbW`; MIME: `text/x-python`.
- Local destination: `data_prep_pipeline/data_explore.py`.
- Current preserved original: `archive/original_pilot/data_prep_pipeline/data_explore.py`.
- Current working destination: `src/data_preprocessing_DELTA/data_explore.py` (path-adapted for code/notebook; unchanged bytes for data/results).
- Import time (UTC): `2026-11-19T05:55:48.191879+00:00`.
- Bytes: 299; reviewed expected and current folder metadata both matched.
- SHA-256: `e5773e47496dbbf4e53f15c6e53c71a26d6ab8d1381d71c9032f5805a6927274`.
- Original author as stated: Timothy Tran (handoff attribution); upstream dataset creator Dingdong-Inc for underlying data.
- Verification: original bytes preserved; download size and local hash checked. No independently supplied historical hash exists. Syntax/JSON/schema and key checks are described in [setup verification](setup_verification.md); raw pipeline and metrics were not rerun.

## Derived reading copy and setup prompt

`docs/handoff/README.original.md` retains the UTF-16 BOM and original bytes. `docs/handoff/README.utf8.md` was produced by decoding UTF-16 and encoding UTF-8, retaining text/line endings. Only encoding changed; the original remains the authority for byte preservation.

- UTF-8 reading-copy bytes: 11714.
- UTF-8 reading-copy SHA-256: `181a897097ef1024de4d3cf1bdbc21a46f954c5dcb6763d05ac528a91f4dd198`.
- Conversion by Codex during setup; text equality checked without executing source instructions as standalone tasks.

The user-supplied setup prompt was copied unchanged from `/Users/farzu/Downloads/DATA245_Codex_Setup_Prompt.md` to `docs/prompts/DATA245_Codex_Setup_Prompt.md` on 2026-11-18. Its author is not named in the file; it was supplied and explicitly authorized by the user. It is not a record of earlier unseen conversations.

- Prompt bytes: 25097.
- Prompt SHA-256: `ebb06ae09e97d8f5f9881796a5bcafdb5366c26bb273c5ca5d72bcc7da191dd5`.

## Intentionally unavailable or deferred

- Raw export (old documented destination `data/freshretail.csv`, current `data/raw/freshretail.csv`): Drive ID `1A0nGSmtUDzAi_AGHYbuoxzNub4yLcubL`, [canonical source](https://drive.google.com/file/d/1A0nGSmtUDzAi_AGHYbuoxzNub4yLcubL/view?usp=drivesdk), current metadata 323,577,557 bytes. Not downloaded, not hashed, and ignored. Raw author/export lineage is stated by the handoff; full raw contents were not independently inspected. See [data acquisition](../data/README.md).
- Original proposal, intermediate report, and professor starter code: not supplied as separate files in this import; no content or hashes invented. The supplied setup prompt is the design/course-requirement source until checked against Canvas.
- Drive `experiments/` folder: accessible listing was empty during setup. No remaining experiments were imported or implemented.

## Rights and attribution status

The official [dataset card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K/blob/main/README.md#licenseterms-of-use) was checked on 2026-11-18 and states CC BY 4.0. [Data attribution and modification notice](../data/README.md#attribution-and-permitted-redistribution) documents the upstream developer, license link, and team transformations before committing the small extracts. Their source bytes were not changed by setup. The source card does not establish which upstream revision produced the local export; that lineage remains unverified.

`.gitattributes` disables line-ending normalization for imported originals, the reading copy, and the supplied prompt so Git preserves the recorded bytes on all clones. Staged blobs are compared individually against working files before the bootstrap commit.

No blanket license was applied to teammate code or third-party data. Import commits use the authenticated project owner's existing Git identity for the import operation, without fabricated teammate commits or AI co-author trailers. Imported authorship is recorded here and in [contributions](contributions.md).

## Authorized structure migration

The user explicitly changed the active team to three and requested codename-based folders: DELTA, DEVGRU, SAS, with identities in `context.md`. Historical source authorship is unchanged. The [migration record](structure_migration.md) explains path changes and separates byte-identical originals/data from derived working code. [migration_manifest.json](handoff/migration_manifest.json) records migration-time paths, byte counts, hashes, and adaptation status. Working notebook execution state was cleared; its original outputs remain archived. No raw pipeline, feature producer, model, scoring, or new result was executed.
