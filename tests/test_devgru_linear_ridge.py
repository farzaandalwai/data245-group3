import unittest

import numpy as np
import pandas as pd

from src.features_DELTA.bundle import load_bundle
from src.models.linear_regression_DEVGRU.core import (
    FEATURES, PREDICTION_COLUMNS, TrainOnlyStandardizer, feature_names,
    keyed_observations, prediction_frame, validate_paired_conditions, verify_prediction_frame,
)
from src.models.linear_regression_DEVGRU.model import LinearRegressionModel
from src.models.ridge_regression_DEVGRU.model import RidgeRegressionModel, select_ridge_alpha


ROOT = "data/processed/feature_bundles/v2-synthetic-fixture-r2"
HASH = "3c51884b4d24a615d797578af8fc047c1109d82ec55b3017ce97556b7b180769"
KEY = ["store_id", "product_id", "dt"]


class DevgruModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables, cls.manifest = load_bundle(ROOT, expected_manifest_sha256=HASH)

    def test_exact_allowlists_order_and_unsupported_set(self):
        sales = ["sales_lag_1", "sales_lag_2", "sales_lag_3", "sales_lag_7", "sales_lag_14",
                 "sales_mean_7", "sales_mean_14", "weekday", "is_weekend"]
        extra = ["stockout_hours_lag_1", "stockout_hours_mean_7", "stockout_hours_mean_14",
                 "stockout_day_fraction_7", "stockout_day_fraction_14"]
        self.assertEqual(feature_names("sales_only"), sales)
        self.assertEqual(feature_names("stockout_aware"), sales + extra)
        with self.assertRaises(ValueError):
            feature_names("unexpected")

    def test_unexpected_observation_metadata_never_enters_model_matrix(self):
        tables = {name: frame.copy() for name, frame in self.tables.items()}
        tables["observations"]["unexpected_numeric_metadata"] = 123.0
        model = LinearRegressionModel("none")
        predictions = model.fit_predict_bundle(tables, "sales_only", "synthetic-linear")
        self.assertEqual(list(predictions.columns), PREDICTION_COLUMNS)
        self.assertEqual(model.coef_.shape, (len(FEATURES["sales_only"]),))

    def test_keyed_pair_validation_and_missing_duplicate_extra_failures(self):
        validate_paired_conditions(self.tables)
        missing = {name: frame.copy() for name, frame in self.tables.items()}
        missing["features_sales_only"] = missing["features_sales_only"].iloc[:-1]
        with self.assertRaises(ValueError):
            keyed_observations(missing, "sales_only")
        duplicate = {name: frame.copy() for name, frame in self.tables.items()}
        duplicate["features_stockout_aware"] = pd.concat([
            duplicate["features_stockout_aware"], duplicate["features_stockout_aware"].iloc[:1]
        ])
        with self.assertRaises(ValueError):
            keyed_observations(duplicate, "stockout_aware")
        extra = {name: frame.copy() for name, frame in self.tables.items()}
        extra["features_sales_only"]["unexpected"] = 1.0
        with self.assertRaises(ValueError):
            keyed_observations(extra, "sales_only")
        inconsistent = {name: frame.copy() for name, frame in self.tables.items()}
        inconsistent["features_sales_only"].loc[0, "dt"] = "2024-04-12"
        with self.assertRaises(ValueError):
            validate_paired_conditions(inconsistent)

    def test_train_only_preprocessing_validation_reuse_and_zero_variance(self):
        scaler = TrainOnlyStandardizer().fit(np.array([[1.0, 4.0], [3.0, 4.0]]))
        np.testing.assert_allclose(scaler.mean_, [2.0, 4.0])
        np.testing.assert_allclose(scaler.scale_, [1.0, 1.0])
        np.testing.assert_allclose(scaler.transform(np.array([[5.0, 4.0]])), [[3.0, 0.0]])
        with self.assertRaises(RuntimeError):
            TrainOnlyStandardizer().transform(np.ones((1, 1)))

        joined = keyed_observations(self.tables, "sales_only")
        names = feature_names("sales_only")
        train = joined.split.eq("train")
        model = LinearRegressionModel("standardize").fit(
            joined.loc[train, names].to_numpy(), joined.loc[train, "actual"].to_numpy()
        )
        np.testing.assert_allclose(model.preprocessor.mean_, joined.loc[train, names].mean().to_numpy())
        ridge = RidgeRegressionModel(1.0, "standardize").fit(
            joined.loc[train, names].to_numpy(), joined.loc[train, "actual"].to_numpy()
        )
        np.testing.assert_allclose(ridge.preprocessor.mean_, model.preprocessor.mean_)

    def test_test_predictions_blocked_and_permitted_population_is_exact(self):
        joined = keyed_observations(self.tables, "sales_only")
        model = LinearRegressionModel("none")
        predictions = model.fit_predict_bundle(self.tables, "sales_only", "synthetic-linear")
        self.assertEqual(set(predictions.split), {"train", "validation"})
        expected = joined[joined.split.isin(["train", "validation"])]
        self.assertEqual(len(predictions), len(expected))
        verify_prediction_frame(predictions, expected)
        validation_only = model.fit_predict_bundle(
            self.tables, "sales_only", "synthetic-validation", permitted_splits=("validation",)
        )
        self.assertEqual(set(validation_only.split), {"validation"})
        with self.assertRaises(ValueError):
            model.fit_predict_bundle(self.tables, "sales_only", "blocked", permitted_splits=("test",))
        with self.assertRaises(ValueError):
            model.fit_predict_bundle(self.tables, "sales_only", "blocked", permitted_splits=("train", "test"))

    def test_direct_prediction_frame_and_verifier_reject_test_rows(self):
        joined = keyed_observations(self.tables, "sales_only")
        test_rows = joined[joined.split.eq("test")]
        with self.assertRaises(ValueError):
            prediction_frame(test_rows, np.zeros(len(test_rows)), "linear_regression", "sales_only", "blocked")
        predictions = LinearRegressionModel("none").fit_predict_bundle(
            self.tables, "sales_only", "synthetic-validation", permitted_splits=("validation",)
        )
        test_expected = joined[joined.split.eq("test")]
        test_frame = predictions.copy()
        test_frame = test_frame.iloc[:len(test_expected)].copy()
        test_frame[["store_id", "product_id", "dt", "actual", "split"]] = test_expected[
            ["store_id", "product_id", "dt", "actual", "split"]
        ].to_numpy()
        with self.assertRaises(ValueError):
            verify_prediction_frame(test_frame, test_expected)

    def test_prediction_frame_labels_are_consistent(self):
        joined = keyed_observations(self.tables, "sales_only")
        rows = joined[joined.split.eq("validation")]
        base = prediction_frame(rows, np.zeros(len(rows)), "linear_regression", "sales_only", "run-a")
        for column, value in (("model", "ridge_regression"), ("feature_set", "stockout_aware"), ("run_id", "run-b")):
            mixed = base.copy()
            mixed.loc[mixed.index[0], column] = value
            with self.subTest(column=column):
                with self.assertRaises(ValueError):
                    verify_prediction_frame(mixed, rows)

    def test_prediction_schema_labels_dates_actuals_splits_and_keys(self):
        joined = keyed_observations(self.tables, "sales_only")
        predictions = LinearRegressionModel("none").fit_predict_bundle(
            self.tables, "sales_only", "synthetic-linear", permitted_splits=("validation",)
        )
        expected = joined[joined.split.eq("validation")]
        verify_prediction_frame(predictions, expected)
        cases = []
        first_index = predictions.index[0]
        bad_order = predictions.copy()
        bad_order["prediction"] = bad_order.pop("prediction")
        cases.append(bad_order)
        bad_date = predictions.copy()
        bad_date.loc[first_index, "dt"] = "2024-01-01 00:00:00"
        cases.append(bad_date)
        bad_actual = predictions.copy()
        bad_actual.loc[first_index, "actual"] += 1
        cases.append(bad_actual)
        bad_model = predictions.copy()
        bad_model.loc[first_index, "model"] = "other"
        cases.append(bad_model)
        bad_run = predictions.copy()
        bad_run.loc[first_index, "run_id"] = ""
        cases.append(bad_run)
        duplicate = pd.concat([predictions, predictions.iloc[:1]], ignore_index=True)
        cases.append(duplicate)
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    verify_prediction_frame(case, expected)

    def test_ridge_intercept_alpha_validation_and_ill_conditioning(self):
        X = np.column_stack([np.ones(20), np.linspace(0, 1, 20) + 1e-12 * np.arange(20)])
        y = 4.0 + 0.25 * X[:, 1]
        model = RidgeRegressionModel(1.0, "none").fit(X, y)
        self.assertTrue(np.isfinite(model.predict(X)).all())
        intercept_model = RidgeRegressionModel(100.0, "none").fit(np.zeros((3, 2)), np.array([2.0, 4.0, 6.0]))
        self.assertAlmostEqual(intercept_model.intercept_, 4.0)
        np.testing.assert_allclose(intercept_model.coef_, [0.0, 0.0])
        for alpha in (0, -1, np.nan, np.inf, "1", True):
            with self.assertRaises(ValueError):
                RidgeRegressionModel(alpha, "none")

    def test_validation_only_alpha_selection_bounds_and_tie_break(self):
        joined = keyed_observations(self.tables, "sales_only")

        class ConstantModel:
            def __init__(self, alpha, preprocessing_policy):
                self.alpha = alpha

            def fit(self, X, y):
                return self

            def predict(self, X):
                return np.zeros(len(X))

        factory = lambda alpha, preprocessing_policy: ConstantModel(alpha, preprocessing_policy)
        selected, evidence = select_ridge_alpha(
            factory, joined, [10.0, 1.0], feature_set="sales_only", preprocessing_policy="none"
        )
        self.assertEqual(selected, 1.0)
        self.assertEqual([row["alpha"] for row in evidence], [10.0, 1.0])
        invalid_grids = ([], [1.0, 1.0], [0], [-1], [np.nan], [np.inf], ["1"], list(range(1, 22)))
        for grid in invalid_grids:
            with self.subTest(grid=grid):
                with self.assertRaises(ValueError):
                    select_ridge_alpha(factory, joined, grid, feature_set="sales_only", preprocessing_policy="none")

        duplicate = pd.concat([joined, joined.iloc[:1]], ignore_index=True)
        with self.assertRaises(ValueError):
            select_ridge_alpha(factory, duplicate, [1.0], feature_set="sales_only", preprocessing_policy="none")
        invalid_split = joined.copy()
        invalid_split.loc[invalid_split.index[0], "split"] = "unknown"
        with self.assertRaises(ValueError):
            select_ridge_alpha(factory, invalid_split, [1.0], feature_set="sales_only", preprocessing_policy="none")
        missing = joined.drop(columns=["actual"])
        with self.assertRaises(ValueError):
            select_ridge_alpha(factory, missing, [1.0], feature_set="sales_only", preprocessing_policy="none")
        nonfinite = joined.copy()
        nonfinite.loc[nonfinite.split.eq("train"), "sales_lag_1"] = np.inf
        with self.assertRaises(ValueError):
            select_ridge_alpha(factory, nonfinite, [1.0], feature_set="sales_only", preprocessing_policy="none")
        with self.assertRaises(ValueError):
            select_ridge_alpha(factory, joined, [1.0], feature_set="sales_only", preprocessing_policy="invalid")

    def test_synthetic_smoke_is_non_test_only_and_deterministic(self):
        for model in (LinearRegressionModel("none"), RidgeRegressionModel(1.0, "none")):
            first = model.fit_predict_bundle(self.tables, "stockout_aware", "synthetic-smoke")
            self.assertFalse(first.split.eq("test").any())
            self.assertTrue(np.isfinite(first.prediction).all())


if __name__ == "__main__":
    unittest.main()
