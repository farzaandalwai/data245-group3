# SAS shared evaluation/comparison output

Status: synthetic smoke checks plus real SAS development comparison; no final model comparison.
`python3 -m scripts.sas_v2 evaluate` writes immutable ignored runs beneath
`v2/<run_id>/`: overall/subgroup/per-series/per-store metrics, paired MAE
comparisons, full-coverage audit and input/output hashes. Test scoring is blocked.
Paired 95% store-cluster intervals are exported separately with store count and limitations. See [SAS handoff](../../docs/SAS_LOCAL_HANDOFF.md).
