# Methodology entry point

The fixed design, target, splits, features, leakage limits, metrics, test exposure, and deviations are defined once in [experiment_protocol.md](experiment_protocol.md). This file is a navigation entry point, not a second protocol or an experiment result.

Implementation boundaries follow [team_responsibilities.md](team_responsibilities.md); file/data contracts are frozen as v1.0.0 in [interfaces.md](interfaces.md) and [the canonical YAML](../configs/contract.yaml). DELTA supplies shared data/features and baselines, DEVGRU supplies linear/ridge predictions, and SAS supplies tree predictions and common evaluation/integration. Both feature conditions must remain matched.

At restructuring, only inherited preparation/baseline code exists. The later source/local stockout-field audit verified the eligibility definition/counts without producing features or scores. Feature producers, models, evaluator, and actual experiment-wide leakage verification remain pending. The [experiment log](experiment_log.md) distinguishes executed evidence from planned work. No sustainability outcome or final comparison is claimed.
