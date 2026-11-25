"""Submission demo of the approved V2 final stockout-aware Ridge (not a new run).

From the repository root, with the recorded Python 3.12 scientific environment:
    python -B submission_local/demo/ml_pipeline.py --build-model --bundle PATH
    python -B submission_local/demo/ml_pipeline.py --demo
    python -B submission_local/demo/ml_pipeline.py --demo --bundle PATH

PATH is the existing v2-final-1000-r2 DELTA bundle. Build never overwrites a
saved artifact. Demo never fits. Without --bundle, demo uses one authentic test
observation embedded in the artifact so a live presentation needs no dataset.
With --bundle, demo also checks all test predictions against recorded MAE.
Optional --reference-predictions accepts only the hash-pinned final-run CSV.

Owner: DELTA / Timothytran109. Task checkout: main at b4df926; no Git publication.
Scope: exactly this entry point and stockout_aware_ridge.joblib; existing source,
frozen configs and results are read-only. User request: reuse DELTA features and
the approved 1,000-series final Ridge, alpha=100, 14-day past-only history,
chronological splits, training-only scaling/fitting, and honest verification.
Dependencies/acceptance: authentic pinned bundle, existing DEVGRU solver, frozen
settings, 14 ordered features, fresh-process no-fit inference, MAE comparison.

Training calls the unchanged DEVGRU augmented least-squares implementation.
Its learned scaler/Ridge arrays are restored into standard sklearn estimators
for portable inference; sklearn Ridge.fit is never used. This retains the exact
DEVGRU preprocessing arithmetic, including its population standard deviation.
The artifact contains library versions, provenance, numeric DEVGRU state and a
fitted StandardScaler -> Ridge Pipeline. Only trusted joblib files may be loaded.
Historical test exposure and retrospective cohort completeness still apply.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "final-1000-attested-20261124T094349Z"
EVIDENCE = ROOT / "docs" / "final_execution_evidence" / RUN_ID
BUNDLE_SHA256 = "52f4faec954ee311970bb567682d4ac7b466a2d5b8ce7f8c87af5d171fc6af7c"
SAMPLE_SHA256 = "830d30a1249f609ad3c95c37032d2e7b7f0d5671fc7ad8864ad8b5e31d1356e7"
FEATURES = [
    "sales_lag_1", "sales_lag_2", "sales_lag_3", "sales_lag_7", "sales_lag_14",
    "sales_mean_7", "sales_mean_14", "weekday", "is_weekend",
    "stockout_hours_lag_1", "stockout_hours_mean_7", "stockout_hours_mean_14",
    "stockout_day_fraction_7", "stockout_day_fraction_14",
]
KEY = ["store_id", "product_id", "dt"]
COUNTS = {"train": 46000, "validation": 15000, "test": 15000}
REPORTED_MAE = 0.377191379885
TOLERANCE = 1e-12
FORMAT = "data245-submission-ridge-1"
DEFAULT_MODEL = Path(__file__).with_name("stockout_aware_ridge.joblib")


def _producer_imports():
    # Only bundle/build paths need this repository. Embedded-row demo is portable.
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from src.features_DELTA.bundle import load_bundle, sha256
    from src.features_DELTA.v2 import COMMON, EXTRA
    from src.models.linear_regression_DEVGRU.core import keyed_observations

    if COMMON + EXTRA != FEATURES:
        raise ValueError("DELTA feature order differs from the frozen 14 features")
    return load_bundle, sha256, keyed_observations


def load_inputs(bundle):
    """Reuse DELTA's serialized features and its integrity/coverage/split checks."""
    load_bundle, _, keyed_observations = _producer_imports()
    tables, manifest = load_bundle(bundle, expected_manifest_sha256=BUNDLE_SHA256)
    joined = keyed_observations(tables, "stockout_aware")
    if (manifest["bundle_id"] != "v2-final-1000-r2"
            or manifest["sample_sha256"] != SAMPLE_SHA256
            or manifest["purpose"] != "final_experiment"
            or joined.split.value_counts().to_dict() != COUNTS
            or len(joined[KEY[:2]].drop_duplicates()) != 1000):
        raise ValueError("Bundle is not the approved final cohort/splits")
    return joined, manifest


