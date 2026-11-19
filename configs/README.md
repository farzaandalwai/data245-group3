# Shared configuration metadata

[Scientific authority](../docs/experiment_protocol.md) takes precedence over these machine-readable summaries. `dataset.yaml` records source paths, development/final sample strategy and verification status; `experiments.yaml` records approved timing/features/populations/metrics; `models.yaml` records scope/ownership and draft prediction fields.

These YAML files are **metadata only**. Layout tests consume existing path/owner fields; no ML producer/runner consumes the new scientific fields. New fields document approved concepts, proposed sampling guidance, projected counts and pending details, not runtime support. `original_rows` refers to inherited pilot source rows; final counts are projections. `planned_history_days` now describes optional sensitivity only. Proposed column names and null final manifest are deliberate draft/not-generated markers.

Scientific approval is separate from technical completion: `contract_frozen: false`. Exact V1 definition/lock/audit/source records are preserved under [historical evidence](../docs/history/contract_v1/README.md), tested separately. Their old path/hash mapping is resolved explicitly by historical tests; no lock hash was rewritten. There is no active V2 freeze lock. Semantic reconciliation is local; Git ancestry integration remains pending. Coordinate shared edits across DELTA/DEVGRU/SAS; see [interfaces](../docs/interfaces.md).

Active `contract.yaml` registers the three V2 metadata sources, authority paths, pending details and test gates; `pyproject.toml` registers only this active contract.
