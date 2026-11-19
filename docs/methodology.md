# Methodology entry point

The [approved v2 protocol](experiment_protocol.md) is the scientific source of truth for the recorded-sales question, population, sample strategy, features, splits, models, metrics and limitations. It supersedes conflicting historical v1 assumptions. This file is navigation, not a second protocol or experimental result.

Implementation boundaries are in [responsibilities](team_responsibilities.md); shared conceptual requirements and **DRAFT CONTRACT** details are in [interfaces](interfaces.md). DELTA produces the shared data/features/baselines; DEVGRU consumes them for linear/ridge and SAS for tree/optional forest plus common evaluation.

Scientific approval does not mean technical freeze or implemented functionality. The new final sample, feature bundle, model runs and evaluation remain **NOT IMPLEMENTED**. Historical pilot results and narrower audit evidence remain historical. See [context](../context.md) for remaining Git integration and technical-verification dependencies and [experiment log](experiment_log.md) for dated decisions.
