"""Inspectable numeric Linear/Ridge state for NEW runs; never executable pickle."""
import numpy as np

from src.models.linear_regression_DEVGRU.core import feature_names
from src.models.linear_regression_DEVGRU.model import LinearRegressionModel
from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel

FORMAT = "devgru-numeric-model-1"


def _vector(value, width, name):
    if not isinstance(value, list) or len(value) != width:
        raise ValueError(f"Invalid {name} width")
    if any(type(x) not in (int, float) for x in value):
        raise ValueError(f"Invalid numeric {name}")
    out = np.asarray(value, dtype=float)
    if not np.isfinite(out).all():
        raise ValueError(f"Nonfinite {name}")
    return out


def model_from_state(state):
    """Validate the allowlist and fitted arrays, then restore without calling fit."""
    required = {"format", "model", "feature_set", "feature_names", "preprocessing_policy",
                "intercept", "coefficients", "alpha", "preprocessor"}
    if not isinstance(state, dict) or set(state) != required or state["format"] != FORMAT:
        raise ValueError("Unsupported fitted-model schema")
    names = feature_names(state["feature_set"])
    if state["feature_names"] != names:
        raise ValueError("Fitted-model feature order differs from approved allowlist")
    width = len(names)
    if state["model"] == "linear_regression" and state["alpha"] is None:
        model = LinearRegressionModel(state["preprocessing_policy"])
    elif state["model"] == "ridge_regression":
        model = RidgeRegressionModel(state["alpha"], state["preprocessing_policy"])
    else:
        raise ValueError("Unsupported fitted-model family/alpha")
    intercept = state["intercept"]
    if type(intercept) not in (int, float) or not np.isfinite(intercept):
        raise ValueError("Invalid fitted intercept")
    model.intercept_ = float(intercept)
    model.coef_ = _vector(state["coefficients"], width, "coefficients")
    scaler = state["preprocessor"]
    if model.preprocessor is None:
        if scaler is not None:
            raise ValueError("Unexpected preprocessing state")
    else:
        if not isinstance(scaler, dict) or set(scaler) != {"mean", "scale"}:
            raise ValueError("Missing fitted preprocessing state")
        model.preprocessor.mean_ = _vector(scaler["mean"], width, "mean")
        model.preprocessor.scale_ = _vector(scaler["scale"], width, "scale")
        if (model.preprocessor.scale_ <= 0).any():
            raise ValueError("Preprocessing scales must be positive")
    return model


def model_state(model, feature_set):
    """Export current fitted state; this does not reconstruct an unsaved old model."""
    if not isinstance(model, (LinearRegressionModel, RidgeRegressionModel)):
        raise ValueError("Unsupported fitted-model class")
    if model.coef_ is None or model.intercept_ is None:
        raise ValueError("Cannot export an unfitted model")
    scaler = model.preprocessor
    if scaler is not None and (scaler.mean_ is None or scaler.scale_ is None):
        raise ValueError("Cannot export an unfitted preprocessor")
    state = {"format": FORMAT, "model": model.label, "feature_set": feature_set,
             "feature_names": feature_names(feature_set),
             "preprocessing_policy": model.preprocessing_policy,
             "intercept": float(model.intercept_), "coefficients": model.coef_.tolist(),
             "alpha": float(model.alpha) if isinstance(model, RidgeRegressionModel) else None,
             "preprocessor": None if scaler is None else {
                 "mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist()}}
    model_from_state(state)
    return state
