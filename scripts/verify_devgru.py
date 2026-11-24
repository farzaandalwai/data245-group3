"""Read-only saved DEVGRU metrics and final INPUT readiness; never fit or predict."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from src.features_DELTA.bundle import load_bundle, sha256
from src.models.linear_regression_DEVGRU.core import (
    KEY, feature_names, keyed_observations, verify_prediction_frame,
)

ROOT = Path(__file__).resolve().parents[1]


def verify_files(directory, records):
    """Match actual bytes to explicitly registered identities; never normalize them."""
    directory = Path(directory)
    accepted = {}
    for name, record in records.items():
        path = directory / name
        if (Path(name).is_absolute() or ".." in Path(name).parts or "\\" in name
                or path.is_symlink() or not path.resolve().is_relative_to(directory.resolve())):
            raise ValueError(f"Unsafe evidence path: {name}")
        actual = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        if actual == {k: record[k] for k in ("bytes", "sha256")}:
            accepted[name] = "published_LF_bytes"
        elif actual == record.get("windows_crlf"):
            accepted[name] = "registered_CRLF_representation_NOT_original_byte_identity"
        else:
            raise ValueError(f"Unregistered evidence bytes: {name}")
    return accepted


def verify_saved_development(bundle, directory, evidence):
    if sha256(Path(bundle) / "bundle_manifest.json") != evidence["bundle_manifest_sha256"]:
        raise ValueError("Development bundle identity mismatch")
    header = json.loads((Path(bundle) / "bundle_manifest.json").read_text())
    if header.get("purpose") != "development_debugging":
        raise ValueError("Saved development verification rejects final-purpose bundles")
    representations = verify_files(directory, evidence["files"])
    tables, manifest = load_bundle(bundle, evidence["bundle_manifest_sha256"])
    directory = Path(directory)
    metadata = json.loads((directory / "run_metadata.json").read_text(encoding="utf-8-sig"))
    if metadata.get("bundle_manifest_sha256") != evidence["bundle_manifest_sha256"]:
        raise ValueError("Saved model metadata bundle mismatch")
    metrics = pd.read_csv(directory / "validation_metrics.csv")
    selected = metadata["selected_ridge_alphas"]
    tuning = pd.read_csv(directory / "ridge_alpha_selection.csv")
    if len(metrics) != 8 or metrics.duplicated(["model", "feature_set", "split"]).any():
        raise ValueError("Saved metric coverage mismatch")
    output = []
    for model in ("linear_regression", "ridge_regression"):
        for condition in ("sales_only", "stockout_aware"):
            frame = pd.read_csv(directory / model / f"{condition}.predictions.csv",
                                converters={"actual": float, "prediction": float})
            expected = keyed_observations(tables, condition)
            expected = expected.loc[expected.split.isin(["train", "validation"])]
            verify_prediction_frame(frame, expected)
            if set(frame.model) != {model} or set(frame.feature_set) != {condition}:
                raise ValueError("Saved model/feature condition mismatch")
            for split in ("train", "validation"):
                part = frame.loc[frame.split.eq(split)]
                error = part.prediction.to_numpy() - part.actual.to_numpy()
                measured = {"MAE": float(np.mean(np.abs(error))),
                            "RMSE": float(np.sqrt(np.mean(error**2))),
                            "signed_bias": float(np.mean(error))}
                row = metrics.loc[metrics.model.eq(model) & metrics.feature_set.eq(condition)
                                  & metrics.split.eq(split)]
                if len(row) != 1 or int(row.iloc[0]["rows"]) != len(part):
                    raise ValueError("Saved metric population mismatch")
                if not all(np.isclose(measured[k], row.iloc[0][k], rtol=1e-12, atol=1e-12) for k in measured):
                    raise ValueError("Saved metrics disagree with original predictions")
                output.append({"model": model, "feature_set": condition, "split": split,
                               "rows": len(part), **measured, "run_id": frame.run_id.iloc[0]})
            if model == "ridge_regression":
                rows = tuning.loc[tuning.feature_set.eq(condition)]
                if sorted(rows.alpha.tolist()) != sorted(metadata["ridge_alpha_candidates"]):
                    raise ValueError("Saved Ridge candidate grid mismatch")
                if not np.isfinite(rows[["alpha", "validation_mae"]].to_numpy()).all():
                    raise ValueError("Nonfinite Ridge selection evidence")
                best = rows.sort_values(["validation_mae", "alpha"]).iloc[0]
                val = next(x for x in reversed(output) if x["split"] == "validation")
                if best.alpha != selected[condition] or not np.isclose(best.validation_mae, val["MAE"], rtol=1e-12, atol=1e-12):
                    raise ValueError("Saved Ridge choice differs from validation evidence")
    return {"status": "VERIFIED_FROM_SAVED_DEVELOPMENT_PREDICTIONS", "cohort": manifest["bundle_id"],
            "metrics": output, "selected_ridge_alphas": selected, "representations": representations,
            "original_fitted_models": "NOT_SAVED_NOT_RECONSTRUCTED",
            "original_execution_provenance": "base revision only; exact dirty source not established"}


def final_input_readiness(bundle, *, root=ROOT):
    """Verify existing final inputs and report gates. Never fit, predict or score."""
    evidence = json.loads((root / "docs/DELTA_V2_RUN_EVIDENCE.json").read_text())
    expected_hash = evidence["bundles"]["v2-final-1000-r2"]["manifest_sha256"]
    tables, manifest = load_bundle(bundle, expected_hash)
    if manifest["purpose"] != "final_experiment" or manifest["split_counts"] != {"train": 46000, "validation": 15000, "test": 15000}:
        raise ValueError("Unexpected final input purpose/population")
    for condition in ("sales_only", "stockout_aware"):
        joined = keyed_observations(tables, condition)
        if len(feature_names(condition)) != (9 if condition == "sales_only" else 14) or len(joined) != 76000:
            raise ValueError("Unexpected final model input dimensions")
    registration = yaml.safe_load((root / "configs/contract.yaml").read_text())
    gates = ["contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed"]
    return {"input_compatibility": "VERIFIED", "bundle_manifest_sha256": expected_hash,
            "split_counts": manifest["split_counts"],
            "blocking_gates": [k for k in gates if registration.get(k) is not True],
            "ready_for_final_execution": False,
            "joint_parameter_freeze": "NOT_VERIFIED",
            "reason": "Input compatibility is not authorization; SAS executor and joint freeze review required",
            "final_predictions_generated": False, "final_metrics_computed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=ROOT / "data/processed/feature_bundles/v2-development-200-r2")
    parser.add_argument("--package", type=Path)
    parser.add_argument("--final-inputs", type=Path)
    args = parser.parse_args()
    evidence = json.loads((ROOT / "docs/DEVGRU_DEVELOPMENT_EVIDENCE.json").read_text())
    result = verify_saved_development(args.bundle, args.package or ROOT / evidence["path"], evidence)
    if args.final_inputs:
        result["final_input_readiness"] = final_input_readiness(args.final_inputs)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