def reference_comparison(joined, predicted, path):
    """Compare by keys, actuals and splits; never silently discard missing rows."""
    if path is None or not path.is_file():
        if path is not None:
            raise FileNotFoundError(path)
        return {"status": "UNVERIFIED: original final predictions.csv unavailable"}
    _, sha256, _ = _producer_imports()
    run = json.loads((EVIDENCE / "run_manifest.json").read_text())
    expected = run["artifacts"]["predictions.csv"]
    if sha256(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]:
        raise ValueError("Reference CSV does not match the authentic final-run hash")
    saved = pd.read_csv(path, converters={"actual": float, "prediction": float})
    saved = saved.loc[(saved.model == "ridge_regression")
                      & (saved.feature_set == "stockout_aware")
                      & (saved.run_id == RUN_ID)]
    current = joined[KEY + ["actual", "split"]].assign(prediction=predicted)
    matched = current.merge(saved[KEY + ["actual", "split", "prediction"]],
                            on=KEY, how="outer", validate="one_to_one",
                            suffixes=("_demo", "_final"), indicator=True)
    if (len(matched) != len(joined) or not matched._merge.eq("both").all()
            or not np.array_equal(matched.actual_demo, matched.actual_final)
            or not np.array_equal(matched.split_demo, matched.split_final)
            or not np.isfinite(matched.prediction_final).all()):
        raise ValueError("Final reference has different keys/actuals/splits/coverage")
    difference = float(np.max(np.abs(matched.prediction_demo - matched.prediction_final)))
    return {"status": "MATCH" if difference <= TOLERANCE else "DIFFERENT",
            "rows": len(matched), "max_absolute_prediction_difference": difference,
            "reference_sha256": expected["sha256"]}


def verify(pipeline, joined, reference=None):
    predicted = pipeline.predict(joined[FEATURES])
    if not np.isfinite(predicted).all():
        raise ValueError("Nonfinite predictions")
    test = joined.split.eq("test").to_numpy()
    mae = float(np.mean(np.abs(predicted[test] - joined.loc[test, "actual"].to_numpy())))
    result = {"test_rows": int(test.sum()), "test_mae": mae,
              "reported_test_mae": REPORTED_MAE,
              "difference_from_reported_mae": mae - REPORTED_MAE,
              "mae_matches_at_1e_12": abs(mae - REPORTED_MAE) <= TOLERANCE,
              "prediction_comparison": reference_comparison(joined, predicted, reference)}
    overall_path = EVIDENCE / "overall.csv"
    if overall_path.is_file():
        overall = pd.read_csv(overall_path, converters={"MAE": float})
        row = overall.loc[(overall.model == "ridge_regression")
                          & (overall.feature_set == "stockout_aware") & (overall.split == "test")]
        if len(row) != 1:
            raise ValueError("Recorded final Ridge MAE is ambiguous")
        result["recorded_full_precision_mae"] = float(row.MAE.iloc[0])
        result["difference_from_full_precision_mae"] = mae - result["recorded_full_precision_mae"]
    return result


