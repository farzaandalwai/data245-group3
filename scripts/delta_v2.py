"""Explicit V2 producer CLI. Run from repository root: python -m scripts.delta_v2."""
import argparse
import csv
import json
import logging
from pathlib import Path
import platform
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yaml

from src.data_preprocessing_DELTA.v2 import REQUIRED, SERIES, validate_records, complete_series, select_sample, subset, coverage
from src.features_DELTA.v2 import build_features, reconstruct, COMMON, EXTRA
from src.features_DELTA.bundle import publish_bundle, load_bundle, sha256
from src.models.baselines_DELTA.v2 import run_development

ROOT=Path(__file__).resolve().parents[1]
LOG=logging.getLogger(__name__)


def configuration():
    configs={p.stem:yaml.safe_load(p.read_text()) for p in (ROOT/"configs").glob("*.yaml")}
    e=configs["experiments"]
    if e["sales_only_predictors"]!=COMMON or e["stockout_additional_predictors"]!=EXTRA or e["first_target_day"]!=15 or e["eligibility"]["exclude_solely_for_target_stockout"]:
        raise ValueError("Configuration contradicts implemented approved V2 contract")
    if [(e["splits"][s]["first_day"],e["splits"][s]["last_day"]) for s in ("train","validation","test")]!=[(1,60),(61,75),(76,90)]:
        raise ValueError("Unexpected split configuration")
    return configs


def source_identity():
    paths=[*sorted((ROOT/"src").rglob("v2.py")),ROOT/"src/features_DELTA/bundle.py",ROOT/"scripts/delta_v2.py",ROOT/"scripts/audit_contract.py"]
    return {str(p.relative_to(ROOT)).replace("\\","/"):sha256(p) for p in paths}


def fixture():
    rows=[]
    for store in (1,2):
        for i,dt in enumerate(pd.date_range("2024-03-28",periods=90)):
            hours=[0]*24
            hours[6]=int(i%3==0)
            rows.append([store,10,dt.strftime("%Y-%m-%d"),float(i+store*100),hours[6],"["+" ".join(map(str,hours))+"]"])
    return pd.DataFrame(rows,columns=REQUIRED)


