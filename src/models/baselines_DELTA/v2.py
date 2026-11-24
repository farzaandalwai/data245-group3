"""Common reference forecasts from accepted V2 inputs; no learned models."""
from pathlib import Path
import numpy as np
import pandas as pd

from src.features_DELTA.bundle import load_bundle, sha256, write_csv, write_json
from src.data_preprocessing_DELTA.v2 import KEY
from src.data_preprocessing_DELTA.run_artifacts import (
    check_destination, checked_run_id, environment, inventory, new_run, source_snapshot,
)


def predictions(tables, run_id):
    obs=tables["observations"]
    features=tables["features_sales_only"]
    joined=obs.merge(features,on=KEY,validate="one_to_one")
    if len(joined)!=len(obs):
        raise ValueError("Baseline key coverage mismatch")
    outputs=[]
    for model,column in (("persistence","sales_lag_1"),("recent_avg_7","sales_mean_7")):
        out=joined[KEY+["actual","split"]].copy()
        out["prediction"]=joined[column]
        out["model"]=model
        out["feature_set"]="common_reference"
        out["run_id"]=run_id
        outputs.append(out[KEY+["actual","prediction","model","feature_set","split","run_id"]])
    return pd.concat(outputs,ignore_index=True)


def metrics(predicted):
    rows=[]
    for (model,split),group in predicted.groupby(["model","split"],sort=True):
        error=(group.prediction-group.actual).to_numpy()
        rows.append({"model":model,"split":split,"rows":len(group),"MAE":float(np.mean(abs(error))),
                     "RMSE":float(np.sqrt(np.mean(error**2))),"signed_bias":float(np.mean(error))})
    return pd.DataFrame(rows)


def run_development(bundle, destination, run_id, *, expected_manifest_sha256):
    checked_run_id(run_id)
    bundle=Path(bundle)
    destination=check_destination(destination,inputs=[bundle])
    if not expected_manifest_sha256 or sha256(bundle/"bundle_manifest.json")!=expected_manifest_sha256:
        raise ValueError("A matching trusted bundle manifest SHA-256 is required")
    # Reject final purpose before opening outcome CSVs.
    import json
    header=json.loads((bundle/"bundle_manifest.json").read_text())
    if header.get("purpose")!="development_debugging":
        raise ValueError("Final test scoring is blocked; only development baselines supported")
    tables,manifest=load_bundle(bundle,expected_manifest_sha256)
    keys=tables["observations"].loc[tables["observations"].split.isin(["train","validation"]),KEY]
    non_test={name:tables[name].merge(keys,on=KEY,validate="one_to_one")
              for name in ("observations","features_sales_only")}
    predicted=predictions(non_test,run_id)
    with new_run(destination,inputs=[bundle]) as temporary:
        write_csv(temporary/"predictions.csv",predicted)
        write_csv(temporary/"metrics.csv",metrics(predicted))
        write_json(temporary/"run_manifest.json",{
            "prediction_run_version":"2.0-development-1", "protocol_version":"2.0",
            "producer_contract_version":manifest["producer_contract_version"],
            "purpose":manifest["purpose"],"run_id":run_id,"owner":"DELTA",
            "bundle_manifest_sha256":sha256(bundle/"bundle_manifest.json"),
            "sample_sha256":manifest["sample_sha256"],"models":["persistence","recent_avg_7"],
            "scored_splits":["train","validation"],"test_scored":False,
            "evidence_status":"DEVELOPMENT_NOT_FINAL","group_validation_choices_frozen":False,
            "policy":{"preprocessing":"none","prediction_postprocessing":"none",
                      "predictors":{"persistence":"sales_lag_1","recent_avg_7":"sales_mean_7"}},
            "selected_parameters":{},"environment":environment(),
            "source":source_snapshot(["src/models/baselines_DELTA/v2.py",
                "src/data_preprocessing_DELTA/run_artifacts.py","src/features_DELTA/bundle.py",
                "src/features_DELTA/v2.py","scripts/delta_v2.py"]),
            "artifacts":inventory(temporary),
            "test_exposure":"Historical development holdout previously examined; no new test scoring"})