def build_model(bundle, destination, reference):
    joined, manifest = load_inputs(bundle)
    from src.models.linear_regression_DEVGRU.artifacts import model_state
    from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel
    _, sha256, _ = _producer_imports()

    freeze = json.loads((ROOT / "docs/FINAL_FREEZE_20261124T094349Z.json").read_text())
    settings_path = EVIDENCE / "final_settings_at_execution.json"
    settings = json.loads(settings_path.read_text())
    ridge_settings = settings["models"]["ridge_regression"]
    if (sha256(settings_path) != freeze["settings_sha256"]
            or not settings["approved"] or settings["fit_split"] != "train"
            or settings["prediction_postprocessing"] != "none"
            or ridge_settings["alpha"]["stockout_aware"] != 100
            or ridge_settings["preprocessing"] != "standardize"):
        raise ValueError("Frozen final settings do not match this demo")
    sources = ["src/features_DELTA/v2.py", "src/features_DELTA/bundle.py",
               "src/data_preprocessing_DELTA/v2.py",
               "src/models/linear_regression_DEVGRU/core.py",
               "src/models/ridge_regression_DEVGRU/model.py"]
    source_hashes = {name: sha256(ROOT / name) for name in sources}
    if any(digest != freeze["source_files_sha256"][name]
           for name, digest in source_hashes.items()):
        raise ValueError("A feature/training source differs from the approved freeze")

    train = joined.loc[joined.split.eq("train")]
    x_train = train[FEATURES].to_numpy(dtype=float)
    y_train = train.actual.to_numpy(dtype=float)
    fitted = RidgeRegressionModel(alpha=100.0, preprocessing_policy="standardize")
    fitted.fit(x_train, y_train)  # The only fitting call: exactly 46,000 TRAIN rows.

    # Restore StandardScaler from the existing training-only standardizer, without
    # changing floating-point reduction order by fitting a different implementation.
    scaler = StandardScaler()
    scaler.mean_ = fitted.preprocessor.mean_.copy()
    scaler.scale_ = fitted.preprocessor.scale_.copy()
    scaler.var_ = x_train.var(axis=0)
    scaler.n_features_in_ = len(FEATURES)
    scaler.n_samples_seen_ = np.int64(len(train))
    scaler.feature_names_in_ = np.asarray(FEATURES, dtype=object)
    ridge = Ridge(alpha=100.0, fit_intercept=True)
    ridge.coef_, ridge.intercept_ = fitted.coef_.copy(), fitted.intercept_
    ridge.n_features_in_, ridge.n_iter_ = len(FEATURES), None
    pipeline = Pipeline([("scaler", scaler), ("ridge", ridge)])
    # A state export must preserve the actual DEVGRU predictions on every row.
    original = fitted.predict(joined[FEATURES].to_numpy(dtype=float))
    exported = pipeline.predict(joined[FEATURES])
    np.testing.assert_array_equal(exported, original)
    verification = verify(pipeline, joined, reference)
    test_row = joined.loc[joined.split.eq("test")].iloc[0]
    demo_row = {name: float(test_row[name]) for name in FEATURES + ["actual"]}
    demo_row.update({"store_id": int(test_row.store_id),
                     "product_id": int(test_row.product_id), "dt": str(test_row["dt"]), "split": "test"})
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                              capture_output=True, check=True).stdout.strip()
    artifact = {
        "format": FORMAT, "experiment_version": "2.0", "purpose": "submission_demo_reproduction",
        "pipeline": pipeline, "feature_names": FEATURES, "devgru_model_state": model_state(fitted, "stockout_aware"),
        "model_configuration": {"alpha": 100.0, "preprocessing": "standardize",
                                "fit_intercept": True, "random_state": None,
                                "random_state_reason": "Deterministic numpy.linalg.lstsq; no RNG in Ridge",
                                "training_solver": "DEVGRU augmented numpy.linalg.lstsq(rcond=None)",
                                "sklearn_estimators": "Inference-only numeric-state export; no sklearn Ridge.fit",
                                "prediction_postprocessing": "none", "lookback_days": 14},
        "library_versions": {"python": platform.python_version(), **{
            name: version(name) for name in ("numpy", "pandas", "scikit-learn", "scipy", "joblib", "PyYAML", "threadpoolctl")}},
        "training_provenance": {
            "status": "REPRODUCED_TRAINING; original fitted artifact unavailable",
            "source_final_run_id": RUN_ID, "source_revision": revision,
            "created_utc": datetime.now(timezone.utc).isoformat(), "owner": "DELTA / Timothytran109",
            "bundle_id": manifest["bundle_id"], "bundle_manifest_sha256": BUNDLE_SHA256,
            "sample_manifest_sha256": SAMPLE_SHA256, "sampling_seed": 245,
            "selection": manifest["sample_origin"], "split_counts": COUNTS,
            "fit_split": "train", "fit_rows": len(train),
            "fit_target_dates": [str(train.dt.min()), str(train.dt.max())],
            "validation_target_dates": ["2024-05-27", "2024-06-10"],
            "test_target_dates": ["2024-06-11", "2024-06-25"],
            "tuning": "None; retained frozen development-selected alpha=100; no validation refit",
            "settings_sha256": sha256(settings_path), "source_files_sha256": source_hashes,
            "entry_point_sha256": sha256(Path(__file__)),
            "limitations": ["Original final fitted object was not saved/found",
                            "Aggregate MAE agreement alone cannot establish prediction equality",
                            "Historical test exposure; retrospective 90-day completeness",
                            "One authentic test observation embedded solely for live inference"]},
        "demo_observation": demo_row, "verification": verification,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as handle:  # Refuse overwrite, including concurrent creation.
        joblib.dump(artifact, handle, compress=3)
    print(f"Saved {destination} ({destination.stat().st_size:,} bytes)")
    print(json.dumps(verification, indent=2))


def load_model(path):
    artifact = joblib.load(path)
    if artifact["format"] != FORMAT or artifact["feature_names"] != FEATURES:
        raise ValueError("Artifact format or 14-feature ordering mismatch")
    pipeline = artifact["pipeline"]
    if (not isinstance(pipeline, Pipeline) or list(pipeline.named_steps) != ["scaler", "ridge"]
            or not isinstance(pipeline.named_steps["scaler"], StandardScaler)
            or not isinstance(pipeline.named_steps["ridge"], Ridge)
            or pipeline.named_steps["ridge"].alpha != 100
            or pipeline.n_features_in_ != 14
            or list(pipeline.feature_names_in_) != FEATURES
            or int(pipeline.named_steps["scaler"].n_samples_seen_) != COUNTS["train"]):
        raise ValueError("Invalid fitted scaler/Ridge configuration")
    return artifact


def demo(path, bundle=None, reference=None):
    artifact = load_model(path)
    if bundle is not None:
        joined, _ = load_inputs(bundle)
        print(json.dumps(verify(artifact["pipeline"], joined, reference), indent=2))
        row = joined.loc[joined.split.eq("test")].iloc[0]
        origin = "verified final bundle"
    else:
        row = artifact["demo_observation"]
        origin = "authentic test row embedded in artifact"
    x = pd.DataFrame([[row[name] for name in FEATURES]], columns=FEATURES)
    prediction = float(artifact["pipeline"].predict(x)[0])
    actual = float(row["actual"])
    print(f"Loaded 14 features; alpha=100; inference only (no fitting). Source: {origin}.")
    print(f"Test key: store={row['store_id']}, product={row['product_id']}, date={row['dt']}")
    print(f"Prediction: {prediction:.12f} | actual recorded sales: {actual:.12f} | "
          f"absolute error: {abs(prediction - actual):.12f}")
    if bundle is None:
        print("Saved build verification: " + json.dumps(artifact["verification"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build-model", action="store_true", help="Build only if missing; never overwrite")
    mode.add_argument("--demo", action="store_true", help="Load and predict, with no fitting")
    parser.add_argument("--bundle", type=Path, help="Existing approved v2-final-1000-r2 feature bundle")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--reference-predictions", type=Path, help="Original hash-pinned final predictions.csv")
    args = parser.parse_args(argv)
    if args.reference_predictions is not None and args.bundle is None:
        parser.error("--reference-predictions requires --bundle")
    reference = args.reference_predictions
    conventional_reference = ROOT / "results/final_evaluation/v2" / RUN_ID / "predictions.csv"
    if reference is None and conventional_reference.is_file():
        reference = conventional_reference
    if args.build_model and not args.model.exists():
        if args.bundle is None:
            parser.error("Building requires --bundle pointing to the approved final bundle")
        build_model(args.bundle, args.model, reference)
    elif args.build_model:
        print("Existing artifact retained; loading without retraining.")
    demo(args.model, args.bundle, reference)


if __name__ == "__main__":
    main()
