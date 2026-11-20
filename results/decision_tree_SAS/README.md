# SAS decision-tree regression output

Status: synthetic smoke checks plus real development/validation runs; no final results.
`python3 -m scripts.sas_v2 train-tree` writes immutable ignored runs beneath
`v2/<run_id>/`: predictions, train/validation metrics, candidate/selection evidence,
numeric tree exports, coverage and a hash/provenance manifest. Synthetic outputs
are labeled `SYNTHETIC_NOT_RESEARCH`. See [SAS handoff](../../docs/SAS_LOCAL_HANDOFF.md).