def generate(purpose, bundle_id, configs):
    if not bundle_id or Path(bundle_id).name!=bundle_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in bundle_id):
        raise ValueError("Bundle ID must contain only letters, digits, hyphen, underscore")
    destination=ROOT/configs["experiments"]["feature_bundle_root"]/bundle_id
    if destination.exists():
        raise FileExistsError(f"Immutable destination exists: {destination}")
    if purpose=="synthetic_test_only":
        raw=validate_records(fixture())
        source_hash="synthetic_test_only"
        header=REQUIRED
    else:
        source=ROOT/configs["dataset"]["raw"]
        source_hash=sha256(source)
        if source_hash!=configs["dataset"]["source_sha256"]:
            raise ValueError("Raw export identity differs from registered source")
        with source.open(newline="",encoding="utf-8") as handle:
            header=next(csv.reader(handle))
        LOG.info("Reading and validating raw source once (%s)",source_hash)
        raw=validate_records(pd.read_csv(source,usecols=REQUIRED))
    eligible,excluded=complete_series(raw)
    source_report={"rows":len(raw),"columns":header,"series":len(eligible)+len(excluded),"complete_series":len(eligible),
                   "stores":int(raw.store_id.nunique()),"products":int(raw.product_id.nunique()),
                   "date_min":str(raw.dt.min().date()),"date_max":str(raw.dt.max().date()),
                   "invalid_records":0,"duplicate_keys":0,"hourly_count_mismatches":0,
                   "incomplete_series":excluded.to_dict(orient="records")}
    if purpose=="development_debugging":
        manifest_path=ROOT/configs["dataset"]["manifest"]
        sample=pd.read_csv(manifest_path)
        pilot_path=ROOT/configs["dataset"]["pilot"]
        selected=validate_records(pd.read_csv(pilot_path,usecols=REQUIRED))
        selected=subset(selected,sample)
        raw_selected=subset(raw,sample)
        pd.testing.assert_frame_equal(selected,raw_selected,check_exact=False,rtol=1e-12,atol=1e-12)
        if len(sample)!=configs["dataset"]["pilot_series"]:
            raise ValueError("Canonical pilot size changed")
        difference=(selected.sale_amount-raw_selected.sale_amount).abs()
        sample_origin={"canonical_manifest_sha256":sha256(manifest_path),"canonical_pilot_sha256":sha256(pilot_path),
                       "pilot_raw_sales_different_float_values":int(difference.gt(0).sum()),
                       "pilot_raw_max_absolute_difference":float(difference.max()),
                       "pilot_raw_comparison_tolerance":{"rtol":1e-12,"atol":1e-12},
                       "development_values":"canonical pilot retained; legacy serialization has sub-ULP-scale differences from raw"}
    else:
        count=2 if purpose=="synthetic_test_only" else configs["dataset"]["final_sample"]["series"]
        sample=select_sample(raw,count,configs["dataset"]["seed"])
        selected=subset(raw,sample)
        sample_origin={"selection_algorithm":"SHA256 rank of ASCII v2|seed|integer_store|integer_product; ascending digest then keys; first n; output sorted keys",
                       "seed":configs["dataset"]["seed"],"selection_uses_outcomes":False}
    LOG.info("Building %s: %s selected series",purpose,len(sample))
    tables=build_features(selected)
    quality={"source":source_report,"coverage":coverage(selected,len(eligible)),
             "population_coverage":coverage(raw.merge(eligible,on=SERIES,validate="many_to_one"),len(eligible)),
             "validation":reconstruct(selected,tables),"quality_exclusions_selected":0,
             "stockout_interpretation":"Operationally verified: 24 binary entries, 1=stockout, indices [6:22]; full export reconciled",
             "business_semantics":"PROVISIONAL: missing/closed hours not independently documented; fully_stocked means zero annotated stockout in interval only"}
    provenance={"bundle_id":bundle_id,"purpose":purpose,"source_sha256":source_hash,
                "source_bytes":None if purpose=="synthetic_test_only" else source.stat().st_size,
                "sample_origin":sample_origin,"configuration_snapshot":configs,
                "source_revision":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
                "source_files_sha256":source_identity(),"owner":"DELTA","generated_date":datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat(),
                "environment":{"python":platform.python_version(),"pandas":pd.__version__,"numpy":np.__version__,"PyYAML":yaml.__version__}}
    publish_bundle(destination,tables,sample,quality,provenance)
    LOG.info("Published %s; split counts %s",destination,tables["observations"].split.value_counts().to_dict())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    build=sub.add_parser("build")
    build.add_argument("--purpose",choices=["development_debugging","final_experiment","synthetic_test_only"],required=True)
    build.add_argument("--bundle-id",required=True)
    verify=sub.add_parser("verify")
    verify.add_argument("bundle")
    verify.add_argument("--manifest-sha256")
    baseline=sub.add_parser("baselines")
    baseline.add_argument("bundle")
    baseline.add_argument("--run-id",required=True)
    baseline.add_argument("--manifest-sha256",required=True,
                          help="Trusted development bundle manifest SHA-256 from DELTA evidence")
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format="%(levelname)s: %(message)s")
    if args.command=="build":
        generate(args.purpose,args.bundle_id,configuration())
    elif args.command=="verify":
        _,manifest=load_bundle(ROOT/args.bundle,args.manifest_sha256)
        LOG.info("Verified %s: %s",manifest["purpose"],manifest["split_counts"])
    else:
        if not args.run_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in args.run_id):
            raise ValueError("Invalid run ID")
        run_development(ROOT/args.bundle,ROOT/"results/baselines_DELTA/v2"/args.run_id,args.run_id,
                        expected_manifest_sha256=args.manifest_sha256)
        LOG.info("Development baselines saved: %s",args.run_id)


if __name__=="__main__":
    main()
