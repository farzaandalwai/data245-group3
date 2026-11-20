"""Pinned bundle consumers and immutable local prediction/comparison artifacts."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd

from src.evaluation_SAS.v2 import (
    BASELINES, PREDICTION_COLUMNS, development_gate, evaluate_predictions,
    validate_predictions,
)
from src.features_DELTA.bundle import load_bundle, sha256, write_csv, write_json


ROOT = Path(__file__).resolve().parents[2]


def read_json(path):
    def pairs(items):
        result = {}
        for name, value in items:
            if name in result:
                raise ValueError(f"Duplicate JSON field: {name}")
            result[name] = value
        return result

    def invalid(value):
        raise ValueError(f"Nonfinite JSON value: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=invalid)


def checked_id(run_id):
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError("Run IDs may contain only letters, digits, hyphen and underscore")
    return run_id


def pinned_bundle(path, manifest_sha256):
    if not isinstance(manifest_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256):
        raise ValueError("Supply the trusted 64-character lowercase bundle manifest SHA-256")
    # Reject final-purpose manifests before load_bundle can open any outcome CSV.
    if sha256(Path(path) / "bundle_manifest.json") != manifest_sha256:
        raise ValueError("Bundle manifest identity mismatch")
    header = read_json(Path(path) / "bundle_manifest.json")
    development_gate(header.get("purpose"), ("validation",))
    tables, manifest = load_bundle(path, expected_manifest_sha256=manifest_sha256)
    development_gate(manifest["purpose"], ("validation",))
    identity = {name: manifest[name] for name in (
        "protocol_version", "producer_contract_version", "purpose", "sample_sha256",
    )}
    identity["bundle_manifest_sha256"] = manifest_sha256
    return tables, manifest, identity


@contextmanager
def new_run(destination):
    """Publish only a complete run; remove this task's temporary files on failure."""
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(f"Immutable run already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".sas-building-", dir=destination.parent))
    try:
        yield temporary
        if destination.exists():
            raise FileExistsError(f"Immutable run already exists: {destination}")
        os.rename(temporary, destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def source_snapshot():
    paths = [*sorted((ROOT / "src/evaluation_SAS").glob("*.py")),
             *sorted((ROOT / "src/models/decision_tree_SAS").glob("*.py")),
             ROOT / "scripts/sas_v2.py", ROOT / "requirements.txt"]
    files = {path.relative_to(ROOT).as_posix(): sha256(path) for path in paths}
    return {
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "working_tree_dirty": bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()),
        "files_sha256": files,
    }


def _inventory(directory):
    return {path.name: {"sha256": sha256(path), "bytes": path.stat().st_size}
            for path in sorted(directory.iterdir()) if path.is_file()}


def train_tree_run(bundle, manifest_sha256, destination, run_id, policy_path):
    # Keep the evaluator usable without importing sklearn or a model's internals.
    import sklearn
    import scipy
    from src.models.decision_tree_SAS.v2 import fit_development, serialize_tree, validate_policy

    checked_id(run_id)
    if Path(destination).exists():
        raise FileExistsError(f"Immutable run already exists: {destination}")
    tables, _, identity = pinned_bundle(bundle, manifest_sha256)
    policy = read_json(policy_path)
    validate_policy(policy)
    predicted, selection, estimators = fit_development(
        tables, policy, purpose=identity["purpose"], run_id=run_id)
    report = evaluate_predictions(
        predicted, tables["observations"], tables["evaluation_metadata"],
        purpose=identity["purpose"], models=["decision_tree"], splits=("train", "validation"))
    with new_run(destination) as temporary:
        write_csv(temporary / "predictions.csv", predicted)
        write_csv(temporary / "development_metrics.csv", report["overall"])
        write_csv(temporary / "mae_difference_intervals.csv", report["mae_difference_intervals"])
        write_json(temporary / "selection.json", selection)
        write_json(temporary / "coverage_audit.json", report["coverage_audit"])
        for condition, estimator in estimators.items():
            write_json(temporary / f"{condition}_tree.json", serialize_tree(estimator))
        manifest = {
            **identity, "prediction_run_version": "2.0-development-1", "owner": "SAS",
            "run_id": run_id, "models": ["decision_tree"], "scored_splits": ["train", "validation"],
            "evidence_status": report["coverage_audit"]["evidence_status"],
            "technical_contract_status": "draft", "group_validation_choices_frozen": False,
            "test_scored": False, "generated_utc": datetime.now(timezone.utc).isoformat(),
            "uncertainty": report["coverage_audit"]["uncertainty"],
            "policy": policy, "policy_file_sha256": sha256(policy_path),
            "selected_parameters": selection["selected_parameters"],
            "training_rows": selection["training_rows"], "validation_rows": selection["validation_rows"],
            "source": source_snapshot(),
            "environment": {"python": platform.python_version(), "numpy": np.__version__,
                            "pandas": pd.__version__, "scikit-learn": sklearn.__version__,
                            "scipy": scipy.__version__},
            "artifacts": _inventory(temporary),
        }
        write_json(temporary / "run_manifest.json", manifest)
        # Verify serialized values and provenance through the exchange consumer.
        load_prediction_run(temporary, identity, tables["observations"])
    return manifest


def load_prediction_run(directory, identity, observations):
    """Read standardized predictions, including DELTA's existing V2 baselines.

    The exact bundle-manifest hash binds DELTA baselines to the producer/sample
    even though their older manifest omits separate sample/producer fields.
    """
    directory = Path(directory)
    manifest = read_json(directory / "run_manifest.json")
    for name in ("protocol_version", "purpose", "bundle_manifest_sha256"):
        if manifest.get(name) != identity[name]:
            raise ValueError(f"Incompatible prediction run {name}")
    models = manifest.get("models")
    if not isinstance(models, list) or not models or not all(isinstance(m, str) for m in models):
        raise ValueError("Prediction manifest needs explicit models")
    run_id = checked_id(manifest.get("run_id"))
    delta_baseline = (set(models) <= set(BASELINES) and "prediction_run_version" not in manifest)
    if delta_baseline:
        scored_splits = ["train", "validation", "test"]
    else:
        if manifest.get("prediction_run_version") != "2.0-development-1":
            raise ValueError("Unsupported development prediction manifest")
        for name in ("sample_sha256", "producer_contract_version"):
            if manifest.get(name) != identity[name]:
                raise ValueError(f"Incompatible prediction run {name}")
        scored_splits = manifest.get("scored_splits")
        development_gate(identity["purpose"], scored_splits)
        if manifest.get("test_scored") is not False:
            raise ValueError("Learned-model runs may not score test observations")
        if (not isinstance(manifest.get("source"), dict)
                or not isinstance(manifest.get("environment"), dict)
                or not isinstance(manifest.get("policy"), dict)
                or not isinstance(manifest.get("selected_parameters"), dict)):
            raise ValueError("Development run lacks source/environment/policy/selection provenance")
    artifacts = manifest.get("artifacts", {})
    if not isinstance(artifacts, dict) or "predictions.csv" not in artifacts:
        raise ValueError("Prediction artifact is not registered")
    for name, record in artifacts.items():
        if Path(name).name != name or "\\" in name or name in (".", "..", "run_manifest.json"):
            raise ValueError("Unsafe run artifact name")
        digest = record if isinstance(record, str) else record.get("sha256")
        path = directory / name
        if sha256(path) != digest:
            raise ValueError(f"Prediction run artifact integrity mismatch: {name}")
        if isinstance(record, dict) and path.stat().st_size != record.get("bytes"):
            raise ValueError(f"Prediction run artifact size mismatch: {name}")
    predicted = pd.read_csv(directory / "predictions.csv", converters={"actual": float, "prediction": float})
    if list(predicted) != PREDICTION_COLUMNS or set(predicted.run_id) != {run_id}:
        raise ValueError("Prediction schema/run ID differs from manifest")
    validate_predictions(predicted, observations, models, scored_splits)
    return predicted, manifest


def evaluate_runs(bundle, manifest_sha256, run_directories, destination, run_id, models,
                  splits=("validation",)):
    checked_id(run_id)
    if Path(destination).exists():
        raise FileExistsError(f"Immutable comparison already exists: {destination}")
    tables, _, identity = pinned_bundle(bundle, manifest_sha256)
    development_gate(identity["purpose"], splits)
    if not run_directories:
        raise ValueError("At least one prediction run is required")
    frames, inputs = [], []
    for directory in run_directories:
        predicted, manifest = load_prediction_run(directory, identity, tables["observations"])
        # Baseline files can contain historical development-test records. They
        # are structurally checked above, never passed to the metric functions.
        frames.append(predicted.loc[predicted.split.isin(splits)].copy())
        inputs.append({"run_id": manifest["run_id"], "models": manifest["models"],
                       "run_manifest_sha256": sha256(Path(directory) / "run_manifest.json")})
    predicted = pd.concat(frames, ignore_index=True)
    report = evaluate_predictions(
        predicted, tables["observations"], tables["evaluation_metadata"],
        purpose=identity["purpose"], models=models, splits=splits)
    with new_run(destination) as temporary:
        for name in ("overall", "subgroups", "per_series", "per_store", "paired_comparisons", "mae_difference_intervals"):
            write_csv(temporary / f"{name}.csv", report[name])
        write_json(temporary / "coverage_audit.json", report["coverage_audit"])
        manifest = {**identity, "comparison_version": "2.0-development-1", "owner": "SAS",
                    "run_id": run_id, "models": list(models), "scored_splits": list(splits),
                    "evidence_status": report["coverage_audit"]["evidence_status"],
                    "test_scored": False, "uncertainty_status": "implemented_development_paired_store_bootstrap",
                    "uncertainty": report["coverage_audit"]["uncertainty"],
                    "technical_contract_status": "draft", "prediction_runs": inputs,
                    "generated_utc": datetime.now(timezone.utc).isoformat(), "source": source_snapshot(),
                    "environment": {"python": platform.python_version(), "numpy": np.__version__,
                                    "pandas": pd.__version__},
                    "artifacts": _inventory(temporary)}
        write_json(temporary / "comparison_manifest.json", manifest)
    return manifest
