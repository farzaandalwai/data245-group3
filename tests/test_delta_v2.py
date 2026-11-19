"""Behavioral V2 guards: small independent golden cases and temporal perturbations."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from scripts.delta_v2 import fixture
from src.data_preprocessing_DELTA.v2 import validate_records, complete_series, select_sample, subset, KEY, SERIES
from src.features_DELTA.v2 import build_features, reconstruct, COMMON, EXTRA
from src.features_DELTA.bundle import publish_bundle, load_bundle, sha256, validate_tables
from src.models.baselines_DELTA.v2 import predictions, metrics, run_development


class DeltaV2Tests(unittest.TestCase):
    def setUp(self):
        self.raw=fixture()
        self.frame=validate_records(self.raw)
        self.tables=build_features(self.frame)

    def test_required_fields(self):
        for col in self.raw:
            with self.subTest(col=col),self.assertRaises(ValueError):
                validate_records(self.raw.drop(columns=col))

    def test_null_fields(self):
        for col in self.raw:
            f=self.raw.copy().astype({col:object}); f.loc[0,col]=None
            with self.subTest(col=col),self.assertRaises(ValueError): validate_records(f)

    def test_bad_keys_and_dates(self):
        for col,value in [("store_id",-1),("product_id",1.5),("store_id",True),("dt","2024-03-27"),("dt","2024-03-28 12:00"),("dt","nonsense")]:
            f=self.raw.copy().astype({col:object});f.loc[0,col]=value
            with self.subTest(col=col,value=value),self.assertRaises(ValueError):validate_records(f)

    def test_duplicate_records(self):
        with self.assertRaises(ValueError):validate_records(pd.concat([self.raw,self.raw.iloc[:1]]))

    def test_incomplete_is_separate_from_invalid(self):
        f=validate_records(self.raw.drop(index=3))
        eligible,excluded=complete_series(f)
        self.assertEqual((len(eligible),len(excluded),excluded.iloc[0].missing_days),(1,1,1))
        with self.assertRaises(ValueError):subset(f,self.frame[SERIES].drop_duplicates())
        with self.assertRaises(ValueError):build_features(f)

    def test_numeric_bounds_and_finiteness(self):
        for col,values in [("sale_amount",[-1,np.inf,-np.inf,np.nan]),("stock_hour6_22_cnt",[-1,17,.5,np.inf]),("store_id",[np.inf,2**64])]:
            for value in values:
                f=self.raw.copy().astype({col:object});f.loc[0,col]=value
                with self.subTest(col=col,value=value),self.assertRaises(ValueError):validate_records(f)

    def test_hourly_parser_and_endpoints(self):
        for value in ["[0 1]","["+" ".join(["2"]*24)+"]","__import__('os')", "["+" ".join(["nan"]*24)+"]"]:
            f=self.raw.copy();f.loc[0,"hours_stock_status"]=value
            with self.assertRaises(ValueError):validate_records(f)
        f=self.raw.copy();vector=[0]*24
        for hour in (5,6,21,22):vector[hour]=1
        f.loc[0,"hours_stock_status"]=str(vector);f.loc[0,"stock_hour6_22_cnt"]=2
        validate_records(f)
        f.loc[0,"stock_hour6_22_cnt"]=4
        with self.assertRaises(ValueError):validate_records(f)

    def test_sampling_determinism_order_and_outcome_independence(self):
        selected=select_sample(self.frame,1)
        pd.testing.assert_frame_equal(selected,select_sample(self.frame.sample(frac=1,random_state=7),1))
        changed=self.frame.copy();later=changed.dt>pd.Timestamp('2024-05-26')
        changed.loc[later,"sale_amount"]=9999
        changed.loc[later,"stock_hour6_22_cnt"]=16
        pd.testing.assert_frame_equal(selected,select_sample(changed,1))
        for count in (0,3,True):
            with self.assertRaises(ValueError):select_sample(self.frame,count)

    def test_golden_prior_features_and_series_isolation(self):
        first=self.tables["features_stockout_aware"].iloc[0]
        self.assertEqual(first[COMMON].tolist(),[113,112,111,107,100,110,106.5,3,0])
        self.assertEqual(first[EXTRA].tolist(),[0,2/7,5/14,2/7,5/14])
        second=self.tables["features_sales_only"].query('store_id == 2').iloc[0]
        self.assertEqual(second.sales_lag_14,200)
        self.assertEqual(reconstruct(self.frame,self.tables)["independent_predictor_values"],152*14)

    def test_day15_and_split_boundaries(self):
        obs=self.tables["observations"]
        self.assertEqual(obs.split.value_counts().to_dict(),{"train":92,"validation":30,"test":30})
        for dt,split in [("2024-04-11","train"),("2024-05-26","train"),("2024-05-27","validation"),("2024-06-10","validation"),("2024-06-11","test")]:
            self.assertEqual(set(obs.loc[obs.dt.eq(dt),"split"]),{split})

    def test_preserves_stockout_targets(self):
        self.assertEqual(len(self.tables["observations"]),152)
        self.assertGreater(self.tables["evaluation_metadata"].target_stockout_hours.gt(0).sum(),0)
        self.assertEqual(self.tables["eligibility_audit"].target_stockout_exclusions.sum(),0)

    def test_target_and_future_perturbations(self):
        changed=self.frame.copy();mask=(changed.store_id==1)&(changed.dt>=pd.Timestamp("2024-05-27"))
        changed.loc[mask,"sale_amount"]=9000;changed.loc[mask,"stock_hour6_22_cnt"]=16
        altered=build_features(changed)
        for name in ("features_sales_only","features_stockout_aware"):
            before=self.tables[name];after=altered[name]
            pd.testing.assert_frame_equal(before.loc[before.dt<="2024-05-27"],after.loc[after.dt<="2024-05-27"])
            pd.testing.assert_frame_equal(before.loc[before.store_id==2],after.loc[after.store_id==2])

    def test_allowlists_and_common_values(self):
        self.assertEqual(list(self.tables["features_sales_only"]),KEY+COMMON)
        self.assertEqual(list(self.tables["features_stockout_aware"]),KEY+COMMON+EXTRA)
        pd.testing.assert_frame_equal(self.tables["features_sales_only"],self.tables["features_stockout_aware"][KEY+COMMON])
        for name in ("features_sales_only","features_stockout_aware"):
            self.assertFalse(set(self.tables[name])&{"actual","split","target_stockout_hours","target_stockout_group"})

    def test_baseline_formulas_coverage_and_metrics(self):
        pred=predictions(self.tables,"test-only")
        self.assertEqual(len(pred),304)
        for model in ("persistence","recent_avg_7"):
            pd.testing.assert_frame_equal(pred.loc[pred.model.eq(model),KEY].reset_index(drop=True),self.tables["observations"][KEY])
        row=pred.iloc[0];self.assertEqual((row.actual,row.prediction),(114,113))
        self.assertEqual(pred.loc[pred.model.eq("recent_avg_7")].iloc[0].prediction,110)
        score=metrics(pred)
        self.assertTrue(score.loc[score.model.eq("persistence"),"MAE"].eq(1).all())
        self.assertTrue(score.loc[score.model.eq("recent_avg_7"),"signed_bias"].eq(-4).all())

    def publish(self,path,purpose="synthetic_test_only"):
        return publish_bundle(path,self.tables,self.frame[SERIES].drop_duplicates(),{"fixture":"test only"},
                              {"purpose":purpose,"source_sha256":"synthetic","configuration_snapshot":{"test_only":True}})

    def test_deterministic_artifacts_integrity_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"a";b=Path(d)/"b"
            self.publish(a);self.publish(b)
            self.assertEqual({p.name:sha256(p) for p in a.iterdir()},{p.name:sha256(p) for p in b.iterdir()})
            load_bundle(a,sha256(a/"bundle_manifest.json"))
            with self.assertRaises(FileExistsError):self.publish(a)
            with self.assertRaises(ValueError):load_bundle(a,"wrong")
            (a/"observations.csv").write_text("tamper")
            with self.assertRaises(ValueError):load_bundle(a)

    def test_reject_bad_contract_keys_targets_and_splits(self):
        sample=self.frame[SERIES].drop_duplicates()
        for table,column,value in [("observations","split","test"),("observations","actual",-1),("evaluation_metadata","target_stockout_group","wrong"),("features_sales_only","weekday",99)]:
            tables=copy.deepcopy(self.tables);tables[table].loc[0,column]=value
            with self.subTest(table=table,column=column),self.assertRaises((ValueError,AssertionError)):validate_tables(tables,sample)
        tables=copy.deepcopy(self.tables);tables["features_sales_only"]=tables["features_sales_only"].iloc[1:]
        with self.assertRaises(AssertionError):validate_tables(tables,sample)

    def test_final_and_development_separation_and_scoring_gate(self):
        with tempfile.TemporaryDirectory() as d:
            final=Path(d)/"final";dev=Path(d)/"dev"
            self.publish(final,"final_experiment");self.publish(dev,"development_debugging")
            self.assertNotEqual(sha256(final/"bundle_manifest.json"),sha256(dev/"bundle_manifest.json"))
            with self.assertRaises(ValueError):run_development(final,Path(d)/"blocked","blocked")
            self.assertFalse((Path(d)/"blocked").exists())
            run_development(dev,Path(d)/"run","fixture")
            self.assertTrue((Path(d)/"run/run_manifest.json").is_file())


if __name__=="__main__":unittest.main()
