# Baselines — DELTA

Existing persistence and preceding-seven-day-mean implementations remain together in the adapted legacy preparation script under `src/data_preprocessing_DELTA/`. Their original results are in `results/baselines_DELTA/inherited/`; the raw pipeline and scores have not been independently reproduced.

Future task: produce baseline predictions on exactly the matched eligible keys from the verified feature bundle, in the shared prediction format. Save new runs separately. Lag-7 and stocked-history mean/fallback baselines remain planned, not implemented. Do not copy the inherited all-row scores into the matched comparison.
