# Baselines — DELTA

Existing persistence and preceding-seven-day-mean implementations remain together in the adapted legacy preparation script under `src/data_preprocessing_DELTA/`. Their original results are in `results/baselines_DELTA/inherited/`; the raw pipeline and scores have not been independently reproduced.

Future task: produce baseline predictions on exactly the matched eligible keys from the verified feature bundle, in the shared prediction format. Save new runs separately. Only persistence and the 7-day mean are required. Historical lag-7 and stocked-history-mean ideas are outside the core task, not implemented or required. Do not copy the inherited all-row scores into the matched comparison.

Follow the [approved v2 protocol](../../../docs/experiment_protocol.md) and [draft shared contract](../../../docs/interfaces.md). Real runs use DELTA's same verified development/final bundle and target keys, including otherwise eligible stockout target dates; subgroup labels are evaluation-only. V1 evidence/tests are now separate from active V2 checks; finalize the draft technical interface before implementation. Git ancestry integration remains pending.
