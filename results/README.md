# Results and evidence

The three inherited baseline artifacts are now in `baselines_DELTA/inherited/`, unchanged. The historical restructuring produced no new runs. DELTA V2 development baselines now exist separately under `baselines_DELTA/v2/`; learned-model/comparison directories remain guidance only.

Owners write separate versioned run folders under their own model directory. The shared prediction contract is documented in `docs/interfaces.md`; imported predictions retain their historical schema. Generated results and model binaries are ignored by default. Small evidence files need a deliberate reviewed exception; large artifacts need an accessible source plus byte count/hash/acquisition instructions.

The redesigned v2 final experiment (1,000 series) has no results. Keep historical/development/final evidence separate and identify protocol version plus sample manifest on every new run. Approved science is in [the protocol](../docs/experiment_protocol.md); technical schemas remain draft.

## DELTA V2 update - 2026-11-19

Development baseline results exist under `baselines_DELTA/v2/v2-development-baselines-r2/`. No final test predictions or metrics were generated. See [handoff](../docs/DELTA_DATA_HANDOFF.md).
