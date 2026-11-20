"""Reproducible DEVGRU development-only Linear/Ridge experiments.

The runner requires a trusted development-bundle manifest hash and refuses
final-purpose bundles. It never emits or scores test rows.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.features_DELTA.bundle import load_bundle, sha256
from src.models.linear_regression_DEVGRU.core import (
    PREDICTION_COLUMNS, feature_names, keyed_observations, validate_paired_conditions,
    verify_prediction_frame,
)
from src.models.linear_regression_DEVGRU.model import LinearRegressionModel
from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel, select_ridge_alpha

ALPHA_CANDIDATES = [0.01, 0.1, 1.0, 10.0, 100.0]
PREPROCESSING_POLICY = "standardize"
BOOTSTRAP_REPETITIONS = 2000


def _git_revision() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split in ("train", "validation"):
        part = predictions[predictions["split"].eq(split)]
        if part.empty:
            raise ValueError(f"Missing permitted {split} rows")
        error = part["prediction"].to_numpy(dtype=float) - part["actual"].to_numpy(dtype=float)
        rows.append({
            "split": split, "rows": len(part),
            "MAE": float(np.mean(np.abs(error))),
            "RMSE": float(np.sqrt(np.mean(error ** 2))),
            "signed_bias": float(np.mean(error)),
        })
    return pd.DataFrame(rows)


def _paired_bootstrap(predictions: dict[str, pd.DataFrame], model: str, seed: int,
                      repetitions: int = BOOTSTRAP_REPETITIONS) -> dict:
    sales = predictions[f"{model}:sales_only"]
    aware = predictions[f"{model}:stockout_aware"]
    sales = sales[sales["split"].eq("validation")]
    aware = aware[aware["split"].eq("validation")]
    merged = sales[KEY + ["actual", "prediction"]].merge(
        aware[KEY + ["actual", "prediction"]], on=KEY, how="outer", validate="one_to_one",
        indicator=True, suffixes=("_sales_only", "_stockout_aware"),
    )
    if not merged["_merge"].eq("both").all():
        raise ValueError(f"Paired bootstrap keys do not match for {model}")
    if not merged["actual_sales_only"].equals(merged["actual_stockout_aware"]):
        raise ValueError(f"Paired bootstrap actuals do not match for {model}")
    merged["loss_difference"] = (
        (merged["prediction_stockout_aware"] - merged["actual_stockout_aware"]).abs()
        - (merged["prediction_sales_only"] - merged["actual_sales_only"]).abs()
    )
    series_losses = merged.groupby(SERIES, sort=True)["loss_difference"].mean().to_numpy(dtype=float)
    if len(series_losses) == 0 or not np.isfinite(series_losses).all():
        raise ValueError(f"Invalid paired bootstrap series losses for {model}")
    rng = np.random.default_rng(seed)
    samples = rng.integers(0, len(series_losses), size=(repetitions, len(series_losses)))
    bootstrap_means = series_losses[samples].mean(axis=1)
    return {
        "model": model,
        "MAE_sales_only": float(merged["prediction_sales_only"].sub(merged["actual_sales_only"]).abs().mean()),
        "MAE_stockout_aware": float(merged["prediction_stockout_aware"].sub(merged["actual_stockout_aware"]).abs().mean()),
        "MAE_difference_stockout_aware_minus_sales_only": float(merged["loss_difference"].mean()),
        "bootstrap_ci_lower": float(np.percentile(bootstrap_means, 2.5)),
        "bootstrap_ci_upper": float(np.percentile(bootstrap_means, 97.5)),
        "bootstrap_repetitions": repetitions,
        "bootstrap_seed": seed,
        "resampled_series": int(len(series_losses)),
        "bootstrap_unit": "store-product series",
        "interpretation": "negative favors stockout-aware forecasting",
    }


def run_development(bundle_path: str | Path, expected_manifest_sha256: str,
                    output_root: str | Path, run_id: str, seed: int = 245,
                    bootstrap_repetitions: int = BOOTSTRAP_REPETITIONS) -> Path:
    output_root = Path(output_root)
    if output_root.exists():
        raise FileExistsError(f"Refusing to overwrite existing run directory: {output_root}")
    if not run_id or not run_id.strip():
        raise ValueError("run_id must be non-empty")
    if bootstrap_repetitions < 1:
        raise ValueError("bootstrap_repetitions must be positive")

    tables, manifest = load_bundle(bundle_path, expected_manifest_sha256=expected_manifest_sha256)
    if manifest.get("purpose") != "development_debugging":
        raise ValueError("Development runner accepts only development_debugging bundles")
    validate_paired_conditions(tables)
    bundle_manifest_sha256 = sha256(Path(bundle_path) / "bundle_manifest.json")
    if bundle_manifest_sha256 != expected_manifest_sha256:
        raise ValueError("Loaded bundle manifest does not match trusted evidence")

    predictions: dict[str, pd.DataFrame] = {}
    alpha_rows = []
    metric_rows = []
    selected_alphas = {}
    for model_name in ("linear_regression", "ridge_regression"):
        for feature_set in ("sales_only", "stockout_aware"):
            joined = keyed_observations(tables, feature_set)
            if model_name == "linear_regression":
                model = LinearRegressionModel(PREPROCESSING_POLICY)
                selected_alpha = None
            else:
                selected_alpha, evidence = select_ridge_alpha(
                    RidgeRegressionModel, joined, ALPHA_CANDIDATES,
                    feature_set=feature_set, preprocessing_policy=PREPROCESSING_POLICY,
                )
                selected_alphas[feature_set] = selected_alpha
                for row in evidence:
                    alpha_rows.append({"feature_set": feature_set, **row})
                model = RidgeRegressionModel(selected_alpha, PREPROCESSING_POLICY)
            combo_run_id = f"{run_id}-{model_name}-{feature_set}"
            predicted = model.fit_predict_bundle(tables, feature_set, combo_run_id)
            expected = joined[joined["split"].isin(("train", "validation"))]
            verify_prediction_frame(predicted, expected)
            if predicted["split"].eq("test").any():
                raise AssertionError("Development runner emitted test predictions")
            predictions[f"{model_name}:{feature_set}"] = predicted
            metrics = _metrics(predicted)
            metrics["model"] = model_name
            metrics["feature_set"] = feature_set
            metrics["selected_ridge_alpha"] = selected_alpha
            metric_rows.append(metrics)

    output_root.mkdir(parents=True)
    for key, predicted in predictions.items():
        model_name, feature_set = key.split(":")
        destination = output_root / model_name / f"{feature_set}.predictions.csv"
        destination.parent.mkdir(parents=True, exist_ok=True)
        predicted[PREDICTION_COLUMNS].to_csv(destination, index=False, lineterminator="\n")
    pd.concat(metric_rows, ignore_index=True).to_csv(output_root / "validation_metrics.csv", index=False, lineterminator="\n")
    pd.DataFrame(alpha_rows).to_csv(output_root / "ridge_alpha_selection.csv", index=False, lineterminator="\n")
    comparison = pd.DataFrame([
        _paired_bootstrap(predictions, model, seed + index, bootstrap_repetitions)
        for index, model in enumerate(("linear_regression", "ridge_regression"))
    ])
    comparison.to_csv(output_root / "paired_validation_comparison.csv", index=False, lineterminator="\n")

    metadata = {
        "protocol_version": "2.0", "technical_contract_status": "draft",
        "evidence_status": "development_validation_only",
        "purpose": "development_debugging", "run_id": run_id,
        "bundle_id": Path(bundle_path).name, "bundle_manifest_sha256": bundle_manifest_sha256,
        "models": ["linear_regression", "ridge_regression"],
        "feature_sets": {name: feature_names(name) for name in ("sales_only", "stockout_aware")},
        "preprocessing_policy": PREPROCESSING_POLICY, "prediction_postprocessing": "none",
        "ridge_alpha_candidates": ALPHA_CANDIDATES, "selected_ridge_alphas": selected_alphas,
        "bootstrap": {"seed_by_model": {"linear_regression": seed, "ridge_regression": seed + 1},
                      "repetitions": bootstrap_repetitions, "unit": "store-product series",
                      "interval": "percentile 95%", "difference": "MAE(stockout_aware) - MAE(sales_only)"},
        "split_populations": manifest["split_counts"],
        "generated_predictions": "train and validation only; test blocked",
        "source_git_revision": _git_revision(), "python": sys.version,
        "platform": platform.platform(), "numpy": np.__version__, "pandas": pd.__version__,
    }
    (output_root / "run_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# DEVGRU development experiment report", "", "Status: DEVELOPMENT VALIDATION ONLY; PROVISIONAL SETTINGS.", "",
        f"Bundle: `{metadata['bundle_id']}`", f"Trusted manifest SHA-256: `{bundle_manifest_sha256}`", "",
        "No development test rows were predicted, scored, or used for selection. The final bundle was not opened.", "",
        "## Validation metrics", "", pd.concat(metric_rows, ignore_index=True).to_string(index=False), "",
        "## Ridge alpha selection", "", pd.DataFrame(alpha_rows).to_string(index=False), "",
        "## Paired comparison", "", comparison.to_string(index=False), "",
        "Bootstrap resampled whole store-product series with reproducible percentile 95% intervals. Negative MAE differences favor stockout-aware forecasting.",
    ]
    (output_root / "development_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return output_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DEVGRU development-only Linear/Ridge experiments")
    parser.add_argument("bundle_path")
    parser.add_argument("expected_manifest_sha256")
    parser.add_argument("output_root")
    parser.add_argument("run_id")
    parser.add_argument("--seed", type=int, default=245)
    parser.add_argument("--bootstrap-repetitions", type=int, default=BOOTSTRAP_REPETITIONS)
    args = parser.parse_args()
    print(run_development(args.bundle_path, args.expected_manifest_sha256, args.output_root,
                          args.run_id, args.seed, args.bootstrap_repetitions))


if __name__ == "__main__":
    main()
