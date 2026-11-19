"""Opt-in real artifact reproduction; no learned models or final predictions/scoring."""
import json
from pathlib import Path
import tempfile

import pandas as pd

from scripts.delta_v2 import ROOT
from src.data_preprocessing_DELTA.v2 import REQUIRED, SERIES, validate_records, select_sample, subset
from src.features_DELTA.v2 import build_features, reconstruct
from src.features_DELTA.bundle import load_bundle, sha256, write_csv
from src.models.baselines_DELTA.v2 import predictions, metrics


def main():
    evidence=json.loads((ROOT/"docs/DELTA_V2_RUN_EVIDENCE.json").read_text())
    source=ROOT/"data/raw/freshretail.csv"
    if sha256(source)!=evidence["raw_sha256"]:
        raise ValueError("Source identity changed")
    raw=validate_records(pd.read_csv(source,usecols=REQUIRED))
    reproduced=0
    with tempfile.TemporaryDirectory() as temporary:
        for name,record in evidence["bundles"].items():
            path=ROOT/record["path"]
            tables,manifest=load_bundle(path,record["manifest_sha256"])
            if record["purpose"]=="synthetic_test_only":
                continue
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
            rebuilt=build_features(source_rows)
            reconstruct(source_rows,rebuilt)
            for table_name,frame in rebuilt.items():
                target=Path(temporary)/f"{table_name}.csv"
                write_csv(target,frame)
                if sha256(target)!=sha256(path/target.name):
                    raise ValueError(f"Reproduction mismatch: {name}/{target.name}")
                reproduced+=1
            for relative,digest in manifest["source_files_sha256"].items():
                if sha256(ROOT/evidence["source_snapshot"]/relative)!=digest:
                    raise ValueError("Immutable source snapshot mismatch")
        development=ROOT/evidence["bundles"]["v2-development-200-r2"]["path"]
        tables,_=load_bundle(development)
        predicted=predictions(tables,"v2-development-baselines-r2")
        for name,frame in (("predictions.csv",predicted),("metrics.csv",metrics(predicted))):
            target=Path(temporary)/name
            write_csv(target,frame)
            if sha256(target)!=evidence["baseline_run"]["files"][name]["sha256"]:
                raise ValueError(f"Development baseline reproduction mismatch: {name}")
    print(f"PASS: raw identity, three bundles, sample selection, {reproduced} real CSV byte hashes, source snapshots and two development baseline CSV byte hashes")
    print("No final predictions or metrics computed; temporary reproduction files removed.")


if __name__=="__main__":
    main()
