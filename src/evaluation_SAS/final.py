"""Reviewed-final evaluator: frozen settings, V2 gates, shared checks, pooled-row bootstrap.

Nothing here runs unless every V2 gate is open: the contract flags in
`configs/contract.yaml`, a jointly approved `configs/final_settings.json` with a
freeze record, and a bundle whose manifest hash and purpose match the settings.
Readiness is checked from configuration and the bundle manifest header only,
before any outcome CSV is opened. Models are fitted on the training split only;
the test split is never used for fitting or selection. Settings are read, never
tuned. Outputs are published transactionally into a new directory.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import yaml

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.bootstrap import pooled_store_interval_rows
from src.evaluation_SAS.runs import ROOT, _inventory, checked_id, new_run, read_json, source_snapshot
from src.evaluation_SAS.v2 import (
    BASELINES, CONDITIONS, PREDICTION_COLUMNS, _summarize, validate_metadata, validate_predictions,
)
from src.features_DELTA.bundle import load_bundle, sha256, write_csv, write_json
from src.features_DELTA.v2 import COMMON, EXTRA

FINAL_PURPOSE = "final_experiment"
SPLITS = ("train", "validation", "test")
REPORTED_SPLITS = ("validation", "test")
CONTRACT_GATES = ("contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed")
REQUIRED_APPROVERS = {"DELTA", "DEVGRU", "SAS"}
LEARNED_ORDER = ("linear_regression", "ridge_regression", "decision_tree", "random_forest")
SETTINGS_PATH = Path("configs/final_settings.json")
UNCERTAINTY = {"method": "paired_store_cluster_percentile", "weighting": "pooled_row",
               "difference": "MAE_stockout_aware_minus_sales_only", "confidence_level": 0.95,
               "replicates": 2000, "seed": 245}
FINAL_LIMITATIONS = [
    "Conditional on the frozen fitted models and settings; no refitting or tuning uncertainty",
    "Assumes independent stores; shared calendar shocks and cross-store dependence are not addressed",
    "Observed-store resampling does not establish population representativeness",
    "Historical holdout exposure and retrospective series completeness remain limitations",
    "Overall intervals do not imply subgroup intervals; no multiple-comparison adjustment",
]


def _positive_int(value, name, *, allow_none=False):
    if value is None and allow_none:
        return
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def validate_settings(settings):
    """Strict schema check. It never decides approval; it only reads it."""
    required = {"settings_version", "status", "approved", "approvals", "freeze_record", "protocol_version",
                "purpose", "final_bundle", "fit_split", "selection", "prediction_postprocessing", "models",
                "baselines", "uncertainty", "provenance"}
    if set(settings) != required:
        raise ValueError("Unexpected/missing final settings fields")
    if (settings["protocol_version"] != "2.0" or settings["purpose"] != FINAL_PURPOSE
            or settings["fit_split"] != "train" or settings["selection"] != "frozen_settings_no_final_tuning"
            or settings["prediction_postprocessing"] != "none"):
        raise ValueError("Final settings contradict the approved V2 protocol")
    if type(settings["approved"]) is not bool or not isinstance(settings["approvals"], list):
        raise ValueError("approved must be boolean and approvals a list")
    bundle = settings["final_bundle"]
    if (not isinstance(bundle, dict) or set(bundle) != {"bundle_id", "manifest_sha256"}
            or not isinstance(bundle["manifest_sha256"], str) or len(bundle["manifest_sha256"]) != 64):
        raise ValueError("final_bundle needs bundle_id and a 64-character manifest SHA-256")
    if settings["uncertainty"] != UNCERTAINTY:
        raise ValueError("Uncertainty settings differ from the approved pooled-row store bootstrap")
    if settings["baselines"] != list(BASELINES):
        raise ValueError("Both required baselines must be scored")
    models = settings["models"]
    if not isinstance(models, dict) or set(models) != set(LEARNED_ORDER):
        raise ValueError("Settings must list every learned model, enabled or not")
    for name in ("linear_regression", "ridge_regression", "decision_tree"):
        if models[name].get("enabled") is not True:
            raise ValueError("Linear, Ridge and Decision Tree are required in the final comparison")
    if type(models["random_forest"].get("enabled")) is not bool:
        raise ValueError("random_forest.enabled must be boolean")
    for name in ("linear_regression", "ridge_regression"):
        if models[name].get("preprocessing") != "standardize":
            raise ValueError("Linear/Ridge require training-only standardization")
    alphas = models["ridge_regression"].get("alpha")
    if not isinstance(alphas, dict) or set(alphas) != set(CONDITIONS) or not all(
            isinstance(a, (int, float)) and not isinstance(a, bool) and np.isfinite(a) and a > 0
            for a in alphas.values()):
        raise ValueError("Ridge needs one finite positive alpha per condition")
    for name in ("decision_tree", "random_forest"):
        spec = models[name]
        if type(spec.get("random_state")) is not int:
            raise ValueError(f"{name} needs a fixed integer random_state")
        parameters = spec.get("parameters")
        if not isinstance(parameters, dict) or set(parameters) != set(CONDITIONS):
            raise ValueError(f"{name} needs parameters for both conditions")
        for condition in CONDITIONS:
            if set(parameters[condition]) != {"max_depth", "min_samples_leaf"}:
                raise ValueError(f"{name} parameters must be max_depth/min_samples_leaf only")
            _positive_int(parameters[condition]["max_depth"], "max_depth", allow_none=True)
            _positive_int(parameters[condition]["min_samples_leaf"], "min_samples_leaf")
    forest = models["random_forest"]
    _positive_int(forest.get("n_estimators"), "n_estimators")
    if forest.get("max_features") != 1.0 or forest.get("bootstrap") is not True:
        raise ValueError("Random Forest max_features/bootstrap differ from the development policy")
    return settings


def _approval_blockers(settings):
    blockers = []
    if settings["approved"] is not True or settings["status"] != "APPROVED":
        blockers.append("final_settings_not_jointly_approved")
    approvers = {item.get("codename") for item in settings["approvals"]
                 if isinstance(item, dict) and item.get("date") and item.get("github")}
    if not REQUIRED_APPROVERS <= approvers:
        blockers.append("missing_recorded_approvals_from_" + "_".join(sorted(REQUIRED_APPROVERS - approvers)))
    if not settings["freeze_record"]:
        blockers.append("missing_freeze_record")
    return blockers


def inspect_final_readiness(root=ROOT, settings_path=SETTINGS_PATH, bundle=None):
    """Configuration/manifest-header check only; never opens an outcome CSV."""
    root = Path(root)
    blockers = []
    registration = yaml.safe_load((root / "configs/contract.yaml").read_text(encoding="utf-8")) or {}
    blockers += [name for name in CONTRACT_GATES if registration.get(name) is not True]
    settings, settings_sha = None, None
    path = root / settings_path
    if not path.is_file():
        blockers.append("missing_final_settings_file")
    else:
        try:
            settings = validate_settings(read_json(path))
            settings_sha = sha256(path)
            blockers += _approval_blockers(settings)
        except ValueError as error:
            blockers.append(f"invalid_final_settings: {error}")
    if bundle is not None:
        manifest_path = Path(bundle) / "bundle_manifest.json"
        if not manifest_path.is_file():
            blockers.append("missing_bundle_manifest")
        else:
            if settings and sha256(manifest_path) != settings["final_bundle"]["manifest_sha256"]:
                blockers.append("bundle_manifest_hash_differs_from_frozen_settings")
            if read_json(manifest_path).get("purpose") != FINAL_PURPOSE:
                blockers.append("bundle_purpose_is_not_final_experiment")
    return {"ready_for_final_scoring": not blockers, "blocking_requirements": blockers,
            "final_data_opened": False, "settings_sha256": settings_sha, "settings": settings}


def _enabled_models(settings):
    return [m for m in LEARNED_ORDER if settings["models"][m]["enabled"]]


def fit_predict(tables, settings, run_id):
    """Fit enabled models on train rows only; predict every split with frozen settings."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor
    from src.models.baselines_DELTA.v2 import predictions as baseline_predictions
    from src.models.linear_regression_DEVGRU.model import LinearRegressionModel
    from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel

    models, observations = settings["models"], tables["observations"]
    train = observations.split.eq("train")
    frames = []
    for condition in CONDITIONS:
        names = COMMON if condition == "sales_only" else COMMON + EXTRA
        joined = observations.merge(tables[f"features_{condition}"], on=KEY, how="left",
                                    validate="one_to_one", sort=False)
        if joined[names].isna().any().any():
            raise ValueError(f"Missing predictor values for {condition}")
        x_train, y_train = joined.loc[train, names], joined.loc[train, "actual"]
        for name in _enabled_models(settings):
            if name == "linear_regression":
                estimator = LinearRegressionModel(models[name]["preprocessing"])
            elif name == "ridge_regression":
                estimator = RidgeRegressionModel(float(models[name]["alpha"][condition]),
                                                 models[name]["preprocessing"])
            elif name == "decision_tree":
                estimator = DecisionTreeRegressor(criterion="squared_error", splitter="best",
                                                  random_state=models[name]["random_state"],
                                                  **models[name]["parameters"][condition])
            else:
                spec = models[name]
                estimator = RandomForestRegressor(criterion="squared_error", n_estimators=spec["n_estimators"],
                                                  max_features=spec["max_features"], bootstrap=spec["bootstrap"],
                                                  random_state=spec["random_state"], n_jobs=1,
                                                  **spec["parameters"][condition])
            if name in ("linear_regression", "ridge_regression"):
                estimator.fit(x_train.to_numpy(dtype=float), y_train.to_numpy(dtype=float))
                predicted = estimator.predict(joined[names].to_numpy(dtype=float))
            else:
                estimator.fit(x_train, y_train)
                predicted = estimator.predict(joined[names])
            output = joined[KEY + ["actual", "split"]].copy()
            output["prediction"] = np.asarray(predicted, dtype=float)
            output["model"], output["feature_set"], output["run_id"] = name, condition, run_id
            frames.append(output[PREDICTION_COLUMNS])
    frames.append(baseline_predictions(tables, run_id)[PREDICTION_COLUMNS])
    return pd.concat(frames, ignore_index=True)


