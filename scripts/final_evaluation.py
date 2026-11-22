"""Authorized, frozen-configuration final evaluation; never tunes on test data."""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.v2 import regression_metrics
from src.features_DELTA.bundle import load_bundle, sha256
from src.features_DELTA.v2 import COMMON, EXTRA
from src.models.linear_regression_DEVGRU.core import feature_names, keyed_observations
from src.models.linear_regression_DEVGRU.model import LinearRegressionModel
from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel

ROOT = Path(__file__).resolve().parents[1]
FINAL_MANIFEST_SHA256 = "52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c"
RIDGE_ALPHAS = {"sales_only": 10.0, "stockout_aware": 100.0}
TREE_PARAMETERS = {
    "sales_only": {"max_depth": 5, "min_samples_leaf": 5},
    "stockout_aware": {"max_depth": 5, "min_samples_leaf": 5},
}


def _git_revision():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _prediction_rows(tables, run_id):
    rows = []
    for condition in ("sales_only", "stockout_aware"):
        joined = keyed_observations(tables, condition)
        names = feature_names(condition)
        train = joined["split"].eq("train")
        models = {
            "linear_regression": LinearRegressionModel("standardize"),
            "ridge_regression": RidgeRegressionModel(RIDGE_ALPHAS[condition], "standardize"),
            "decision_tree": DecisionTreeRegressor(
                criterion="squared_error", random_state=245, splitter="best",
                **TREE_PARAMETERS[condition]),
        }
        for model_name, model in models.items():
            if model_name == "linear_regression":
                model.fit(joined.loc[train, names].to_numpy(), joined.loc[train, "actual"].to_numpy())
                predict = model.predict
            elif model_name == "ridge_regression":
                model.fit(joined.loc[train, names].to_numpy(), joined.loc[train, "actual"].to_numpy())
                predict = model.predict
            else:
                model.fit(joined.loc[train, names], joined.loc[train, "actual"])
                predict = lambda values, fitted=model: fitted.predict(values)
            output = joined[KEY + ["actual", "split"]].copy()
            output["prediction"] = predict(joined[names].to_numpy() if model_name != "decision_tree" else joined[names])
            output["model"] = model_name
            output["feature_set"] = condition
            output["run_id"] = run_id
            rows.append(output)

    joined = keyed_observations(tables, "sales_only")
    for model_name, column in (("persistence", "sales_lag_1"), ("recent_avg_7", "sales_mean_7")):
        output = joined[KEY + ["actual", "split"]].copy()
        output["prediction"] = joined[column].to_numpy()
        output["model"] = model_name
        output["feature_set"] = "common_reference"
        output["run_id"] = run_id
        rows.append(output)
    return pd.concat(rows, ignore_index=True)


def _metric_rows(predictions):
    rows = []
    for (model, condition, split), part in predictions.groupby(["model", "feature_set", "split"], sort=True):
        values = regression_metrics(part["actual"].to_numpy(), part["prediction"].to_numpy())
        rows.append({"model": model, "feature_set": condition, "split": split, **values})
    return pd.DataFrame(rows)


def _subgroup_rows(predictions, metadata):
    test = predictions[predictions["split"].eq("test")].merge(metadata, on=KEY, validate="many_to_one")
    rows = []
    for (model, condition, group), part in test.groupby(["model", "feature_set", "target_stockout_group"], sort=True):
        rows.append({"model": model, "feature_set": condition, "target_stockout_group": group,
                     **regression_metrics(part["actual"].to_numpy(), part["prediction"].to_numpy())})
    return pd.DataFrame(rows)


