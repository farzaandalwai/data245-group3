"""Immutable bundle serialization and lightweight consumer validation."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import shutil

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY, SERIES, CALENDAR
from src.features_DELTA.v2 import COMMON, EXTRA


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n", encoding="utf-8", newline="\n")


def write_csv(path, frame):
    frame.to_csv(path, index=False, float_format="%.17g", lineterminator="\n")


def spec():
    definitions = {}
    for name in COMMON + EXTRA:
        if "lag" in name:
            timing = f"t-{name.rsplit('_',1)[1]}"
        elif "mean" in name or "fraction" in name:
            timing = f"t-{name.rsplit('_',1)[1]} through t-1 inclusive"
        else:
            timing = "known target calendar date"
        unit = "normalized recorded sales" if name.startswith("sales") else "stockout hours [6,22)" if "hours" in name else "fraction of prior days with positive count" if "fraction" in name else "Monday=0 through Sunday=6" if name=="weekday" else "Saturday/Sunday=1; otherwise=0"
        definitions[name] = {"timing": timing, "units": unit, "dtype": "int64" if name in ("weekday","is_weekend") else "float64", "availability": "observed through t-1; calendar known at forecast time"}
    return {"sales_only": COMMON, "stockout_aware": COMMON+EXTRA, "definitions": definitions,
            "keys": KEY, "target": "actual", "preprocessing": "No imputation/scaling; consumer fits any transformations on train only"}


def validate_tables(tables, sample):
    schemas = {"observations": KEY+["actual","split"], "features_sales_only": KEY+COMMON,
               "features_stockout_aware": KEY+COMMON+EXTRA,
               "evaluation_metadata": KEY+["target_stockout_hours","target_stockout_group"]}
    obs = tables["observations"]
    if sample.duplicated(SERIES).any() or sample[SERIES].isna().any().any():
        raise ValueError("Invalid sample manifest")
    expected = pd.DataFrame([(int(s),int(p),dt.strftime("%Y-%m-%d")) for s,p in sample[SERIES].sort_values(SERIES).itertuples(index=False,name=None) for dt in CALENDAR[14:]],columns=KEY)
    for name, columns in schemas.items():
        table = tables[name]
        if list(table) != columns or table.isna().any().any() or table.duplicated(KEY).any():
            raise ValueError(f"Invalid schema/null/duplicate: {name}")
        pd.testing.assert_frame_equal(table[KEY],expected,check_dtype=False)
        numeric = [c for c in columns if c not in KEY+["split","target_stockout_group"]]
        if not np.isfinite(table[numeric].to_numpy()).all():
            raise ValueError(f"Nonfinite artifact: {name}")
    day = (pd.to_datetime(obs.dt)-CALENDAR[0]).dt.days+1
    expected_split = np.select([day<=60,day<=75],["train","validation"],default="test")
    if not np.array_equal(obs.split,expected_split) or obs.actual.lt(0).any():
        raise ValueError("Invalid target/split")
    pd.testing.assert_frame_equal(tables["features_sales_only"],tables["features_stockout_aware"][KEY+COMMON])
    meta = tables["evaluation_metadata"]
    h = meta.target_stockout_hours
    if not (h.between(0,16)&h.mod(1).eq(0)).all() or not np.array_equal(meta.target_stockout_group,np.where(h.eq(0),"fully_stocked","stockout")):
        raise ValueError("Invalid retrospective metadata")
    aware=tables["features_stockout_aware"]
    if (aware[COMMON+EXTRA]<0).any().any():
        raise ValueError("Negative predictors")
    if not np.array_equal(aware.weekday,pd.to_datetime(obs.dt).dt.day_of_week) or not np.array_equal(aware.is_weekend,aware.weekday.ge(5).astype(int)):
        raise ValueError("Invalid calendar predictors")
    for col in EXTRA:
        maximum=1 if "fraction" in col else 16
        if aware[col].gt(maximum+1e-12).any():
            raise ValueError("Invalid stockout predictor range")


def publish_bundle(destination, tables, sample, quality, provenance):
    destination=Path(destination)
    if destination.exists():
        raise FileExistsError(f"Immutable destination exists: {destination}")
    validate_tables(tables,sample)
    destination.parent.mkdir(parents=True,exist_ok=True)
    temporary=Path(tempfile.mkdtemp(prefix=".building-",dir=destination.parent))
    try:
        for name,table in {**tables,"sample_manifest":sample}.items():
            write_csv(temporary/f"{name}.csv",table)
        write_json(temporary/"quality_report.json",quality)
        write_json(temporary/"feature_spec.json",spec())
        write_json(temporary/"configuration_snapshot.json",provenance.pop("configuration_snapshot"))
        manifest={**provenance,"protocol_version":"2.0","producer_contract_version":"2.0.0",
                  "contract_status":"producer_verified_overall_contract_draft",
                  "validation_status":"VERIFIED_operational_PROVISIONAL_business_semantics",
                  "split_counts":{str(k):int(v) for k,v in tables["observations"].split.value_counts().items()},
                  "artifacts":{p.name:{"sha256":sha256(p),"bytes":p.stat().st_size} for p in sorted(temporary.iterdir())},
                  "sample_sha256":sha256(temporary/"sample_manifest.csv"),
                  "limitations":["Local export lineage and normalization coefficient unverified", "No independent missing/closed-hour business definition", "90-day completeness is retrospective selection", "Historical pilot test exposure; holdout not pristine", "Final test scoring blocked pending joint freeze"]}
        write_json(temporary/"bundle_manifest.json",manifest)
        load_bundle(temporary)
        os.rename(temporary,destination)
    except BaseException:
        shutil.rmtree(temporary)
        raise
    return manifest


def load_bundle(path, expected_manifest_sha256=None):
    """Hash/schema/coverage validation; no raw-data dependency. Pin manifest hash for trust."""
    path=Path(path)
    if expected_manifest_sha256 and sha256(path/"bundle_manifest.json")!=expected_manifest_sha256:
        raise ValueError("Bundle manifest identity mismatch")
    manifest=json.loads((path/"bundle_manifest.json").read_text())
    if manifest["protocol_version"]!="2.0" or manifest["producer_contract_version"]!="2.0.0":
        raise ValueError("Unsupported bundle contract")
    required={"observations.csv","features_sales_only.csv","features_stockout_aware.csv","evaluation_metadata.csv","sample_manifest.csv","eligibility_audit.csv","quality_report.json","feature_spec.json","configuration_snapshot.json"}
    if set(manifest["artifacts"])!=required:
        raise ValueError("Artifact inventory mismatch")
    for name,record in manifest["artifacts"].items():
        if Path(name).name!=name or sha256(path/name)!=record["sha256"] or (path/name).stat().st_size!=record["bytes"]:
            raise ValueError(f"Artifact integrity mismatch: {name}")
    if manifest["sample_sha256"]!=sha256(path/"sample_manifest.csv"):
        raise ValueError("Sample identity mismatch")
    if json.loads((path/"feature_spec.json").read_text())!=spec():
        raise ValueError("Unexpected predictor specification")
    tables={name:pd.read_csv(path/f"{name}.csv",converters={name: float for name in ["actual", *COMMON, *EXTRA] if name not in ("weekday", "is_weekend")}) for name in ("observations","features_sales_only","features_stockout_aware","evaluation_metadata")}
    sample=pd.read_csv(path/"sample_manifest.csv")
    validate_tables(tables,sample)
    if tables["observations"].split.value_counts().to_dict()!=manifest["split_counts"]:
        raise ValueError("Split count manifest mismatch")
    return tables,manifest