def evaluate_final(predictions, observations, metadata, models, splits=REPORTED_SPLITS):
    """Shared exact-coverage checks, protocol metrics and pooled-row paired intervals."""
    audit = validate_predictions(predictions, observations, models, list(SPLITS))
    validate_metadata(metadata, observations)
    scored = predictions.loc[predictions.split.isin(splits)]
    joined = scored.merge(metadata, on=KEY, how="left", validate="many_to_one")
    grouping = ["model", "feature_set", "split"]
    overall = _summarize(joined, grouping)
    subgroups = _summarize(joined, grouping + ["target_stockout_group"])
    paired = []
    for model in models:
        if model in BASELINES:
            continue
        for split in splits:
            pair = overall.loc[overall.model.eq(model) & overall.split.eq(split)].set_index("feature_set")
            sales, aware = float(pair.loc["sales_only", "MAE"]), float(pair.loc["stockout_aware", "MAE"])
            paired.append({"model": model, "split": split, "MAE_sales_only": sales, "MAE_stockout_aware": aware,
                           "MAE_difference_aware_minus_sales": aware - sales,
                           "relative_MAE_improvement_pct": None if sales == 0 else 100 * (sales - aware) / sales})
    intervals = pooled_store_interval_rows(scored, models, list(splits), FINAL_LIMITATIONS)
    return {"overall": overall, "subgroups": subgroups, "paired_comparisons": pd.DataFrame(paired),
            "per_store": _summarize(joined, grouping + ["store_id"]),
            "per_series": _summarize(joined, grouping + SERIES),
            "mae_difference_intervals": intervals,
            "coverage_audit": {"exact_coverage_verified": True, "conditions": audit,
                               "validated_splits": list(SPLITS), "reported_splits": list(splits),
                               "metadata_coverage_verified": True}}


