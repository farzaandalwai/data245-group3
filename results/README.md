# Results and evidence

The three inherited baseline artifacts are now in `baselines_DELTA/inherited/`, unchanged. All other result directories currently contain ownership/output guidance only. No feature/model/evaluation run was produced by restructuring.

Owners write separate versioned run folders under their own model directory. The shared prediction contract is documented in `docs/interfaces.md`; imported predictions retain their historical schema. Generated results and model binaries are ignored by default. Small evidence files need a deliberate reviewed exception; large artifacts need an accessible source plus byte count/hash/acquisition instructions.

The redesigned v2 final experiment (1,000 series) has no results. Keep historical/development/final evidence separate and identify protocol version plus sample manifest on every new run. Approved science is in [the protocol](../docs/experiment_protocol.md); technical schemas remain draft.
