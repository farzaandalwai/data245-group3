"""Reviewed final evaluator on synthetic fixtures only; never opens a real final bundle."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY, SERIES
from src.evaluation_SAS.bootstrap import paired_store_intervals, pooled_store_interval_rows
from src.evaluation_SAS.final import (
    FINAL_LIMITATIONS, fit_predict, inspect_final_readiness, run_final, validate_settings,
)
from src.evaluation_SAS.runs import ROOT, read_json
from src.features_DELTA.bundle import publish_bundle, sha256, write_json
from tests.test_sas_v2 import shared_tables

APPROVALS = [{"codename": c, "github": g, "date": "2099-01-01"}
             for c, g in (("DELTA", "fixture-delta"), ("DEVGRU", "fixture-devgru"), ("SAS", "fixture-sas"))]


def fixture_settings(digest, *, forest=False):
    settings = read_json(ROOT / "configs/final_settings.json")
    settings.update(status="APPROVED", approved=True, approvals=copy.deepcopy(APPROVALS),
                    freeze_record="fixture-freeze-record-not-real")
    settings["final_bundle"] = {"bundle_id": "synthetic-final-fixture", "manifest_sha256": digest}
    settings["models"]["random_forest"].update(enabled=forest, n_estimators=5)
    return settings


class FinalEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "configs").mkdir()
        self.tables = shared_tables()
        sample = self.tables["observations"][SERIES].drop_duplicates().reset_index(drop=True)
        self.bundle = self.root / "synthetic-final-bundle"
        publish_bundle(self.bundle, self.tables, sample, {},
                       {"purpose": "final_experiment", "configuration_snapshot": {}})
        self.digest = sha256(self.bundle / "bundle_manifest.json")
        self.open_gates()
        self.write_settings(fixture_settings(self.digest))

    def open_gates(self, value=True):
        (self.root / "configs/contract.yaml").write_text(json.dumps(dict.fromkeys(
            ["contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed"], value)))

    def write_settings(self, settings):
        write_json(self.root / "configs/final_settings.json", settings)

    def run_fixture(self, name="final-out", run_id="synthetic-final"):
        return run_final(self.bundle, self.root / name, run_id, root=self.root)

    def assert_blocked_before_loading(self, fragment):
        with patch("src.evaluation_SAS.final.load_bundle", side_effect=AssertionError("must not load")) as loader:
            with self.assertRaises(RuntimeError) as caught:
                self.run_fixture()
            loader.assert_not_called()
        self.assertIn(fragment, str(caught.exception))
        self.assertFalse((self.root / "final-out").exists())

    def test_repository_gates_and_settings_block_final_scoring(self):
        shutil.copy(ROOT / "configs/contract.yaml", self.root / "configs/contract.yaml")
        shutil.copy(ROOT / "configs/final_settings.json", self.root / "configs/final_settings.json")
        result = inspect_final_readiness(self.root, bundle=self.bundle)
        self.assertFalse(result["ready_for_final_scoring"])
        self.assertFalse(result["final_data_opened"])
        self.assert_blocked_before_loading("final_settings_not_jointly_approved")

    def test_closed_contract_flag_blocks_before_loading(self):
        self.open_gates(False)
        self.assert_blocked_before_loading("contract_frozen")

    def test_missing_approver_or_freeze_record_blocks(self):
        settings = fixture_settings(self.digest)
        settings["approvals"] = settings["approvals"][:2]
        self.write_settings(settings)
        self.assert_blocked_before_loading("missing_recorded_approvals_from_SAS")
        settings = fixture_settings(self.digest)
        settings["freeze_record"] = None
        self.write_settings(settings)
        self.assert_blocked_before_loading("missing_freeze_record")

    def test_bundle_hash_and_purpose_must_match(self):
        self.write_settings(fixture_settings("0" * 64))
        self.assert_blocked_before_loading("bundle_manifest_hash_differs_from_frozen_settings")
        manifest = read_json(self.bundle / "bundle_manifest.json")
        manifest["purpose"] = "development_debugging"
        write_json(self.bundle / "bundle_manifest.json", manifest)
        self.write_settings(fixture_settings(sha256(self.bundle / "bundle_manifest.json")))
        self.assert_blocked_before_loading("bundle_purpose_is_not_final_experiment")

    def test_settings_schema_rejects_protocol_changes(self):
        base = fixture_settings(self.digest)
        changes = [("prediction_postprocessing", "clip_nonnegative"), ("fit_split", "train_validation"),
                   ("selection", "tune_on_test"), ("baselines", ["persistence"])]
        for name, value in changes:
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_settings(dict(copy.deepcopy(base), **{name: value}))
        for mutate in (lambda s: s["uncertainty"].update(weighting="store_mean"),
                       lambda s: s["uncertainty"].update(seed=1),
                       lambda s: s["models"]["decision_tree"].update(enabled=False),
                       lambda s: s["models"]["random_forest"].update(max_features=0.5),
                       lambda s: s["models"]["ridge_regression"]["alpha"].update(sales_only=0),
                       lambda s: s["models"].pop("random_forest")):
            settings = copy.deepcopy(base)
            mutate(settings)
            with self.assertRaises(ValueError):
                validate_settings(settings)

    def test_end_to_end_synthetic_run_outputs_and_immutability(self):
        manifest = self.run_fixture()
        out = self.root / "final-out"
        self.assertEqual(manifest["models"], ["linear_regression", "ridge_regression", "decision_tree",
                                              "persistence", "recent_avg_7"])
        self.assertEqual(manifest["fit_split"], "train")
        self.assertEqual(manifest["settings_sha256"], sha256(self.root / "configs/final_settings.json"))
        for name, record in manifest["artifacts"].items():
            self.assertEqual(sha256(out / name), record["sha256"])
        predictions = pd.read_csv(out / "predictions.csv")
        observations = self.tables["observations"]
        self.assertEqual(len(predictions), len(observations) * 8)
        self.assertEqual(set(predictions.split), {"train", "validation", "test"})
        overall = pd.read_csv(out / "overall.csv")
        self.assertEqual(set(overall.split), {"validation", "test"})
        intervals = pd.read_csv(out / "mae_difference_intervals.csv")
        self.assertEqual(len(intervals), 6)
        self.assertTrue(intervals.replicates.eq(2000).all())
        paired = pd.read_csv(out / "paired_comparisons.csv")
        row = paired.iloc[0]
        self.assertAlmostEqual(row.relative_MAE_improvement_pct,
                               100 * (row.MAE_sales_only - row.MAE_stockout_aware) / row.MAE_sales_only)
        with self.assertRaises(FileExistsError):
            self.run_fixture()

    def test_optional_random_forest_is_included_only_when_enabled(self):
        self.write_settings(fixture_settings(self.digest, forest=True))
        manifest = self.run_fixture()
        self.assertIn("random_forest", manifest["models"])
        predictions = pd.read_csv(self.root / "final-out" / "predictions.csv")
        self.assertEqual(set(predictions.loc[predictions.model.eq("random_forest"), "feature_set"]),
                         {"sales_only", "stockout_aware"})

    def test_test_outcomes_and_test_features_never_affect_fitting(self):
        settings = fixture_settings(self.digest, forest=True)
        first = fit_predict(self.tables, settings, "fixture")
        altered = copy.deepcopy(self.tables)
        test = altered["observations"].split.eq("test")
        altered["observations"].loc[test, "actual"] = 1e6
        second = fit_predict(altered, settings, "fixture")
        non_test = first.split.ne("test")
        pd.testing.assert_frame_equal(first.loc[non_test].reset_index(drop=True),
                                      second.loc[non_test].reset_index(drop=True))
        np.testing.assert_array_equal(first.prediction.to_numpy(), second.prediction.to_numpy())

    def test_pooled_row_weighting_matches_development_bootstrap_not_store_means(self):
        predictions = fit_predict(self.tables, fixture_settings(self.digest), "fixture")
        validation = predictions.loc[predictions.split.eq("validation")]
        # Unequal store sizes: drop one store's later rows from every model/condition.
        store = validation.store_id.min()
        drop_dates = sorted(validation.loc[validation.store_id.eq(store), "dt"].unique())[:5]
        uneven = validation.loc[~(validation.store_id.eq(store) & validation.dt.isin(drop_dates))].copy()
        # Make the smaller store's aware forecasts clearly worse so store weighting matters.
        worse = uneven.store_id.eq(store) & uneven.feature_set.eq("stockout_aware")
        uneven.loc[worse, "prediction"] += 1.0
        final = pooled_store_interval_rows(uneven, ["linear_regression"], ["validation"], FINAL_LIMITATIONS)
        observations = self.tables["observations"]
        kept = uneven[KEY].drop_duplicates()
        development = paired_store_intervals(
            uneven.loc[uneven.model.eq("linear_regression")],
            observations.merge(kept, on=KEY).loc[lambda f: f.split.eq("validation")].reset_index(drop=True),
            purpose="synthetic_test_only", models=["linear_regression"])
        for column in ("MAE_difference", "ci_lower", "ci_upper", "n_observations", "n_stores"):
            self.assertEqual(final[column].iloc[0], development[column].iloc[0])
        part = uneven.loc[uneven.model.eq("linear_regression")]
        sales = part.loc[part.feature_set.eq("sales_only")].sort_values(KEY).reset_index(drop=True)
        aware = part.loc[part.feature_set.eq("stockout_aware")].sort_values(KEY).reset_index(drop=True)
        difference = (aware.prediction - aware.actual).abs() - (sales.prediction - sales.actual).abs()
        self.assertAlmostEqual(final.MAE_difference.iloc[0], difference.mean())
        store_mean = difference.groupby(sales.store_id).mean().mean()
        self.assertNotAlmostEqual(final.MAE_difference.iloc[0], store_mean)

    def test_failed_write_publishes_nothing(self):
        with patch("src.evaluation_SAS.final.write_json", side_effect=RuntimeError("fixture failure")):
            with self.assertRaises(RuntimeError):
                self.run_fixture()
        self.assertFalse((self.root / "final-out").exists())
        self.assertFalse(list(self.root.glob(".sas-building-*")))


class EvidencePreservationTests(unittest.TestCase):
    def test_legacy_final_evaluator_is_unchanged_and_not_the_entry_point(self):
        original = subprocess.run(["git", "show", "91fab8d:scripts/final_evaluation.py"], cwd=ROOT,
                                  capture_output=True, check=False)
        if original.returncode != 0:
            self.skipTest("Commit 91fab8d unavailable in this clone")
        current = (ROOT / "scripts/final_evaluation.py").read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(hashlib.sha256(current).hexdigest(),
                         hashlib.sha256(original.stdout.replace(b"\r\n", b"\n")).hexdigest())
        preflight = (ROOT / "scripts/sas_final_preflight.py").read_text()
        self.assertIn('"scripts/sas_final_evaluation.py"', preflight)


if __name__ == "__main__":
    unittest.main()
