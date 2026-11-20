"""Model-independent V2 development evaluation; never score the test split.

Public evaluation requires authoritative observations and retrospective metadata.
It validates exact coverage before computing any metric, rather than discarding
unmatched rows. Final scoring remains blocked; development intervals use paired
whole-store bootstrap resampling.
"""
from itertools import product

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_integer_dtype, is_numeric_dtype

from src.data_preprocessing_DELTA.v2 import KEY, SERIES


PREDICTION_COLUMNS = KEY + ["actual", "prediction", "model", "feature_set", "split", "run_id"]
CONDITIONS = ("sales_only", "stockout_aware")
BASELINES = ("persistence", "recent_avg_7")
LEARNED_MODELS = ("linear_regression", "ridge_regression", "decision_tree", "random_forest")
DEVELOPMENT_PURPOSES = ("development_debugging", "synthetic_test_only")
METRIC_NAMES = (
    "MAE", "RMSE", "signed_bias", "mean_underprediction", "mean_overprediction",
    "underprediction_rate", "overprediction_rate",
)


def development_gate(purpose, splits):
    """This implementation intentionally has no final/test-scoring escape hatch."""
    if purpose not in DEVELOPMENT_PURPOSES:
        raise ValueError("Only development_debugging or synthetic_test_only inputs are allowed")
    if (not splits or len(set(splits)) != len(splits)
            or not set(splits) <= {"train", "validation"}):
        raise ValueError("Development evaluation permits train/validation only; test scoring is blocked")


def _real_numeric(frame, columns):
    for name in columns:
        values = frame[name]
        if (not is_numeric_dtype(values) or is_bool_dtype(values)
                or np.iscomplexobj(values.to_numpy())
                or not np.isfinite(values.to_numpy(dtype=float)).all()):
            raise ValueError(f"Expected finite real numbers: {name}")


def _keys(frame):
    if frame.empty or frame[KEY].isna().any().any() or frame.duplicated(KEY).any():
        raise ValueError("Observation keys must be nonempty, complete and unique")
    for name in SERIES:
        if (not is_integer_dtype(frame[name]) or is_bool_dtype(frame[name])
                or frame[name].lt(0).any()):
            raise ValueError(f"Expected nonnegative integer IDs: {name}")
    dates = frame.dt
    if not dates.map(lambda value: isinstance(value, str)).all():
        raise ValueError("Dates must be ISO strings")
    parsed = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce")
    if parsed.isna().any() or not parsed.dt.strftime("%Y-%m-%d").equals(dates):
        raise ValueError("Dates must be exact ISO YYYY-MM-DD")


def validate_observations(observations):
    if list(observations) != KEY + ["actual", "split"] or observations.isna().any().any():
        raise ValueError("Invalid authoritative observation schema/nulls")
    _keys(observations)
    _real_numeric(observations, ["actual"])
    if observations.actual.lt(0).any() or not observations.split.isin(["train", "validation", "test"]).all():
        raise ValueError("Invalid authoritative target/split")


def validate_predictions(predictions, observations, models, splits):
    """Check full coverage for each requested model/condition against the bundle.

    This function checks structure only; it can validate inherited baseline test
    records without computing test metrics. evaluate_predictions gates scoring.
    """
    validate_observations(observations)
    if (not models or len(set(models)) != len(models)
            or not set(models) <= set(BASELINES + LEARNED_MODELS)):
        raise ValueError("Specify unique supported expected models")
    if not splits or len(set(splits)) != len(splits) or not set(splits) <= {"train", "validation", "test"}:
        raise ValueError("Invalid expected split set")
    if list(predictions) != PREDICTION_COLUMNS or predictions.empty or predictions.isna().any().any():
        raise ValueError("Invalid prediction schema/nulls/empty input")
    _real_numeric(predictions, ["actual", "prediction"])
    if not set(predictions.model) == set(models) or set(predictions.split) != set(splits):
        raise ValueError("Model/split coverage differs from the explicit request")
    for label in ("model", "feature_set", "split", "run_id"):
        if not predictions[label].map(lambda value: isinstance(value, str) and bool(value.strip())).all():
            raise ValueError(f"Invalid prediction label: {label}")
    expected = observations.loc[observations.split.isin(splits)].sort_values(KEY).reset_index(drop=True)
    if set(expected.split) != set(splits):
        raise ValueError("Authoritative bundle is missing a requested split")
    audit = []
    for model in models:
        frame = predictions.loc[predictions.model.eq(model)]
        conditions = ("common_reference",) if model in BASELINES else CONDITIONS
        if set(frame.feature_set) != set(conditions) or frame.run_id.nunique() != 1:
            raise ValueError(f"Incorrect condition coverage or mixed run IDs for {model}")
        for condition in conditions:
            part = frame.loc[frame.feature_set.eq(condition)].sort_values(KEY).reset_index(drop=True)
            _keys(part)
            if not part[KEY].equals(expected[KEY]):
                raise ValueError(f"Missing/extra/mismatched observation keys for {model}/{condition}")
            if not part.split.equals(expected.split):
                raise ValueError(f"Split mismatch for {model}/{condition}")
            if not np.array_equal(part.actual.to_numpy(), expected.actual.to_numpy()):
                raise ValueError(f"Target mismatch for {model}/{condition}")
            audit.append({"model": model, "feature_set": condition, "rows": len(part),
                          "run_id": part.run_id.iloc[0], "exact_keys_actuals_splits": True})
    return audit


