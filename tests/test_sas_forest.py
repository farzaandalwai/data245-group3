"""SAS Random Forest behavior on deterministic synthetic fixtures only."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from scripts.delta_v2 import fixture
from src.data_preprocessing_DELTA.v2 import SERIES, validate_records
from src.evaluation_SAS.runs import (
    ROOT, evaluate_runs, load_prediction_run, pinned_bundle, read_json, train_forest_run,
)
from src.evaluation_SAS.v2 import CONDITIONS
from src.features_DELTA.bundle import publish_bundle, sha256, write_json
from src.features_DELTA.v2 import COMMON, EXTRA, build_features
from src.models.random_forest_SAS.v2 import fit_development, validate_policy

POLICY_PATH = ROOT / "src/models/random_forest_SAS/development_policy.json"


def small_policy():
    policy = read_json(POLICY_PATH)
    policy.update(n_estimators=5, max_depth=[1, 3], min_samples_leaf=[2, 10])
    return policy


def tables_fixture():
    return build_features(validate_records(fixture()))


class ForestTests(unittest.TestCase):
    def setUp(self):
        self.tables, self.policy = tables_fixture(), small_policy()

    def fit(self, tables=None, purpose="synthetic_test_only"):
        return fit_development(self.tables if tables is None else tables, self.policy,
                               purpose=purpose, run_id="forest-fixture")

    def test_fit_rows_allowlists_equal_budgets_and_no_test_access(self):
        expected_y = self.tables["observations"].query('split == "train"').actual.to_numpy()
        fits, predicted_indices = [], []

        class Tracking(RandomForestRegressor):
            def fit(estimator, x, y, **kwargs):
                fits.append(list(x.columns))
                np.testing.assert_array_equal(y, expected_y)
                return super().fit(x, y, **kwargs)

            def predict(estimator, x, **kwargs):
                predicted_indices.extend(x.index.tolist())
                return super().predict(x, **kwargs)

        with patch("src.models.random_forest_SAS.v2.RandomForestRegressor", Tracking):
            predicted, selection, _ = self.fit()
        self.assertEqual((len(fits), fits.count(COMMON), fits.count(COMMON + EXTRA)), (8, 4, 4))
        test_indices = set(self.tables["observations"].query('split == "test"').index)
        self.assertFalse(test_indices.intersection(predicted_indices))
        self.assertEqual(set(predicted.split), {"train", "validation"})
        self.assertEqual(set(predicted.model), {"random_forest"})
        self.assertEqual(len(predicted), 244)
        self.assertFalse(selection["refit_on_validation"])
        self.assertEqual(selection["candidates_per_condition"], 4)

    def test_test_and_retrospective_metadata_perturbation_changes_nothing(self):
        predicted, selection, _ = self.fit()
        altered = copy.deepcopy(self.tables)
        test = altered["observations"].split.eq("test")
        altered["observations"].loc[test, "actual"] = 1e9
        for name in ("features_sales_only", "features_stockout_aware"):
            altered[name].loc[test, COMMON[:-2]] = 1e8
        altered["evaluation_metadata"]["target_stockout_hours"] = 16
        altered["evaluation_metadata"]["target_stockout_group"] = "stockout"
        other, other_selection, _ = self.fit(altered)
        pd.testing.assert_frame_equal(predicted, other)
        self.assertEqual(selection, other_selection)

    def test_reproducibility_and_stable_tie_break(self):
        first, selection, _ = self.fit()
        second, other, _ = self.fit()
        pd.testing.assert_frame_equal(first, second)
        self.assertEqual(selection, other)
        raw = fixture()
        raw["sale_amount"] = 1.
        _, tied, _ = self.fit(build_features(validate_records(raw)))
        for parameters in tied["selected_parameters"].values():
            self.assertEqual((parameters["max_depth"], parameters["min_samples_leaf"]), (1, 2))

    def test_policy_and_final_inputs_fail_closed(self):
        for name, value in [("max_depth", [True]), ("min_samples_leaf", [0]), ("max_depth", [1, 1]),
                            ("random_state", True), ("n_estimators", 0), ("n_estimators", 5.0),
                            ("max_features", 0.5), ("bootstrap", 1),
                            ("prediction_postprocessing", "clip_nonnegative")]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_policy(dict(self.policy, **{name: value}))
        with self.assertRaises(ValueError):
            validate_policy({k: v for k, v in self.policy.items() if k != "n_estimators"})
        with self.assertRaises(ValueError):
            self.fit(purpose="final_experiment")

    def test_shipped_policy_is_valid_and_matches_tree_budget(self):
        policy = read_json(POLICY_PATH)
        validate_policy(policy)
        tree = read_json(ROOT / "src/models/decision_tree_SAS/development_policy.json")
        self.assertEqual((policy["max_depth"], policy["min_samples_leaf"], policy["random_state"]),
                         (tree["max_depth"], tree["min_samples_leaf"], tree["random_state"]))


class ForestRunTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.tables = tables_fixture()
        self.bundle = self.root / "bundle"
        sample = self.tables["observations"][SERIES].drop_duplicates().reset_index(drop=True)
        publish_bundle(self.bundle, self.tables, sample, {},
                       {"purpose": "synthetic_test_only", "configuration_snapshot": {}})
        self.digest = sha256(self.bundle / "bundle_manifest.json")
        self.identity = pinned_bundle(self.bundle, self.digest)[2]
        self.policy_path = self.root / "policy.json"
        write_json(self.policy_path, small_policy())

    def test_roundtrip_run_and_validation_only_comparison(self):
        destination = self.root / "forest-run"
        manifest = train_forest_run(self.bundle, self.digest, destination, "forest-fixture", self.policy_path)
        self.assertEqual(manifest["evidence_status"], "SYNTHETIC_NOT_RESEARCH")
        self.assertFalse(manifest["test_scored"])
        self.assertEqual(manifest["models"], ["random_forest"])
        load_prediction_run(destination, self.identity, self.tables["observations"])
        comparison = self.root / "comparison"
        result = evaluate_runs(self.bundle, self.digest, [destination], comparison,
                               "forest-comparison", ["random_forest"])
        self.assertEqual(result["scored_splits"], ["validation"])
        overall = pd.read_csv(comparison / "overall.csv")
        self.assertEqual(set(overall.feature_set), set(CONDITIONS))
        self.assertTrue(overall.n_observations.eq(30).all())
        with self.assertRaises(FileExistsError):
            train_forest_run(self.bundle, self.digest, destination, "forest-fixture", self.policy_path)

    def test_final_bundle_rejected_before_any_output(self):
        path = self.bundle / "bundle_manifest.json"
        manifest = read_json(path)
        manifest["purpose"] = "final_experiment"
        write_json(path, manifest)
        with self.assertRaises(ValueError):
            train_forest_run(self.bundle, sha256(path), self.root / "blocked", "blocked", self.policy_path)
        self.assertFalse((self.root / "blocked").exists())


if __name__ == "__main__":
    unittest.main()