def run_final(bundle, destination, run_id, *, root=ROOT, settings_path=SETTINGS_PATH):
    """The single reviewed final entry point. Refuses before opening data unless every gate is open."""
    checked_id(run_id)
    bundle, destination = Path(bundle), Path(destination)
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite final run: {destination}")
    if destination.resolve().is_relative_to(bundle.resolve()):
        raise ValueError("Final output must be outside the input bundle")
    readiness = inspect_final_readiness(root, settings_path, bundle)
    if not readiness["ready_for_final_scoring"]:
        raise RuntimeError("Final scoring blocked: " + ", ".join(readiness["blocking_requirements"]))
    settings = readiness["settings"]
    expected = settings["final_bundle"]["manifest_sha256"]
    tables, manifest = load_bundle(bundle, expected_manifest_sha256=expected)
    if manifest.get("purpose") != FINAL_PURPOSE:
        raise ValueError("Final evaluator requires a final_experiment bundle")
    if set(tables["observations"].split) != set(SPLITS):
        raise ValueError("Final bundle must contain train, validation and test splits")
    models = [*_enabled_models(settings), *BASELINES]
    predictions = fit_predict(tables, settings, run_id)
    report = evaluate_final(predictions, tables["observations"], tables["evaluation_metadata"], models)
    import sklearn
    with new_run(destination) as temporary:
        write_csv(temporary / "predictions.csv", predictions)
        for name in ("overall", "subgroups", "paired_comparisons", "per_store", "per_series",
                     "mae_difference_intervals"):
            write_csv(temporary / f"{name}.csv", report[name])
        write_json(temporary / "coverage_audit.json", report["coverage_audit"])
        run_manifest = {
            "protocol_version": "2.0", "purpose": FINAL_PURPOSE, "evidence_status": "FINAL_FROZEN_SETTINGS",
            "owner": "SAS", "run_id": run_id, "bundle_id": manifest.get("bundle_id"),
            "bundle_manifest_sha256": expected, "settings_sha256": readiness["settings_sha256"],
            "settings": settings, "models": models, "fit_split": "train", "reported_splits": list(REPORTED_SPLITS),
            "uncertainty": UNCERTAINTY, "limitations": FINAL_LIMITATIONS,
            "generated_utc": datetime.now(timezone.utc).isoformat(), "source": source_snapshot(),
            "environment": {"python": platform.python_version(), "numpy": np.__version__,
                            "pandas": pd.__version__, "scikit-learn": sklearn.__version__},
            "artifacts": _inventory(temporary)}
        write_json(temporary / "run_manifest.json", run_manifest)
    return run_manifest
