"""NumPy implementation of the approved Ridge Regression extension."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY
from src.models.linear_regression_DEVGRU.core import (
    SPLITS, feature_names, keyed_observations, make_preprocessor,
    permitted_prediction_splits, prediction_frame, require_columns,
)


class RidgeRegressionModel:
    label = "ridge_regression"

    def __init__(self, alpha: float, preprocessing_policy: str):
        if isinstance(alpha, bool) or not isinstance(alpha, (int, float, np.number)):
            raise ValueError("Ridge alpha must be numeric")
        if not np.isfinite(alpha) or alpha <= 0:
            raise ValueError("Ridge alpha must be a finite positive number")
        self.alpha = float(alpha)
        self.preprocessing_policy = preprocessing_policy
        self.preprocessor = make_preprocessor(preprocessing_policy)
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None

    def fit(self, X, y) -> "RidgeRegressionModel":
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.ndim != 2 or y.ndim != 1 or len(X) != len(y) or len(X) == 0:
            raise ValueError("X/y dimensions are invalid")
        if not np.isfinite(X).all() or not np.isfinite(y).all():
            raise ValueError("X/y must be finite")
        if self.preprocessor is not None:
            self.preprocessor.fit(X)
            X = self.preprocessor.transform(X)
        design = np.column_stack([np.ones(len(X)), X])
        penalty = np.zeros((X.shape[1], design.shape[1]))
        penalty[:, 1:] = np.eye(X.shape[1]) * np.sqrt(self.alpha)
        augmented_design = np.vstack([design, penalty])
        augmented_target = np.concatenate([y, np.zeros(X.shape[1])])
        solution, _, _, _ = np.linalg.lstsq(augmented_design, augmented_target, rcond=None)
        self.intercept_, self.coef_ = float(solution[0]), solution[1:]
        return self

    def predict(self, X) -> np.ndarray:
        if self.coef_ is None or self.intercept_ is None:
            raise RuntimeError("Model must be fit before predict")
        X = np.asarray(X, dtype=float)
        if self.preprocessor is not None:
            X = self.preprocessor.transform(X)
        predictions = self.intercept_ + X @ self.coef_
        if not np.isfinite(predictions).all():
            raise ValueError("Ridge predictions are nonfinite")
        return predictions

    def fit_predict_bundle(self, tables, feature_set: str, run_id: str,
                           permitted_splits=("train", "validation")):
        joined = keyed_observations(tables, feature_set)
        names = feature_names(feature_set)
        train = joined.split.eq("train")
        if not train.any():
            raise ValueError("Training population is empty")
        requested = permitted_prediction_splits(permitted_splits)
        selected = joined[joined.split.isin(requested)].copy()
        if selected.empty:
            raise ValueError("Requested prediction population is empty")
        self.fit(joined.loc[train, names].to_numpy(), joined.loc[train, "actual"].to_numpy())
        return prediction_frame(selected, self.predict(selected[names].to_numpy()), self.label, feature_set, run_id)


def select_ridge_alpha(model_factory, joined, candidates: list[float], *, feature_set: str,
                       preprocessing_policy: str):
    """Validation-only bounded selection helper; caller supplies the approved grid/budget."""
    if not isinstance(joined, pd.DataFrame):
        raise ValueError("joined must be a pandas DataFrame")
    if not isinstance(candidates, (list, tuple)) or not candidates or len(candidates) > 20:
        raise ValueError("Provide a bounded non-empty alpha grid (max 20)")
    if any(isinstance(alpha, bool) or not isinstance(alpha, (int, float, np.number)) for alpha in candidates):
        raise ValueError("Ridge alpha candidates must be numeric")
    normalized = [float(alpha) for alpha in candidates]
    if any(not np.isfinite(alpha) or alpha <= 0 for alpha in normalized):
        raise ValueError("Ridge alpha candidates must be finite and strictly positive")
    if len(set(normalized)) != len(normalized):
        raise ValueError("Ridge alpha candidates must be unique")
    features = feature_names(feature_set)
    require_columns(joined, [*KEY, "actual", "split", *features], "Alpha-selection input")
    if joined.duplicated(KEY).any():
        raise ValueError("Alpha-selection input contains duplicate authoritative keys")
    if not joined["split"].isin(SPLITS).all():
        raise ValueError("Alpha-selection input contains invalid split labels")
    make_preprocessor(preprocessing_policy)
    train, validation = joined["split"].eq("train"), joined["split"].eq("validation")
    if not train.any() or not validation.any():
        raise ValueError("Validation alpha selection requires nonempty train and validation populations")
    used = joined.loc[train | validation, features + ["actual"]]
    if used.isna().any().any() or not np.isfinite(used.to_numpy(dtype=float)).all():
        raise ValueError("Alpha-selection train/validation predictors and actuals must be finite")
    scores = []
    for alpha in normalized:
        model = model_factory(alpha=alpha, preprocessing_policy=preprocessing_policy)
        model.fit(joined.loc[train, features].to_numpy(), joined.loc[train, "actual"].to_numpy())
        error = model.predict(joined.loc[validation, features].to_numpy()) - joined.loc[validation, "actual"].to_numpy()
        scores.append((float(np.mean(np.abs(error))), float(alpha)))
    selected = min(scores, key=lambda item: (item[0], item[1]))
    return selected[1], [{"alpha": alpha, "validation_mae": mae} for mae, alpha in scores]
