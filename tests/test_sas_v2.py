"""SAS behavior on deterministic fixtures only; no real forecasting findings."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

from scripts.delta_v2 import fixture
from src.data_preprocessing_DELTA.v2 import KEY, SERIES, validate_records
from src.evaluation_SAS.runs import (
    ROOT, evaluate_runs, load_prediction_run, new_run, pinned_bundle, read_json,
    train_tree_run,
)
from src.evaluation_SAS.v2 import (
    CONDITIONS, PREDICTION_COLUMNS, evaluate_predictions, regression_metrics,
    validate_predictions,
)
from src.evaluation_SAS.bootstrap import paired_store_intervals
from src.features_DELTA.bundle import publish_bundle, sha256, write_csv, write_json
from src.features_DELTA.v2 import COMMON, EXTRA, build_features
from src.models.baselines_DELTA.v2 import predictions as baseline_predictions
from src.models.decision_tree_SAS.v2 import fit_development, serialize_tree, validate_policy


POLICY_PATH = ROOT / "src/models/decision_tree_SAS/development_policy.json"


def small_policy():
    policy = read_json(POLICY_PATH)
    policy["max_depth"], policy["min_samples_leaf"] = [1, 3], [2, 10]
    return policy


def shared_tables():
    return build_features(validate_records(fixture()))


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.observations = pd.DataFrame({
            "store_id": [1, 1, 2], "product_id": [10, 10, 20],
            "dt": ["2024-05-27", "2024-05-28", "2024-05-27"],
            "actual": [0., 2., 4.], "split": ["validation"] * 3,
        })
        self.metadata = self.observations[KEY].copy()
        self.metadata["target_stockout_hours"] = [0, 2, 0]
        self.metadata["target_stockout_group"] = ["fully_stocked", "stockout", "fully_stocked"]
        conditions = []
        for condition, values in [("sales_only", [-1., 4., 3.]), ("stockout_aware", [0., 2., 4.])]:
            part = self.observations.copy()
            part["prediction"], part["model"] = values, "decision_tree"
            part["feature_set"], part["run_id"] = condition, "fixture-only"
            conditions.append(part[PREDICTION_COLUMNS])
        self.predictions = pd.concat(conditions, ignore_index=True)

    def evaluate(self, predictions=None, metadata=None, **kwargs):
        return evaluate_predictions(
            self.predictions if predictions is None else predictions, self.observations,
            self.metadata if metadata is None else metadata,
            purpose=kwargs.get("purpose", "synthetic_test_only"),
            models=kwargs.get("models", ["decision_tree"]), splits=kwargs.get("splits", ["validation"]))

    def test_golden_metrics_and_bias_denominators(self):
        score = regression_metrics([0, 2, 4], [-1, 4, 3])
        self.assertEqual(score["n_observations"], 3)
        self.assertAlmostEqual(score["MAE"], 4/3)
        self.assertAlmostEqual(score["RMSE"], np.sqrt(2))
        self.assertEqual(score["signed_bias"], 0)
        self.assertAlmostEqual(score["mean_underprediction"], 2/3)
        self.assertAlmostEqual(score["mean_overprediction"], 2/3)
        self.assertAlmostEqual(score["underprediction_rate"], 2/3)
        self.assertAlmostEqual(score["overprediction_rate"], 1/3)
        self.assertEqual(regression_metrics([0], [-1])["signed_bias"], -1)

    def test_metrics_reject_bad_inputs(self):
        for actual, prediction in [([1], [1, 2]), ([[1]], [[1]]), ([1], [np.nan]), ([np.inf], [1]), ([1e308], [-1e308])]:
            with self.subTest(actual=actual, prediction=prediction), self.assertRaises(ValueError):
                regression_metrics(actual, prediction)

    def test_paired_subgroups_and_series_store_summaries(self):
        report = self.evaluate()
        self.assertEqual(len(report["overall"]), 2)
        self.assertEqual(len(report["subgroups"]), 4)
        self.assertEqual(len(report["per_series"]), 4)
        self.assertEqual(len(report["per_store"]), 4)
        comparisons = report["paired_comparisons"]
        self.assertEqual(set(comparisons.target_stockout_group), {"all", "fully_stocked", "stockout"})
        self.assertTrue(comparisons.relative_MAE_improvement_percent.eq(100).all())
        self.assertEqual(report["coverage_audit"]["evidence_status"], "SYNTHETIC_NOT_RESEARCH")

    def test_row_order_is_irrelevant(self):
        expected = self.evaluate()
        actual = self.evaluate(self.predictions.sample(frac=1, random_state=8))
        pd.testing.assert_frame_equal(expected["overall"], actual["overall"])

    def test_empty_subgroups_and_zero_denominator_are_undefined(self):
        metadata = self.metadata.copy()
        metadata["target_stockout_hours"], metadata["target_stockout_group"] = 0, "fully_stocked"
        predictions = self.predictions.copy()
        predictions["prediction"] = predictions.actual
        report = self.evaluate(predictions, metadata)
        empty = report["subgroups"].query('target_stockout_group == "stockout"')
        self.assertTrue(empty.n_observations.eq(0).all())
        self.assertTrue(empty.MAE.isna().all())
        self.assertTrue(report["paired_comparisons"].relative_MAE_improvement_percent.isna().all())
        self.assertIsNone(regression_metrics([], [])["MAE"])

    def test_missing_extra_duplicate_and_jointly_dropped_keys_rejected(self):
        extra = self.predictions.iloc[:1].copy()
        extra["store_id"] = 999
        bad_frames = [self.predictions.iloc[1:], pd.concat([self.predictions, extra]),
                      pd.concat([self.predictions, self.predictions.iloc[:1]]),
                      self.predictions.loc[self.predictions.product_id.ne(20)]]
        for frame in bad_frames:
            with self.subTest(rows=len(frame)), self.assertRaises(ValueError):
                self.evaluate(frame)

    def test_actual_split_schema_and_condition_mismatches_rejected(self):
        cases = [("actual", np.nextafter(0., 1.)), ("split", "train"),
                 ("feature_set", "unapproved"), ("run_id", "another-run")]
        for name, value in cases:
            frame = self.predictions.copy()
            frame.loc[0, name] = value
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.evaluate(frame)
        for frame in [self.predictions.assign(extra=0), self.predictions.drop(columns="run_id"),
                      self.predictions.query('feature_set == "sales_only"')]:
            with self.assertRaises(ValueError):
                self.evaluate(frame)

    def test_nonfinite_boolean_string_and_noninteger_id_inputs_rejected(self):
        for value in (np.nan, np.inf, True, "1", 1+2j):
            frame = self.predictions.astype({"prediction": object})
            frame.loc[0, "prediction"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.evaluate(frame)
        for name, value in [("store_id", 1.0), ("product_id", -1), ("dt", "2024-5-27")]:
            frame = self.predictions.copy()
            if name == "store_id":
                frame[name] = frame[name].astype(float)
            frame.loc[0, name] = value
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.evaluate(frame)

    def test_metadata_missing_duplicate_or_wrong_labels_rejected(self):
        wrong_label = self.metadata.copy()
        wrong_label.loc[0, "target_stockout_group"] = "stockout"
        for metadata in [self.metadata.iloc[1:], pd.concat([self.metadata, self.metadata.iloc[:1]]), wrong_label]:
            with self.assertRaises(ValueError):
                self.evaluate(metadata=metadata)

    def test_explicit_models_and_final_test_gate(self):
        for models in (["decision_tree", "linear_regression"], ["decision_tree", "decision_tree"], ["unknown"]):
            with self.assertRaises(ValueError):
                self.evaluate(models=models)
        for purpose, splits in [("final_experiment", ["validation"]), ("synthetic_test_only", ["test"]),
                                ("development_debugging", ["validation", "test"])]:
            with self.assertRaises(ValueError):
                self.evaluate(purpose=purpose, splits=splits)

    def test_baselines_use_one_common_reference(self):
        frame = self.predictions.query('feature_set == "sales_only"').copy()
        frame["model"], frame["feature_set"] = "persistence", "common_reference"
        report = self.evaluate(frame, models=["persistence"])
        self.assertTrue(report["paired_comparisons"].empty)
        with self.assertRaises(ValueError):
            self.evaluate(frame.assign(feature_set="stockout_aware"), models=["persistence"])


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.observations = pd.DataFrame({
            "store_id": [1, 2, 2, 2], "product_id": [10] * 4,
            "dt": ["2024-05-27", "2024-05-27", "2024-05-28", "2024-05-29"],
            "actual": [10.] * 4, "split": ["validation"] * 4})
        frames = []
        for condition, prediction in [("sales_only", [10.] * 4), ("stockout_aware", [11., 14., 14., 14.])]:
            frame = self.observations.copy()
            frame["prediction"], frame["model"] = prediction, "decision_tree"
            frame["feature_set"], frame["run_id"] = condition, "bootstrap-fixture"
            frames.append(frame[PREDICTION_COLUMNS])
        self.predictions = pd.concat(frames, ignore_index=True)

    def intervals(self, predictions=None, observations=None, **kwargs):
        return paired_store_intervals(
            self.predictions if predictions is None else predictions,
            self.observations if observations is None else observations,
            purpose=kwargs.get("purpose", "synthetic_test_only"), models=["decision_tree"],
            splits=kwargs.get("splits", ["validation"]))

    def test_literal_cluster_expansion_matches_weighted_estimate_and_percentiles(self):
        result = self.intervals().iloc[0]
        self.assertEqual(result.MAE_difference, 3.25)  # Not store-macro mean 2.5.
        self.assertEqual((result.n_stores, result.n_observations), (2, 4))
        self.assertEqual((result.replicates, result.seed, result.confidence_level), (2000, 245, .95))
        rng = np.random.Generator(np.random.PCG64(245))
        clusters = [[1.], [4., 4., 4.]]
        literal = [np.mean([v for store in selected for v in clusters[store]])
                   for selected in rng.integers(2, size=(2000, 2))]
        np.testing.assert_array_equal([result.ci_lower, result.ci_upper], np.quantile(literal, [.025, .975], method="linear"))
        self.assertIn("shared calendar shocks", result.limitations)

    def test_reproducible_row_order_invariant_and_correct_difference_sign(self):
        expected = self.intervals()
        shuffled = self.intervals(self.predictions.sample(frac=1, random_state=3))
        pd.testing.assert_frame_equal(expected, shuffled)
        reversed_predictions = self.predictions.copy()
        reversed_predictions["feature_set"] = reversed_predictions.feature_set.map(
            {"sales_only": "stockout_aware", "stockout_aware": "sales_only"})
        result = self.intervals(reversed_predictions).iloc[0]
        self.assertEqual(result.MAE_difference, -3.25)
        self.assertEqual((result.ci_lower, result.ci_upper), (-4., -1.))

    def test_one_store_is_not_a_confidence_interval(self):
        result = self.intervals(self.predictions.query('store_id == 2'),
                                self.observations.query('store_id == 2')).iloc[0]
        self.assertEqual(result.status, "insufficient_stores")
        self.assertEqual((result.n_stores, result.replicates), (1, 0))
        self.assertIsNone(result.ci_lower)
        self.assertIsNone(result.ci_upper)

    def test_degenerate_interval_is_labeled(self):
        predictions = self.predictions.copy()
        predictions.loc[predictions.feature_set.eq("stockout_aware"), "prediction"] = 12.
        result = self.intervals(predictions).iloc[0]
        self.assertEqual((result.ci_lower, result.ci_upper), (2., 2.))
        self.assertEqual(result.status, "degenerate_interval")

    def test_unmatched_rows_final_inputs_and_test_scoring_are_rejected(self):
        with self.assertRaises(ValueError):
            self.intervals(self.predictions.iloc[1:])
        with self.assertRaises(ValueError):
            self.intervals(purpose="final_experiment")
        with self.assertRaises(ValueError):
            self.intervals(splits=["test"])


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.tables, self.policy = shared_tables(), small_policy()

    def fit(self, tables=None, **kwargs):
        return fit_development(self.tables if tables is None else tables, self.policy,
                               purpose=kwargs.get("purpose", "synthetic_test_only"), run_id="tree-fixture")

    def test_fit_rows_allowlists_equal_budgets_and_no_validation_refit(self):
        expected_y = self.tables["observations"].query('split == "train"').actual.to_numpy()
        fits, prediction_indices = [], []

        class TrackingTree(DecisionTreeRegressor):
            def fit(estimator, x, y, **kwargs):
                fits.append(list(x.columns))
                np.testing.assert_array_equal(y, expected_y)
                return super().fit(x, y, **kwargs)

            def predict(estimator, x, **kwargs):
                prediction_indices.extend(x.index.tolist())
                return super().predict(x, **kwargs)

        with patch("src.models.decision_tree_SAS.v2.DecisionTreeRegressor", TrackingTree):
            predicted, selection, estimators = self.fit()
        self.assertEqual(len(fits), 8)
        self.assertEqual(fits.count(COMMON), 4)
        self.assertEqual(fits.count(COMMON + EXTRA), 4)
        test_indices = set(self.tables["observations"].query('split == "test"').index)
        self.assertFalse(test_indices.intersection(prediction_indices))
        self.assertEqual(set(predicted.split), {"train", "validation"})
        self.assertEqual(len(predicted), 244)
        self.assertFalse(selection["refit_on_validation"])
        for estimator in estimators.values():
            self.assertEqual(estimator.tree_.n_node_samples[0], 92)

    def test_test_and_retrospective_metadata_perturbation_changes_nothing(self):
        predicted, selection, _ = self.fit()
        altered = copy.deepcopy(self.tables)
        test = altered["observations"].split.eq("test")
        altered["observations"].loc[test, "actual"] = 1e9
        for name, columns in [("features_sales_only", COMMON[:-2]), ("features_stockout_aware", COMMON[:-2])]:
            altered[name].loc[test, columns] = 1e8
        altered["evaluation_metadata"]["target_stockout_hours"] = 16
        altered["evaluation_metadata"]["target_stockout_group"] = "stockout"
        actual, other_selection, _ = self.fit(altered)
        pd.testing.assert_frame_equal(predicted, actual)
        self.assertEqual(selection, other_selection)

    def test_reproducibility_and_stable_tie_break(self):
        first, selection, _ = self.fit()
        second, other_selection, _ = self.fit()
        pd.testing.assert_frame_equal(first, second)
        self.assertEqual(selection, other_selection)
        raw = fixture()
        raw["sale_amount"] = 1.
        _, tied, _ = self.fit(build_features(validate_records(raw)))
        for parameters in tied["selected_parameters"].values():
            self.assertEqual((parameters["max_depth"], parameters["min_samples_leaf"]), (1, 2))

    def test_tree_inspection_json_reconstructs_predictions(self):
        _, _, estimators = self.fit()
        for condition, estimator in estimators.items():
            tree = json.loads(json.dumps(serialize_tree(estimator), allow_nan=False))
            features = self.tables[f"features_{condition}"][tree["feature_names"]].iloc[:10]
            rebuilt = []
            for row in features.to_numpy(dtype=np.float32):
                node = 0
                while tree["children_left"][node] != -1:
                    node = (tree["children_left"][node] if row[tree["feature"][node]] <= tree["threshold"][node]
                            else tree["children_right"][node])
                rebuilt.append(tree["value"][node])
            np.testing.assert_array_equal(rebuilt, estimator.predict(features))

    def test_policy_and_final_inputs_fail_closed(self):
        for name, value in [("max_depth", [True]), ("min_samples_leaf", [0]),
                            ("max_depth", [1, 1]), ("random_state", True),
                            ("prediction_postprocessing", "clip_nonnegative")]:
            policy = dict(self.policy, **{name: value})
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_policy(policy)
        with self.assertRaises(ValueError):
            self.fit(purpose="final_experiment")


class RunIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.tables = shared_tables()
        self.bundle = self.root / "fixture-bundle"
        sample = self.tables["observations"][SERIES].drop_duplicates().reset_index(drop=True)
        publish_bundle(self.bundle, self.tables, sample, {},
                       {"purpose": "synthetic_test_only", "configuration_snapshot": {}})
        self.digest = sha256(self.bundle / "bundle_manifest.json")
        self.identity = pinned_bundle(self.bundle, self.digest)[2]
        self.policy_path = self.root / "policy.json"
        write_json(self.policy_path, small_policy())

    def tree_run(self):
        destination = self.root / "tree-run"
        manifest = train_tree_run(self.bundle, self.digest, destination, "fixture-tree", self.policy_path)
        return destination, manifest

    def baseline_run(self):
        destination = self.root / "baseline-run"
        destination.mkdir()
        predicted = baseline_predictions(self.tables, "fixture-baselines")
        write_csv(destination / "predictions.csv", predicted)
        write_json(destination / "run_manifest.json", {
            "protocol_version": "2.0", "purpose": "synthetic_test_only",
            "run_id": "fixture-baselines", "models": ["persistence", "recent_avg_7"],
            "bundle_manifest_sha256": self.digest,
            "artifacts": {"predictions.csv": sha256(destination / "predictions.csv")},
        })
        return destination

    def test_roundtrip_tree_plus_delta_compatible_baseline_comparison(self):
        tree, manifest = self.tree_run()
        self.assertEqual(manifest["evidence_status"], "SYNTHETIC_NOT_RESEARCH")
        self.assertFalse(manifest["test_scored"])
        self.assertEqual(set(manifest["selected_parameters"]), set(CONDITIONS))
        baseline = self.baseline_run()
        destination = self.root / "comparison"
        with patch("src.evaluation_SAS.runs.evaluate_predictions", wraps=evaluate_predictions) as scoring:
            result = evaluate_runs(self.bundle, self.digest, [tree, baseline], destination,
                                   "fixture-comparison", ["decision_tree", "persistence", "recent_avg_7"])
        self.assertEqual(set(scoring.call_args.args[0].split), {"validation"})
        overall = pd.read_csv(destination / "overall.csv")
        self.assertEqual(len(overall), 4)
        self.assertTrue(overall.n_observations.eq(30).all())
        self.assertFalse(result["test_scored"])
        self.assertEqual(result["scored_splits"], ["validation"])
        intervals = pd.read_csv(destination / "mae_difference_intervals.csv")
        self.assertEqual(set(intervals.split), {"validation"})
        self.assertTrue(intervals.n_stores.eq(2).all())
        self.assertEqual(result["uncertainty"]["replicates"], 2000)
        for name, record in result["artifacts"].items():
            self.assertEqual(sha256(destination / name), record["sha256"])
        with self.assertRaises(FileExistsError):
            evaluate_runs(self.bundle, self.digest, [tree], destination, "fixture-comparison", ["decision_tree"])
        with self.assertRaises(FileExistsError):
            self.tree_run()

    def test_manifest_pin_tamper_and_incompatible_provenance_rejected(self):
        with self.assertRaises(ValueError):
            pinned_bundle(self.bundle, "0" * 64)
        with self.assertRaises(ValueError):
            pinned_bundle(self.bundle, None)
        directory, manifest = self.tree_run()
        original = copy.deepcopy(manifest)
        for name, value in [("sample_sha256", "0" * 64), ("bundle_manifest_sha256", "0" * 64),
                            ("producer_contract_version", "other"), ("purpose", "final_experiment"),
                            ("test_scored", True), ("policy", None)]:
            write_json(directory / "run_manifest.json", dict(original, **{name: value}))
            with self.subTest(name=name), self.assertRaises(ValueError):
                load_prediction_run(directory, self.identity, self.tables["observations"])
        write_json(directory / "run_manifest.json", original)
        with (directory / "predictions.csv").open("a") as handle:
            handle.write("tampered\n")
        with self.assertRaises(ValueError):
            load_prediction_run(directory, self.identity, self.tables["observations"])

    def test_final_bundle_and_test_scoring_rejected(self):
        manifest_path = self.bundle / "bundle_manifest.json"
        manifest = read_json(manifest_path)
        manifest["purpose"] = "final_experiment"
        write_json(manifest_path, manifest)
        digest = sha256(manifest_path)
        with self.assertRaises(ValueError):
            train_tree_run(self.bundle, digest, self.root / "blocked", "blocked", self.policy_path)
        self.assertFalse((self.root / "blocked").exists())
        manifest["purpose"] = "synthetic_test_only"
        write_json(manifest_path, manifest)
        with self.assertRaises(ValueError):
            evaluate_runs(self.bundle, self.digest, [], self.root / "blocked", "blocked", ["decision_tree"], ["test"])

    def test_missing_model_duplicate_run_and_wrong_actual_rejected(self):
        tree, manifest = self.tree_run()
        for directories, models in [([tree], ["decision_tree", "linear_regression"]),
                                    ([tree, tree], ["decision_tree"])]:
            with self.assertRaises(ValueError):
                evaluate_runs(self.bundle, self.digest, directories, self.root / "blocked", "blocked", models)
        path = tree / "predictions.csv"
        predicted = pd.read_csv(path, converters={"actual": float, "prediction": float})
        predicted.loc[0, "actual"] = np.nextafter(predicted.loc[0, "actual"], np.inf)
        write_csv(path, predicted)
        manifest["artifacts"]["predictions.csv"] = {"sha256": sha256(path), "bytes": path.stat().st_size}
        write_json(tree / "run_manifest.json", manifest)
        with self.assertRaises(ValueError):
            load_prediction_run(tree, self.identity, self.tables["observations"])

    def test_transaction_cleanup_and_duplicate_json_fields(self):
        destination = self.root / "failed"
        with self.assertRaises(RuntimeError):
            with new_run(destination) as temporary:
                (temporary / "partial").write_text("test-only")
                raise RuntimeError("fixture failure")
        self.assertFalse(destination.exists())
        self.assertFalse(list(self.root.glob(".sas-building-*")))
        path = self.root / "invalid.json"
        path.write_text('{"criterion":"squared_error","criterion":"absolute_error"}')
        with self.assertRaises(ValueError):
            read_json(path)


if __name__ == "__main__":
    unittest.main()
