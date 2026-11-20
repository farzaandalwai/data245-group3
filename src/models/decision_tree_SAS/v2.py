"""Train-only Decision Tree development consumer of DELTA's shared features."""
from itertools import product

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.v2 import (
    CONDITIONS, PREDICTION_COLUMNS, development_gate, regression_metrics,
    validate_predictions,
)
from src.features_DELTA.bundle import validate_tables
from src.features_DELTA.v2 import COMMON, EXTRA


def validate_policy(policy):
    """Only an explicit, bounded development grid is supported, never a freeze."""
    required = {
        "policy_version": "sas-tree-development-1",
        "status": "development_only_not_group_frozen",
        "criterion": "squared_error",
        "preprocessing": "none",
        "prediction_postprocessing": "none",
        "selection_metric": "MAE",
        "selection_split": "validation",
        "tie_break": "first_in_declared_grid_order",
    }
    if set(policy) != set(required) | {"random_state", "max_depth", "min_samples_leaf"}:
        raise ValueError("Unexpected/missing development policy fields")
    if any(policy[name] != value for name, value in required.items()):
        raise ValueError("Unsupported development policy")
    if type(policy["random_state"]) is not int or not 0 <= policy["random_state"] < 2**32:
        raise ValueError("random_state must be a fixed uint32 integer")
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
    """Return paired train/validation predictions, selection evidence and trees.

    Both conditions receive the identical ordered grid and fitting budget. The
    winning already-train-fitted candidate is retained; no validation refit.
    Test features/targets and retrospective labels never enter fitting/selection.
    """
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
              "feature_columns": {"sales_only": COMMON, "stockout_aware": COMMON + EXTRA}}
    predictions, models = [], {}
    grid = list(product(policy["max_depth"], policy["min_samples_leaf"]))
    for condition in CONDITIONS:
        names = report["feature_columns"][condition]
        features = tables[f"features_{condition}"]
        # Explicit keyed join, even though the verified bundle is already sorted.
        joined = observations.merge(features, on=KEY, how="left", validate="one_to_one", sort=False)
        x_train = joined.loc[train, names]
        y_train = joined.loc[train, "actual"]
        x_validation = joined.loc[validation, names]
        y_validation = joined.loc[validation, "actual"]
        best_score, best_model, best_parameters = np.inf, None, None
        for index, (depth, leaf) in enumerate(grid):
            parameters = {"criterion": policy["criterion"], "splitter": "best",
                          "max_depth": depth, "min_samples_leaf": leaf,
                          "random_state": policy["random_state"]}
            estimator = DecisionTreeRegressor(**parameters)
            estimator.fit(x_train, y_train)
            score = regression_metrics(y_validation, estimator.predict(x_validation))["MAE"]
            report["candidates"].append({"feature_set": condition, "candidate_index": index,
                                         "parameters": parameters, "validation_MAE": score})
            if score < best_score:  # Stable grid order resolves exact ties.
                best_score, best_model, best_parameters = score, estimator, parameters
        models[condition] = best_model
        report["selected_parameters"][condition] = best_parameters
        for split in ("train", "validation"):
            mask = joined.split.eq(split)
            output = joined.loc[mask, KEY + ["actual", "split"]].copy()
            output["prediction"] = best_model.predict(joined.loc[mask, names])
            output["model"], output["feature_set"], output["run_id"] = "decision_tree", condition, run_id
            predictions.append(output[PREDICTION_COLUMNS])
    predicted = pd.concat(predictions, ignore_index=True)
    validate_predictions(predicted, observations, ["decision_tree"], ["train", "validation"])
    report["candidates_per_condition"] = len(grid)
    return predicted, report, models


def serialize_tree(estimator):
    """Inspectable numeric tree, with no executable pickle or custom deserializer."""
    tree = estimator.tree_
    return {"format": "sklearn-tree-inspection-1", "feature_names": estimator.feature_names_in_.tolist(),
            "parameters": estimator.get_params(), "children_left": tree.children_left.tolist(),
            "children_right": tree.children_right.tolist(), "feature": tree.feature.tolist(),
            "threshold": tree.threshold.tolist(), "value": tree.value[:, 0, 0].tolist(),
            "n_node_samples": tree.n_node_samples.tolist(), "impurity": tree.impurity.tolist()}
