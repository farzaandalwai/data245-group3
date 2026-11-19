"""V2 scientific metadata and reusable static guards; no ML execution."""
import tomllib
import unittest
from pathlib import Path

import yaml

from scripts.audit_contract import (
    business_stockout_hours, candidate_history_reason, parse_stock_status,
)

ROOT = Path(__file__).resolve().parents[1]
COMMON = ["sales_lag_1", "sales_lag_2", "sales_lag_3", "sales_lag_7",
          "sales_lag_14", "sales_mean_7", "sales_mean_14", "weekday", "is_weekend"]
EXTRA = ["stockout_hours_lag_1", "stockout_hours_mean_7", "stockout_hours_mean_14",
         "stockout_day_fraction_7", "stockout_day_fraction_14"]


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys that would silently replace protocol settings."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


class SharedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs = {
            path.stem: yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
            for path in (ROOT / "configs").glob("*.yaml")
        }
        cls.data = cls.configs["dataset"]
        cls.experiment = cls.configs["experiments"]
        cls.models = cls.configs["models"]
        cls.contract = cls.configs["contract"]

    def test_active_registration_and_draft_gates(self):
        registration = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["data245"]
        self.assertEqual(registration["contract_file"], "configs/contract.yaml")
        self.assertIn(registration["contract_file"], registration["config_files"])
        self.assertEqual(self.contract["contract_version"], "2.0-draft")
        self.assertEqual(self.contract["authority"], "docs/experiment_protocol.md")
        for name, relative in self.contract["metadata_files"].items():
            self.assertEqual(relative, f"configs/{name}.yaml")
            self.assertTrue((ROOT / relative).is_file())
        for config in self.configs.values():
            self.assertEqual(config["protocol_version"], "2.0")
            self.assertEqual(config["scientific_status"], "approved")
        self.assertEqual(self.contract["technical_contract_status"], "draft")
        for flag in ("contract_frozen", "implementation_verified",
                     "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed"):
            self.assertIs(self.contract[flag], False)
        self.assertIs(self.experiment["contract_frozen"], False)
        self.assertEqual(self.models["prediction_contract_status"], "draft")

    def test_recorded_sales_samples_and_pending_final_manifest(self):
        self.assertEqual(self.data["target"], "sale_amount")
        self.assertEqual(self.data["forecast_horizon_days"], 1)
        self.assertEqual(self.data["key"], ["store_id", "product_id", "dt"])
        self.assertEqual(self.data["pilot_series"], 200)
        self.assertEqual(self.data["pilot_purpose"], "development_debugging")
        final = self.data["final_sample"]
        self.assertEqual(final["series"], 1000)
        self.assertEqual(final["status"], "not_generated")
        self.assertIsNone(final["manifest"])
        self.assertEqual(final["proposed_seed"], 245)
        self.assertTrue(final["same_sample_across_models_and_conditions"])
        self.assertTrue(final["fixed_reproducible_selection_required"])
        self.assertIn("stratify_stockout_activity_using_training_period_only",
                      final["recommended_requirements"])
        self.assertIn("never_select_on_validation_or_test_outcomes", final["recommended_requirements"])

    def test_all_eligible_primary_population_and_retrospective_groups(self):
        eligibility = self.experiment["eligibility"]
        self.assertEqual(eligibility["primary_population"],
                         "all_eligible_target_dates_including_stockouts")
        self.assertIs(eligibility["exclude_solely_for_target_stockout"], False)
        self.assertIs(eligibility["target_availability_is_predictor"], False)
        self.assertEqual(eligibility["secondary_test_groups"],
                         ["fully_stocked_target_dates", "stockout_target_dates"])
        self.assertTrue(eligibility["groups_are_retrospective_evaluation_only"])
        self.assertIs(eligibility["separate_group_models"], False)
        self.assertTrue(eligibility["keep_stockouts_in_history"])
        self.assertTrue(eligibility["same_target_keys_actuals_splits_across_models_conditions_baselines"])
        self.assertNotIn("planned_target_stockout_hours", eligibility)

    def test_day_15_primary_boundary_and_optional_sensitivities(self):
        self.assertEqual(self.experiment["primary_history_days"], 14)
        self.assertEqual(self.experiment["first_target_day"], 15)
        self.assertFalse(self.experiment["history_comparison_required"])
        self.assertEqual(candidate_history_reason(14), "insufficient_14_day_history")
        for day in (15, 28, 29, 60, 61, 75, 76, 90):
            self.assertEqual(candidate_history_reason(day), "candidate")
        # Target stockout count is deliberately absent from this history-only API.
        for value in (0, 91, True, 1.5):
            with self.assertRaises(ValueError):
                candidate_history_reason(value)
        with self.assertRaises(ValueError):
            candidate_history_reason(29, history_days=28)

    def test_chronology_and_projected_not_observed_counts(self):
        splits = self.experiment["splits"]
        self.assertEqual([(splits[s]["first_day"], splits[s]["last_day"])
                          for s in ("train", "validation", "test")],
                         [(1, 60), (61, 75), (76, 90)])
        projected = self.experiment["projected_final_candidate_counts"]
        self.assertEqual(projected["status"], "projected_not_generated")
        self.assertEqual([projected[s] for s in ("train", "validation", "test", "total")],
                         [46000, 15000, 15000, 76000])
        self.assertNotIn("eligible_rows", self.experiment)

    def test_exact_paired_features_exclude_ids_targets_and_metadata(self):
        self.assertEqual(self.experiment["sales_only_predictors"], COMMON)
        self.assertEqual(self.experiment["stockout_additional_predictors"], EXTRA)
        self.assertTrue(self.experiment["stockout_aware_includes_all_sales_only"])
        self.assertEqual(len(set(COMMON + EXTRA)), 14)
        banned = set(self.data["key"]) | {
            "sale_amount", "actual", "prediction", "split", "day_number",
            "hours_sale", "hours_stock_status", "stock_hour6_22_cnt",
            "target_stockout_hours", "target_stockout_free",
            "sales_std_14", "stockout_free_lag_1",
        }
        self.assertFalse(banned & set(COMMON + EXTRA))
        self.assertFalse(self.experiment["identifiers_are_predictors"])
        self.assertTrue(self.experiment["historical_features_exclude_target_date"])
        self.assertEqual(self.experiment["transform_group"], ["store_id", "product_id"])
        self.assertEqual(self.experiment["transform_order"], "chronological")
        self.assertTrue(self.experiment["additional_context_features_require_amendment"])
        interface = (ROOT / "docs/interfaces.md").read_text(encoding="utf-8")
        for name in COMMON + EXTRA:
            self.assertIn(f"`{name}`", interface)

    def test_model_scope_ownership_and_shared_evaluation(self):
        expected = {
            "persistence": ("DELTA", "required_baseline"),
            "recent_avg_7": ("DELTA", "required_baseline"),
            "linear_regression": ("DEVGRU", "required_core"),
            "ridge_regression": ("DEVGRU", "approved_extension"),
            "decision_tree": ("SAS", "required_core"),
            "random_forest": ("SAS", "approved_optional_extension"),
        }
        for name, (owner, scope) in expected.items():
            model = self.models["models"][name]
            self.assertEqual((model["owner"], model["scope"]), (owner, scope))
            self.assertNotIn("enabled", model)  # Approval is distinct from implementation.
            if scope != "required_baseline":
                self.assertEqual(model["status"], "not_implemented")
        self.assertTrue(self.models["applicable_learned_models_compare_both_feature_conditions"])
        self.assertTrue(self.models["baselines_use_same_evaluation_population"])

    def test_training_validation_test_discipline_and_metrics(self):
        e = self.experiment
        self.assertEqual(e["preprocessing_fit"], "training_only")
        self.assertEqual(e["tuning"], "validation_only")
        self.assertTrue(e["matched_tuning_policy_required"])
        self.assertFalse(e["test_used_for_selection"])
        self.assertEqual(e["primary_metric"], "MAE")
        self.assertEqual(e["secondary_metrics"], ["RMSE", "signed_bias"])
        self.assertEqual(e["signed_bias_definition"], "mean(prediction - actual)")
        self.assertEqual(self.models["prediction_columns"],
                         ["store_id", "product_id", "dt", "actual", "prediction",
                          "model", "feature_set", "split", "run_id"])
        self.assertEqual(len(set(self.models["prediction_columns"])), 9)

    def test_retained_safe_parser_and_historical_endpoints(self):
        vector = [0] * 24
        for hour in (5, 6, 21, 22):
            vector[hour] = 1
        parsed = parse_stock_status("[" + " ".join(map(str, vector)) + "]")
        self.assertEqual(business_stockout_hours(parsed), 2)
        self.assertEqual(sum(parsed), 4)
        for malformed in ("[0 1]", "[" + " ".join(["2"] * 24) + "]",
                          "__import__('os')", "[" + " ".join(["nan"] * 24) + "]"):
            with self.assertRaises(ValueError):
                parse_stock_status(malformed)
        self.assertFalse(self.data["stockout_semantics_verified"])
        self.assertEqual(self.experiment["eligibility"]["subgroup_semantics"], "pending_verification")

    def test_duplicate_yaml_keys_rejected(self):
        with self.assertRaises(ValueError):
            yaml.load("first_target_day: 15\nfirst_target_day: 29", Loader=UniqueLoader)


if __name__ == "__main__":
    unittest.main()
