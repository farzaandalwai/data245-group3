"""Opt-in real artifact reproduction; no learned models or final predictions/scoring."""
import hashlib
import io
import json
from pathlib import Path
import time

import pandas as pd

from scripts.delta_v2 import ROOT
from src.data_preprocessing_DELTA.v2 import REQUIRED, SERIES, validate_records, select_sample, subset
from src.features_DELTA.v2 import build_features, reconstruct
from src.features_DELTA.bundle import load_bundle, sha256
from src.models.baselines_DELTA.v2 import predictions, metrics


def _progress(message, started):
    print(f"[verify_delta_v2 +{time.perf_counter() - started:7.1f}s] {message}", flush=True)


def _frame_sha256(frame):
    """Hash the exact CSV bytes emitted by the bundle writer without filesystem I/O."""
    buffer = io.StringIO()
    frame.to_csv(buffer, index=False, float_format="%.17g", lineterminator="\n")
    return hashlib.sha256(buffer.getvalue().encode("utf-8")).hexdigest()


def main():
    started = time.perf_counter()
    evidence=json.loads((ROOT/"docs/DELTA_V2_RUN_EVIDENCE.json").read_text())
    source=ROOT/"data/raw/freshretail.csv"
    _progress("hashing raw source", started)
    if sha256(source)!=evidence["raw_sha256"]:
        raise ValueError("Source identity changed")
    _progress("reading and validating raw source", started)
    raw=validate_records(pd.read_csv(source,usecols=REQUIRED))
    _progress(f"validated {len(raw)} raw rows", started)
    reproduced=0
    for name,record in evidence["bundles"].items():
        _progress(f"loading bundle {name}", started)
        path=ROOT/record["path"]
        tables,manifest=load_bundle(path,record["manifest_sha256"])
        if record["purpose"]=="synthetic_test_only":
            _progress(f"skipping synthetic bundle {name} after manifest validation", started)
            continue
        _progress(f"checking sample selection for {name}", started)
        selected=pd.read_csv(path/"sample_manifest.csv")
        if record["purpose"]=="final_experiment":
            pd.testing.assert_frame_equal(selected,select_sample(raw,1000,245))
        else:
            pd.testing.assert_frame_equal(selected,pd.read_csv(ROOT/"data/manifests/pilot_series_manifest.csv"))
        source_rows=subset(raw,selected)
        if record["purpose"]=="development_debugging":
            pilot=validate_records(pd.read_csv(ROOT/"data/processed/pilot_200_series.csv",usecols=REQUIRED))
            pd.testing.assert_frame_equal(pilot,source_rows,check_exact=False,rtol=1e-12,atol=1e-12)
            source_rows=pilot
        _progress(f"rebuilding features for {name} ({len(source_rows)} rows)", started)
        rebuilt=build_features(source_rows)
        reconstruct(source_rows,rebuilt)
        for table_name,frame in rebuilt.items():
            _progress(f"hashing rebuilt {name}/{table_name}", started)
            if _frame_sha256(frame)!=sha256(path/f"{table_name}.csv"):
                raise ValueError(f"Reproduction mismatch: {name}/{table_name}.csv")
            reproduced+=1
        for relative,digest in manifest["source_files_sha256"].items():
            _progress(f"checking source snapshot for {name}", started)
            if sha256(ROOT/evidence["source_snapshot"]/relative)!=digest:
                raise ValueError("Immutable source snapshot mismatch")
    development=ROOT/evidence["bundles"]["v2-development-200-r2"]["path"]
    _progress("reproducing development baselines", started)
    tables,_=load_bundle(development)
    predicted=predictions(tables,"v2-development-baselines-r2")
    for name,frame in (("predictions.csv",predicted),("metrics.csv",metrics(predicted))):
        if _frame_sha256(frame)!=evidence["baseline_run"]["files"][name]["sha256"]:
            raise ValueError(f"Development baseline reproduction mismatch: {name}")
    _progress(f"PASS: {reproduced} real CSV byte hashes and two development baseline CSV byte hashes", started)
    print("No final predictions or metrics computed; temporary reproduction files removed.")


if __name__=="__main__":
    main()
