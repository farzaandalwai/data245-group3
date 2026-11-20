"""NumPy implementation of the required pooled Linear Regression model."""

from __future__ import annotations

import numpy as np

from .core import feature_names, keyed_observations, make_preprocessor, permitted_prediction_splits, prediction_frame


class LinearRegressionModel:
    label = "linear_regression"

    def __init__(self, preprocessing_policy: str):
        self.preprocessing_policy = preprocessing_policy
        self.preprocessor = make_preprocessor(preprocessing_policy)
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None

    def fit(self, X, y) -> "LinearRegressionModel":
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
        solution, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
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
            raise ValueError("Linear predictions are nonfinite")
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