def validate_metadata(metadata, observations):
    if list(metadata) != KEY + ["target_stockout_hours", "target_stockout_group"] or metadata.isna().any().any():
        raise ValueError("Invalid retrospective metadata schema/nulls")
    _keys(metadata)
    ordered = metadata.sort_values(KEY).reset_index(drop=True)
    expected = observations.sort_values(KEY).reset_index(drop=True)
    if not ordered[KEY].equals(expected[KEY]):
        raise ValueError("Retrospective metadata does not cover authoritative observation keys")
    _real_numeric(metadata, ["target_stockout_hours"])
    hours = metadata.target_stockout_hours
    if (not (hours.between(0, 16) & hours.mod(1).eq(0)).all()
            or not np.array_equal(metadata.target_stockout_group,
                                  np.where(hours.eq(0), "fully_stocked", "stockout"))):
        raise ValueError("Inconsistent retrospective stockout labels/counts")


def regression_metrics(actual, prediction):
    """Protocol metrics. Empty groups return n=0 and undefined (None) metrics."""
    actual, prediction = np.asarray(actual, dtype=float), np.asarray(prediction, dtype=float)
    if actual.ndim != 1 or actual.shape != prediction.shape:
        raise ValueError("Metrics require aligned one-dimensional arrays")
    if not np.isfinite(actual).all() or not np.isfinite(prediction).all():
        raise ValueError("Metrics require finite inputs")
    n = len(actual)
    if not n:
        return {"n_observations": 0, **dict.fromkeys(METRIC_NAMES)}
    with np.errstate(over="raise", invalid="raise"):
        try:
            error = prediction - actual
            result = {
                "n_observations": n,
                "MAE": float(np.mean(np.abs(error))),
                "RMSE": float(np.sqrt(np.mean(error ** 2))),
                "signed_bias": float(np.mean(error)),
                "mean_underprediction": float(np.mean(np.maximum(-error, 0))),
                "mean_overprediction": float(np.mean(np.maximum(error, 0))),
                "underprediction_rate": float(np.mean(error < 0)),
                "overprediction_rate": float(np.mean(error > 0)),
            }
        except FloatingPointError as exc:
            raise ValueError("Metric overflow; inputs exceed supported numeric range") from exc
    return result


def _summarize(frame, grouping):
    rows = []
    for values, part in frame.groupby(grouping, sort=True, observed=True):
        if not isinstance(values, tuple):
            values = (values,)
        rows.append(dict(zip(grouping, values)) | regression_metrics(part.actual, part.prediction))
    return pd.DataFrame(rows, columns=grouping + ["n_observations", *METRIC_NAMES])


def evaluate_predictions(predictions, observations, metadata, *, purpose, models, splits=("validation",)):
    """Evaluate explicitly named models; both learned conditions are mandatory."""
    from src.evaluation_SAS.bootstrap import BOOTSTRAP_SPEC, paired_store_intervals

    development_gate(purpose, splits)
    audit = validate_predictions(predictions, observations, models, splits)
    validate_metadata(metadata, observations)
    joined = predictions.merge(metadata, on=KEY, how="left", validate="many_to_one")
    grouping = ["model", "feature_set", "split"]
    overall = _summarize(joined, grouping)
    subgroup_rows = []
    for labels, part in joined.groupby(grouping, sort=True):
        for group in ("fully_stocked", "stockout"):
            subset = part.loc[part.target_stockout_group.eq(group)]
            subgroup_rows.append(dict(zip(grouping, labels)) | {"target_stockout_group": group}
                                 | regression_metrics(subset.actual, subset.prediction))
    subgroups = pd.DataFrame(subgroup_rows)
    paired = []
    for model, split in product(models, splits):
        if model in BASELINES:
            continue
        for group in ("all", "fully_stocked", "stockout"):
            source = overall if group == "all" else subgroups.loc[subgroups.target_stockout_group.eq(group)]
            pair = source.loc[source.model.eq(model) & source.split.eq(split)].set_index("feature_set")
            sales, aware = pair.loc["sales_only"], pair.loc["stockout_aware"]
            n = int(sales.n_observations)
            delta = None if n == 0 else float(sales.MAE - aware.MAE)
            relative = None if n == 0 or sales.MAE == 0 else float(100 * (delta / sales.MAE))
            paired.append({"model": model, "split": split, "target_stockout_group": group,
                           "n_observations": n, "MAE_sales_only": None if not n else float(sales.MAE),
                           "MAE_stockout_aware": None if not n else float(aware.MAE),
                           "MAE_reduction": delta, "relative_MAE_improvement_percent": relative})
    pair_columns = ["model", "split", "target_stockout_group", "n_observations", "MAE_sales_only",
                    "MAE_stockout_aware", "MAE_reduction", "relative_MAE_improvement_percent"]
    return {
        "overall": overall,
        "subgroups": subgroups,
        "per_series": _summarize(joined, grouping + SERIES),
        "per_store": _summarize(joined, grouping + ["store_id"]),
        "paired_comparisons": pd.DataFrame(paired, columns=pair_columns),
        "mae_difference_intervals": paired_store_intervals(
            predictions, observations, purpose=purpose, models=models, splits=splits),
        "coverage_audit": {"exact_coverage_verified": True, "conditions": audit,
                           "requested_models": list(models), "scored_splits": list(splits),
                           "purpose": purpose, "metadata_coverage_verified": True,
                           "uncertainty_status": "implemented_development_paired_store_bootstrap",
                           "uncertainty": BOOTSTRAP_SPEC,
                           "evidence_status": "SYNTHETIC_NOT_RESEARCH" if purpose == "synthetic_test_only"
                                              else "DEVELOPMENT_NOT_FINAL"},
    }
