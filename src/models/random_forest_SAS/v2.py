"""Train-only Random Forest development consumer of DELTA's shared features.

Mirrors the Decision Tree consumer: same keys/targets/allowlists, the same
depth/leaf grid and 12-candidate per-condition budget, train-only fitting,
validation-MAE selection and no refit, clipping or test access. Ensemble size
and feature fraction are fixed, not tuned. Development only; not group-frozen.
"""
from itertools import product

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.v2 import (
    CONDITIONS, PREDICTION_COLUMNS, development_gate, regression_metrics,
    validate_predictions,
)
from src.features_DELTA.bundle import validate_tables
from src.features_DELTA.v2 import COMMON, EXTRA

FIXED = {
    "policy_version": "sas-forest-development-1",
    "status": "development_only_not_group_frozen",
    "criterion": "squared_error",
    "max_features": 1.0,
    "bootstrap": True,
    "preprocessing": "none",
    "prediction_postprocessing": "none",
    "selection_metric": "MAE",
    "selection_split": "validation",
    "tie_break": "first_in_declared_grid_order",
}


def validate_policy(policy):
    """Only an explicit, bounded development grid is supported, never a freeze."""
    if set(policy) != set(FIXED) | {"random_state", "n_estimators", "max_depth", "min_samples_leaf"}:
        raise ValueError("Unexpected/missing development policy fields")
    for name, value in FIXED.items():
        if type(policy[name]) is not type(value) or policy[name] != value:
            raise ValueError("Unsupported development policy")
    if type(policy["random_state"]) is not int or not 0 <= policy["random_state"] < 2**32:
        raise ValueError("random_state must be a fixed uint32 integer")
    if type(policy["n_estimators"]) is not int or not 1 <= policy["n_estimators"] <= 1000:
        raise ValueError("n_estimators must be a fixed integer from 1 to 1000")
    for name in ("max_depth", "min_samples_leaf"):
        values = policy[name]
        if not isinstance(values, list) or not values:
            raise ValueError("Development grids must be nonempty ordered lists")
        for value in values:
            if value is None and name == "max_depth":
                continue
            if type(value) is not int or value < 1:
                raise ValueError("Depth/leaf grid values must be positive integers (or null depth)")
        if len(values) != len(set(values)):
            raise ValueError("Duplicate grid candidates are not allowed")
    if len(policy["max_depth"]) * len(policy["min_samples_leaf"]) > 64:
        raise ValueError("Development budget exceeds 64 candidates per condition")


def fit_development(tables, policy, *, purpose, run_id):
    """Return paired train/validation predictions, selection evidence and forests."""
    development_gate(purpose, ("train", "validation"))
    validate_policy(policy)
    if not isinstance(run_id, str) or not run_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in run_id):
        raise ValueError("Invalid run ID")
    observations = tables["observations"]
    validate_tables(tables, observations[SERIES].drop_duplicates().reset_index(drop=True))
    train = observations.split.eq("train")
    validation = observations.split.eq("validation")
    report = {"policy": policy, "selected_parameters": {}, "candidates": [],
              "fit_split": "train", "selection_split": "validation",
              "refit_on_validation": False, "test_scored": False,
              "training_rows": int(train.sum()), "validation_rows": int(validation.sum()),
              "feature_columns": {"sales_only": COMMON, "stockout_aware": COMMON + EXTRA},
              "feature_importances": {}}
    predictions, models = [], {}
    grid = list(product(policy["max_depth"], policy["min_samples_leaf"]))
    for condition in CONDITIONS:
        names = report["feature_columns"][condition]
        joined = observations.merge(tables[f"features_{condition}"], on=KEY, how="left",
                                    validate="one_to_one", sort=False)
        x_train, y_train = joined.loc[train, names], joined.loc[train, "actual"]
        x_validation, y_validation = joined.loc[validation, names], joined.loc[validation, "actual"]
        best_score, best_model, best_parameters = np.inf, None, None
        for index, (depth, leaf) in enumerate(grid):
            parameters = {"criterion": policy["criterion"], "n_estimators": policy["n_estimators"],
                          "max_features": policy["max_features"], "bootstrap": policy["bootstrap"],
                          "max_depth": depth, "min_samples_leaf": leaf,
                          "random_state": policy["random_state"], "n_jobs": 1}
            estimator = RandomForestRegressor(**parameters)
            estimator.fit(x_train, y_train)
            score = regression_metrics(y_validation, estimator.predict(x_validation))["MAE"]
            report["candidates"].append({"feature_set": condition, "candidate_index": index,
                                         "parameters": parameters, "validation_MAE": score})
            if score < best_score:  # Stable grid order resolves exact ties.
                best_score, best_model, best_parameters = score, estimator, parameters
        models[condition] = best_model
        report["selected_parameters"][condition] = best_parameters
        report["feature_importances"][condition] = dict(zip(names, best_model.feature_importances_.tolist()))
        for split in ("train", "validation"):
            mask = joined.split.eq(split)
            output = joined.loc[mask, KEY + ["actual", "split"]].copy()
            output["prediction"] = best_model.predict(joined.loc[mask, names])
            output["model"], output["feature_set"], output["run_id"] = "random_forest", condition, run_id
            predictions.append(output[PREDICTION_COLUMNS])
    predicted = pd.concat(predictions, ignore_index=True)
    validate_predictions(predicted, observations, ["random_forest"], ["train", "validation"])
    report["candidates_per_condition"] = len(grid)
    return predicted, report, models
