# Active configuration

The [protocol](../docs/experiment_protocol.md) is scientific authority. `dataset.yaml` configures paths, raw identity, sample sizes and seed. `experiments.yaml` provides bundle paths and allowlists/splits checked by the producer. `models.yaml` registers ownership and pending learned-model settings. `contract.yaml` distinguishes producer 2.0.0 from the overall DRAFT experiment contract.

Generation saves configuration snapshots. Later status updates do not alter immutable runs. Optional sensitivities remain metadata only. Final scoring is blocked by the pending freeze. Historical V1 evidence/tests are unchanged. See [handoff](../docs/DELTA_DATA_HANDOFF.md).
