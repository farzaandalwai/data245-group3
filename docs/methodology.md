# Methodology entry point

The fixed design, target, splits, features, leakage limits, metrics, test exposure, and deviations are defined once in [experiment_protocol.md](experiment_protocol.md). This file is a navigation entry point, not a second protocol or an experiment result.

Implementation boundaries follow [team_responsibilities.md](team_responsibilities.md); file/data contracts are drafted in [interfaces.md](interfaces.md). DELTA supplies shared data/features and baselines, DEVGRU supplies linear/ridge predictions, and SAS supplies tree predictions and common evaluation/integration. Both feature conditions must remain matched.

At restructuring, only inherited preparation/baseline code exists. Feature producers, matched eligibility, models, evaluator, and the formal leakage audit remain pending. The [experiment log](experiment_log.md) distinguishes executed evidence from planned work. No sustainability outcome or final comparison is claimed.
