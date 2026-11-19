# Shared configuration metadata

`dataset.yaml` records fixed inputs and current paths; `experiments.yaml` mirrors the planned chronological design; `models.yaml` records owners and implementation status. These files are documentation/configuration metadata, not a runnable experiment framework. They do not implement features, eligibility, tuning, or prediction producers.

DELTA proposes data/feature changes; DEVGRU proposes linear-model changes; SAS coordinates shared protocol/evaluation changes. Coordinate before editing shared files. Exact predictor allowlists and stockout semantics remain pending; `contract_frozen: false` must remain honest. Do not change that flag without the documented freeze review. Requirements remain in `requirements.txt`; PyYAML is used only to validate these files in layout tests.
