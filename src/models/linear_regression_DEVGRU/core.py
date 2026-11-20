"""Shared, contract-guarded utilities for DEVGRU learned models.

This module deliberately does not choose the still-draft experiment settings.
Callers must provide the preprocessing and prediction policies explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY
from src.features_DELTA.bundle import load_bundle, sha256
from src.features_DELTA.v2 import COMMON, EXTRA

PREDICTION_COLUMNS = KEY + ["actual", "prediction", "model", "feature_set", "split", "run_id"]
FEATURES = {
    "sales_only": list(COMMON),
    "stockout_aware": list(COMMON) + list(EXTRA),
}
FORBIDDEN_PREDICTORS = set(KEY) | {
    "actual", "sale_amount", "split", "prediction", "run_id",
    "target_stockout_hours", "target_stockout_group", "stock_hour6_22_cnt",
    "hours_sale", "hours_stock_status", "day_number",
}
SPLITS = ("train", "validation", "test")
MODEL_LABELS = {"linear_regression", "ridge_regression"}


def feature_names(feature_set: str) -> list[str]:
    """Return a fresh copy of the exact producer-approved allowlist."""
    try:
        return list(FEATURES[feature_set])
    except KeyError as exc:
        raise ValueError(f"Unsupported feature_set: {feature_set!r}") from exc


def _require_unique(frame: pd.DataFrame, label: str) -> None:
    if not set(KEY).issubset(frame.columns):
        raise ValueError(f"{label} is missing key columns {KEY}")
    if frame.duplicated(KEY).any():
        raise ValueError(f"{label} contains duplicate keys")


def require_columns(frame: pd.DataFrame, required: Sequence[str], label: str) -> None:
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def keyed_observations(tables: Mapping[str, pd.DataFrame], feature_set: str) -> pd.DataFrame:
    """Join one condition to authoritative observations with strict coverage checks."""
    names = feature_names(feature_set)
    observations = tables["observations"]
    features = tables[f"features_{feature_set}"]
    _require_unique(observations, "observations")
    _require_unique(features, f"features_{feature_set}")
    if list(features.columns) != KEY + names:
        raise ValueError(f"Unexpected {feature_set} schema/order")
    joined = observations.merge(features, on=KEY, how="left", validate="one_to_one", indicator=True)
    if not joined["_merge"].eq("both").all() or len(joined) != len(observations) or len(joined) != len(features):
        raise ValueError(f"{feature_set} key population does not match observations")
    joined = joined.drop(columns="_merge")
    if joined[names].isna().any().any() or not np.isfinite(joined[names].to_numpy(dtype=float)).all():
        raise ValueError(f"{feature_set} predictors contain missing/nonfinite values")
    if joined[["actual"]].isna().any().any() or not np.isfinite(joined.actual.to_numpy(dtype=float)).all():
        raise ValueError("Observations contain missing/nonfinite actuals")
    if not joined.split.isin(SPLITS).all():
        raise ValueError("Observations contain an unsupported split")
    if set(names) & FORBIDDEN_PREDICTORS:
        raise ValueError("Feature allowlist contains a forbidden predictor")
    return joined


def validate_paired_conditions(tables: Mapping[str, pd.DataFrame]) -> None:
    """Require exact keys, actuals and splits before comparing conditions."""
    left = keyed_observations(tables, "sales_only")
    right = keyed_observations(tables, "stockout_aware")
    for column in KEY + ["actual", "split"]:
        if not left[column].equals(right[column]):
            raise ValueError(f"Feature conditions disagree on {column}")


@dataclass
class TrainOnlyStandardizer:
    """Optional train-only centering/scaling transform."""

    mean_: np.ndarray | None = None
    scale_: np.ndarray | None = None

    def fit(self, values: np.ndarray) -> "TrainOnlyStandardizer":
        values = _numeric_matrix(values)
        self.mean_ = values.mean(axis=0)
        scale = values.std(axis=0)
        self.scale_ = np.where(scale > 0, scale, 1.0)
        return self

    def transform(self, values: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.scale_ is None:
            raise RuntimeError("Preprocessor must be fit on training data first")
        values = _numeric_matrix(values)
        if values.shape[1] != len(self.mean_):
            raise ValueError("Predictor width changed after preprocessing fit")
        return (values - self.mean_) / self.scale_


def _numeric_matrix(values: np.ndarray | pd.DataFrame) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2 or not np.isfinite(matrix).all():
        raise ValueError("Predictors must be a finite two-dimensional numeric matrix")
    return matrix


def make_preprocessor(policy: str) -> TrainOnlyStandardizer | None:
    if policy == "none":
        return None
    if policy == "standardize":
        return TrainOnlyStandardizer()
    raise ValueError("preprocessing_policy must be 'none' or 'standardize'")


def permitted_prediction_splits(permitted_splits: Sequence[str] | None) -> tuple[str, ...]:
    """Validate the non-test prediction surface; test is intentionally unavailable."""
    if permitted_splits is None:
        permitted_splits = ("train", "validation")
    requested = tuple(permitted_splits)
    if not requested or any(split not in ("train", "validation") for split in requested):
        raise ValueError("Only non-empty train/validation prediction requests are permitted; test is blocked")
    if len(set(requested)) != len(requested):
        raise ValueError("permitted_splits must not contain duplicates")
    return requested


def _validate_iso_dates(values: pd.Series, label: str) -> None:
    if not pd.api.types.is_string_dtype(values):
        raise ValueError(f"{label} dates must be ISO YYYY-MM-DD strings")
    parsed = pd.to_datetime(values, format="%Y-%m-%d", errors="coerce")
    if parsed.isna().any() or not values.eq(parsed.dt.strftime("%Y-%m-%d")).all():
        raise ValueError(f"{label} dates must be ISO YYYY-MM-DD strings")


def prediction_frame(joined: pd.DataFrame, values: Iterable[float], model: str,
                     feature_set: str, run_id: str) -> pd.DataFrame:
    require_columns(joined, KEY + ["actual", "split", "dt"], "Prediction input")
    _require_unique(joined, "Prediction input")
    if model not in MODEL_LABELS:
        raise ValueError(f"Unsupported model label: {model!r}")
    feature_names(feature_set)
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string")
    if not joined["split"].isin(("train", "validation")).all():
        raise ValueError("Prediction input may contain only train/validation rows; test is blocked")
    _validate_iso_dates(joined["dt"], "Prediction")
    if joined["actual"].isna().any() or not np.isfinite(joined["actual"].to_numpy(dtype=float)).all():
        raise ValueError("Prediction input actuals must be finite")
    try:
        predictions = np.asarray(list(values), dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Predictions must be numeric") from exc
    if len(predictions) != len(joined) or not np.isfinite(predictions).all():
        raise ValueError("Predictions must be finite and match the authoritative rows")
    output = joined[KEY + ["actual", "split"]].copy()
    output["prediction"] = predictions
    output["model"] = model
    output["feature_set"] = feature_set
    output["run_id"] = run_id
    output = output[PREDICTION_COLUMNS]
    if output.duplicated(KEY + ["model", "feature_set", "split", "run_id"]).any():
        raise ValueError("Prediction keys are not unique")
    return output


def verify_prediction_frame(frame: pd.DataFrame, expected: pd.DataFrame) -> None:
    if list(frame.columns) != PREDICTION_COLUMNS:
        raise ValueError("Prediction schema/order mismatch")
    require_columns(expected, KEY + ["actual", "split", "dt"], "Authoritative observations")
    for label, table in (("predictions", frame), ("authoritative observations", expected)):
        _require_unique(table, label)
        require_columns(table, KEY + ["actual", "split", "dt"], label)
        _validate_iso_dates(table["dt"], label)
    if not frame.model.isin(MODEL_LABELS).all() or not frame.feature_set.isin(FEATURES).all():
        raise ValueError("Prediction labels are not recognized")
    if not frame.split.isin(("train", "validation")).all() or not expected.split.isin(("train", "validation")).all():
        raise ValueError("Prediction/authoritative rows may contain only train/validation splits; test is blocked")
    if len(frame) == 0 or frame.model.nunique(dropna=False) != 1:
        raise ValueError("Prediction frame must contain exactly one model label")
    if frame.feature_set.nunique(dropna=False) != 1:
        raise ValueError("Prediction frame must contain exactly one feature-set label")
    if not frame.run_id.map(lambda value: isinstance(value, str) and bool(value.strip())).all():
        raise ValueError("Prediction run IDs must be non-empty strings")
    if frame.run_id.nunique(dropna=False) != 1:
        raise ValueError("Prediction frame must contain exactly one run ID")
    key_columns = KEY
    if frame[key_columns].duplicated().any():
        raise ValueError("Prediction keys are not unique")
    if expected[key_columns].duplicated().any():
        raise ValueError("Authoritative keys are not unique")
    comparison = frame[key_columns + ["actual", "split"]].merge(
        expected[key_columns + ["actual", "split"]], on=key_columns, how="outer",
        validate="one_to_one", indicator=True, suffixes=("_prediction", "_expected"),
    )
    if not comparison["_merge"].eq("both").all():
        raise ValueError("Prediction keys do not exactly match authoritative keys")
    if not comparison.actual_prediction.equals(comparison.actual_expected):
        raise ValueError("Prediction actuals do not match authoritative actuals")
    if not comparison.split_prediction.equals(comparison.split_expected):
        raise ValueError("Prediction splits do not match authoritative splits")
    if not np.isfinite(frame[["actual", "prediction"]].to_numpy(dtype=float)).all():
        raise ValueError("Prediction actuals/predictions must be finite")


def load_verified_bundle(bundle_path: str | Path, expected_manifest_sha256: str) -> tuple[dict, dict]:
    """Load only a bundle whose top-level manifest matches trusted evidence."""
    if not expected_manifest_sha256:
        raise ValueError("A trusted expected_manifest_sha256 is required")
    return load_bundle(bundle_path, expected_manifest_sha256=expected_manifest_sha256)


def bundle_identity(bundle_path: str | Path) -> str:
    return sha256(Path(bundle_path) / "bundle_manifest.json")


def run_metadata(*, bundle_id: str, manifest_sha256: str, purpose: str, model: str,
                 feature_set: str, run_id: str, preprocessing_policy: str,
                 prediction_policy: str = "none", tuning_status: str = "pending") -> dict:
    """Create explicit metadata without claiming that a run is experimental evidence."""
    if purpose not in {"synthetic_test_only", "development_debugging", "final_experiment"}:
        raise ValueError("Unsupported run purpose")
    return {
        "protocol_version": "2.0", "technical_contract_status": "draft",
        "purpose": purpose, "bundle_id": bundle_id, "bundle_manifest_sha256": manifest_sha256,
        "model": model, "feature_set": feature_set, "feature_columns": feature_names(feature_set),
        "preprocessing_policy": preprocessing_policy, "training_only_preprocessing": True,
        "prediction_policy": prediction_policy, "tuning_status": tuning_status, "run_id": run_id,
        "evidence_status": "test_only_smoke" if purpose == "synthetic_test_only" else "not_generated",
    }
