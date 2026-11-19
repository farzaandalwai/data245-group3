"""Common reference forecasts from accepted V2 inputs; no learned models."""
from pathlib import Path
import numpy as np
import pandas as pd

from src.features_DELTA.bundle import load_bundle, sha256, write_csv, write_json
from src.data_preprocessing_DELTA.v2 import KEY


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


def run_development(bundle, destination, run_id):
    tables,manifest=load_bundle(bundle)
    if manifest["purpose"]!="development_debugging":
        raise ValueError("Final test scoring is blocked; only development baselines supported")
    destination=Path(destination)
    if destination.exists():
        raise FileExistsError("Immutable baseline run already exists")
    predicted=predictions(tables,run_id)
    destination.mkdir(parents=True)
    write_csv(destination/"predictions.csv",predicted)
    write_csv(destination/"metrics.csv",metrics(predicted))
    write_json(destination/"run_manifest.json",{"protocol_version":"2.0","purpose":manifest["purpose"],"run_id":run_id,
               "bundle_manifest_sha256":sha256(Path(bundle)/"bundle_manifest.json"),"models":["persistence","recent_avg_7"],
               "artifacts":{name:sha256(destination/name) for name in ("predictions.csv","metrics.csv")},
               "test_exposure":"development historical holdout previously examined; no adaptive selection"})
