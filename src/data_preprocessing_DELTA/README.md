# Data preparation — DELTA

`prepare_and_baselines.py` is a path-adapted copy of Timothy Tran's inherited script. It resolves the root two parents above this file, reads `data/raw/freshretail.csv`, and writes only to separate `data/processed/reproduction/`, `data/manifests/reproduction/`, and `results/baselines_DELTA/reproduction/` locations. Those generated files do not replace the fixed canonical pilot/manifest or inherited evidence.

`data_explore.py` is a path-adapted historical downloader, guarded by `main`. It would fetch a current upstream training split, which is not proof of reproducing the smaller inherited export. It requires download dependencies beyond the minimal analysis stack; do not use it for bootstrap acquisition.

Both originals are byte-identical in `archive/original_pilot/data_prep_pipeline/`. Neither working script was run during migration. Future task: validate input lineage/schema and support the shared eligibility/feature contract. Do not implement new experiments as part of a folder change.