def _paired_intervals(predictions):
    rows = []
    for model in ("linear_regression", "ridge_regression", "decision_tree"):
        left = predictions[(predictions.model == model) & (predictions.feature_set == "sales_only") & (predictions.split == "test")]
        right = predictions[(predictions.model == model) & (predictions.feature_set == "stockout_aware") & (predictions.split == "test")]
        merged = left[KEY + ["actual", "prediction"]].merge(right[KEY + ["actual", "prediction"]], on=KEY, suffixes=("_sales", "_aware"), validate="one_to_one")
        merged["difference"] = (merged.prediction_aware - merged.actual_aware).abs() - (merged.prediction_sales - merged.actual_sales).abs()
        clusters = merged.assign(store_id=merged.store_id).groupby("store_id", sort=True)["difference"].mean().to_numpy()
        rng = np.random.default_rng(245)
        samples = clusters[rng.integers(0, len(clusters), size=(2000, len(clusters)))].mean(axis=1)
        rows.append({"model": model, "split": "test", "MAE_sales_only": float((merged.prediction_sales - merged.actual_sales).abs().mean()),
                     "MAE_stockout_aware": float((merged.prediction_aware - merged.actual_aware).abs().mean()),
                     "MAE_difference_stockout_aware_minus_sales_only": float(merged.difference.mean()),
                     "bootstrap_ci_lower": float(np.percentile(samples, 2.5)),
                     "bootstrap_ci_upper": float(np.percentile(samples, 97.5)),
                     "bootstrap_repetitions": 2000, "bootstrap_seed": 245,
                     "cluster_unit": "store_id", "clusters": int(len(clusters))})
    return pd.DataFrame(rows)


def run_final(bundle_path, output_root, run_id):
    registration = json.loads((ROOT / "configs/contract.lock.json").read_text())
    if not all(registration.get(key) is True for key in ("initial_validation_parameters_frozen", "initial_new_model_test_evaluation_allowed")):
        raise RuntimeError("Frozen contract gates are not enabled")
    bundle_path = Path(bundle_path)
    tables, manifest = load_bundle(bundle_path, expected_manifest_sha256=FINAL_MANIFEST_SHA256)
    if manifest.get("purpose") != "final_experiment":
        raise ValueError("Final evaluator requires final_experiment bundle")
    output_root = Path(output_root)
    if output_root.exists():
        raise FileExistsError(f"Refusing to overwrite final run: {output_root}")
    predictions = _prediction_rows(tables, run_id)
    expected = tables["observations"]
    if len(predictions) != len(expected) * 8 or predictions.duplicated(KEY + ["model", "feature_set", "split", "run_id"]).any():
        raise ValueError("Final prediction coverage or uniqueness check failed")
    metrics = _metric_rows(predictions)
    subgroups = _subgroup_rows(predictions, tables["evaluation_metadata"])
    intervals = _paired_intervals(predictions)
    per_store = (predictions[predictions.split == "test"].assign(error=lambda x: x.prediction - x.actual)
                 .groupby(["model", "feature_set", "store_id"], as_index=False)
                 .agg(rows=("error", "size"), MAE=("error", lambda x: float(np.mean(np.abs(x))),), signed_bias=("error", "mean")))
    output_root.mkdir(parents=True)
    predictions.to_csv(output_root / "predictions.csv", index=False, lineterminator="\n")
    metrics.to_csv(output_root / "metrics.csv", index=False, lineterminator="\n")
    subgroups.to_csv(output_root / "subgroups.csv", index=False, lineterminator="\n")
    intervals.to_csv(output_root / "paired_intervals.csv", index=False, lineterminator="\n")
    per_store.to_csv(output_root / "per_store.csv", index=False, lineterminator="\n")
    files = {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in output_root.iterdir() if p.is_file()}
    run_manifest = {"protocol_version": "2.0", "purpose": "final_experiment", "evidence_status": "FINAL_AUTHORIZED",
                    "run_id": run_id, "bundle_id": manifest["bundle_id"], "bundle_manifest_sha256": FINAL_MANIFEST_SHA256,
                    "models": ["linear_regression", "ridge_regression", "decision_tree", "persistence", "recent_avg_7"],
                    "feature_sets": {"sales_only": COMMON, "stockout_aware": COMMON + EXTRA, "baselines": "common_reference"},
                    "ridge_alphas": RIDGE_ALPHAS, "tree_parameters": TREE_PARAMETERS,
                    "preprocessing": "training_only_standardize_linear_ridge; tree_none", "prediction_postprocessing": "none",
                    "selection": "frozen development validation MAE; no final selection", "uncertainty": "paired store bootstrap, 2000 replicates, seed 245",
                    "source_revision": _git_revision(), "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
                    "limitations": manifest.get("limitations", []), "files": files}
    (output_root / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", default="data/processed/feature_bundles/v2-final-1000-r2")
    parser.add_argument("--output", default="results/final_evaluation/v2/final-authorized-20261120-r1")
    parser.add_argument("--run-id", default="final-authorized-20261120-r1")
    args = parser.parse_args()
    print(run_final(ROOT / args.bundle, ROOT / args.output, args.run_id))


if __name__ == "__main__":
    main()
