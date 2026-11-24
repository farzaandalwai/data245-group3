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
from src.features_DELTA.bundle import write_csv, write_json
from src.data_preprocessing_DELTA.run_artifacts import (
    ROOT as PROJECT_ROOT, check_destination, checked_run_id, environment, inventory, new_run, source_snapshot,
)
from src.models.linear_regression_DEVGRU.artifacts import model_state
from src.evaluation_SAS.bootstrap import BOOTSTRAP_SPEC, paired_store_intervals
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
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT,
                              check=True, capture_output=True, text=True).stdout.strip()
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
    """Historical series-method reproduction only; not the new runner's policy."""
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
    output_root = check_destination(output_root, inputs=[bundle_path])
    checked_run_id(run_id)
    if type(seed) is not int or seed != 245 or type(bootstrap_repetitions) is not int or bootstrap_repetitions != 2000:
        raise ValueError("Approved development store intervals require seed 245 and 2000 replicates")

    if not expected_manifest_sha256 or sha256(Path(bundle_path) / "bundle_manifest.json") != expected_manifest_sha256:
        raise ValueError("A matching trusted bundle manifest SHA-256 is required")
    header = json.loads((Path(bundle_path) / "bundle_manifest.json").read_text())
    if header.get("purpose") not in ("development_debugging", "synthetic_test_only"):
        raise ValueError("Development runner rejects final-purpose bundles")
    tables, manifest = load_bundle(bundle_path, expected_manifest_sha256=expected_manifest_sha256)
    validate_paired_conditions(tables)
    bundle_manifest_sha256 = sha256(Path(bundle_path) / "bundle_manifest.json")
    if bundle_manifest_sha256 != expected_manifest_sha256:
        raise ValueError("Loaded bundle manifest does not match trusted evidence")

    predictions: dict[str, pd.DataFrame] = {}
    alpha_rows = []
    metric_rows = []
    selected_alphas = {}
    states = {}
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
            predicted = model.fit_predict_bundle(tables, feature_set, run_id)
            expected = joined[joined["split"].isin(("train", "validation"))]
            verify_prediction_frame(predicted, expected)
            if predicted["split"].eq("test").any():
                raise AssertionError("Development runner emitted test predictions")
            predictions[f"{model_name}:{feature_set}"] = predicted
            states[f"{model_name}:{feature_set}"] = model_state(model, feature_set)
            metrics = _metrics(predicted)
            metrics["model"] = model_name
            metrics["feature_set"] = feature_set
            metrics["selected_ridge_alpha"] = selected_alpha
            metric_rows.append(metrics)

    combined = pd.concat(predictions.values(), ignore_index=True)
    comparison = paired_store_intervals(
        combined.loc[combined.split.eq("validation")], tables["observations"], purpose=manifest["purpose"],
        models=["linear_regression", "ridge_regression"], splits=("validation",))
    metadata = {
        "protocol_version": "2.0", "technical_contract_status": "draft",
        "evidence_status": "SYNTHETIC_NOT_RESEARCH" if manifest["purpose"] == "synthetic_test_only" else "DEVELOPMENT_NOT_FINAL",
        "purpose": manifest["purpose"], "run_id": run_id,
        "bundle_id": Path(bundle_path).name, "bundle_manifest_sha256": bundle_manifest_sha256,
        "models": ["linear_regression", "ridge_regression"],
        "feature_sets": {name: feature_names(name) for name in ("sales_only", "stockout_aware")},
        "preprocessing_policy": PREPROCESSING_POLICY, "prediction_postprocessing": "none",
        "ridge_alpha_candidates": ALPHA_CANDIDATES, "selected_ridge_alphas": selected_alphas,
        "bootstrap": BOOTSTRAP_SPEC,
        "split_populations": manifest["split_counts"],
        "generated_predictions": "train and validation only; test blocked",
        "source_git_revision": _git_revision(), "python": sys.version,
        "platform": platform.platform(), "numpy": np.__version__, "pandas": pd.__version__,
    }
    report = [
        "# DEVGRU development experiment report", "", "Status: DEVELOPMENT VALIDATION ONLY; PROVISIONAL SETTINGS.", "",
        f"Bundle: `{metadata['bundle_id']}`", f"Trusted manifest SHA-256: `{bundle_manifest_sha256}`", "",
        "No test rows were predicted, scored, or used for selection. Final-purpose bundles are rejected.", "",
        "## Validation metrics", "", pd.concat(metric_rows, ignore_index=True).to_string(index=False), "",
        "## Ridge alpha selection", "", pd.DataFrame(alpha_rows).to_string(index=False), "",
        "## Paired comparison", "", comparison.to_string(index=False), "",
        "Approved paired whole-store bootstrap uses pooled row weighting, 2000 replicates and seed 245. Negative MAE differences favor stockout-aware forecasting.",
    ]
    # New exchange files use the already implemented SAS development envelope.
    # Existing original packages/run IDs are never rewritten or upgraded in place.
    with new_run(output_root, inputs=[bundle_path]) as temporary:
        for key, predicted in predictions.items():
            model_name, feature_set = key.split(":")
            prefix = f"{model_name}.{feature_set}"
            write_csv(temporary / f"{prefix}.predictions.csv", predicted[PREDICTION_COLUMNS])
            write_json(temporary / f"{prefix}.model.json", states[key])
        write_csv(temporary / "predictions.csv", combined)
        write_csv(temporary / "validation_metrics.csv", pd.concat(metric_rows, ignore_index=True))
        write_csv(temporary / "ridge_alpha_selection.csv", pd.DataFrame(alpha_rows))
        write_csv(temporary / "paired_validation_comparison.csv", comparison)
        write_json(temporary / "run_metadata.json", metadata)
        (temporary / "development_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
        write_json(temporary / "run_manifest.json", {
            "prediction_run_version": "2.0-development-1", "protocol_version": "2.0",
            "producer_contract_version": manifest["producer_contract_version"],
            "purpose": manifest["purpose"], "run_id": run_id, "owner": "DEVGRU",
            "bundle_manifest_sha256": bundle_manifest_sha256, "sample_sha256": manifest["sample_sha256"],
            "models": metadata["models"], "scored_splits": ["train", "validation"],
            "test_scored": False, "group_validation_choices_frozen": False,
            "evidence_status": metadata["evidence_status"],
            "policy": {"preprocessing": PREPROCESSING_POLICY, "prediction_postprocessing": "none",
                       "selection_split": "validation", "selection_metric": "MAE",
                       "ridge_alphas": ALPHA_CANDIDATES, "tie_break": "smaller_alpha_on_exact_MAE_tie",
                       "feature_sets": metadata["feature_sets"]},
            "selected_parameters": {"ridge_regression": selected_alphas, "linear_regression": {}},
            "source": source_snapshot([
                "src/models/linear_regression_DEVGRU/core.py", "src/models/linear_regression_DEVGRU/model.py",
                "src/models/ridge_regression_DEVGRU/model.py", "src/models/linear_regression_DEVGRU/artifacts.py",
                "src/models/linear_regression_DEVGRU/development.py", "src/data_preprocessing_DELTA/run_artifacts.py",
                "src/features_DELTA/v2.py", "src/features_DELTA/bundle.py", "src/data_preprocessing_DELTA/v2.py",
                "src/evaluation_SAS/bootstrap.py", "src/evaluation_SAS/v2.py"]),
            "environment": environment(), "artifacts": inventory(temporary),
            "uncertainty": BOOTSTRAP_SPEC})
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
