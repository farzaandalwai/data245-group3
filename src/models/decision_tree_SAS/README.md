# Decision-tree regression — SAS

Status: not implemented. Own the core tree comparison for both feature conditions using DELTA's shared verified bundle. Preserve paired keys/budgets, fit preprocessing on training only, and choose tree settings on validation only.

Write separate runs under `results/decision_tree_SAS/` in the shared prediction format. Adapter development can proceed with a labeled schema fixture; real runs need the frozen feature bundle, and new test evaluation waits for frozen validation choices. SAS also owns shared evaluation, but model predictions and evaluator implementation should remain separate components.

Follow the [approved v2 protocol](../../../docs/experiment_protocol.md) and [draft shared contract](../../../docs/interfaces.md). Real runs use DELTA's same verified development/final bundle and target keys, including otherwise eligible stockout target dates; subgroup labels are evaluation-only. V1 evidence/tests are now separate from active V2 checks; DELTA producer 2.0.0 is implemented and operationally verified; see [handoff](../../../docs/DELTA_DATA_HANDOFF.md). Base ancestry integration is complete. Consumer development may proceed; human acceptance, remaining model/evaluation details and final-scoring freeze remain pending.
