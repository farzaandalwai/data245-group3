"""Stockout boundary, eligibility and locked-handoff checks; no ML execution."""

import hashlib
import json
import unittest
from pathlib import Path

import yaml

from scripts.audit_contract import (
    audit, business_stockout_hours, eligibility_reason, parse_stock_status,
)

ROOT = Path(__file__).resolve().parents[1]


class SharedContractTests(unittest.TestCase):
    def test_business_hour_endpoints_and_binary_parser(self):
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

    def test_history_boundary_and_sequential_filter_reason(self):
        self.assertEqual(eligibility_reason(28, 0), "insufficient_28_day_history")
        self.assertEqual(eligibility_reason(28, 1), "insufficient_28_day_history")
        self.assertEqual(eligibility_reason(29, 0), "eligible")
        self.assertEqual(eligibility_reason(29, 1), "target_stockout")
        self.assertEqual(eligibility_reason(90, 0), "eligible")

    def test_local_audit_matches_recorded_evidence_without_scoring(self):
        recorded = json.loads((ROOT / "docs/contract_audit.json").read_text())
        self.assertEqual(audit(ROOT), recorded)
        self.assertEqual(recorded["slice_6_22_count_mismatches"], 0)
        self.assertEqual([recorded["splits"][split]["eligible"]
                          for split in ("train", "validation", "test")], [3693, 1698, 1747])

    def test_locked_definition_and_source_hashes(self):
        lock = json.loads((ROOT / "configs/contract.lock.json").read_text())
        self.assertEqual(lock["contract_version"], "1.0.0")
        for relative, expected in lock["sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected,
                             f"Locked artifact changed without a contract amendment: {relative}")

    def test_feature_conditions_exclude_future_and_metadata_inputs(self):
        contract = yaml.safe_load((ROOT / "configs/contract.yaml").read_text())
        features = contract["features"]
        common, extra = features["common_predictors"], features["stockout_additional_predictors"]
        self.assertEqual(features["feature_sets"]["sales_only"], common)
        self.assertEqual(features["feature_sets"]["stockout_aware"], common + extra)
        self.assertFalse(set(common) & set(extra))
        banned = set(features["excluded_source_columns"]) | {"actual", "prediction", "dt", "eligible"}
        self.assertFalse(banned & set(common + extra))
        self.assertTrue(contract["eligibility"]["retain_stockout_days_in_input_history"])
        self.assertTrue(contract["eligibility"]["same_target_keys_for_all_conditions_models_windows"])
        for name, columns in contract["bundle"]["required_files"].items():
            if name.endswith(".csv"):
                self.assertEqual(len(columns), len(set(columns)), f"Duplicate columns in {name}")
        tree = contract["models"]["decision_tree"]
        candidates = len(tree["grid"]["max_depth"]) * len(tree["grid"]["min_samples_leaf"])
        self.assertEqual(candidates, tree["tuning_candidates_per_feature_set"])
        self.assertFalse(contract["models"]["ridge_regression"]["enabled"])
        self.assertFalse(contract["models"]["random_forest"]["enabled"])
        self.assertFalse(contract["selection"]["initial_validation_parameters_frozen"])
        self.assertEqual(contract["stockout_semantics"]["stop_hour_exclusive"], 22)


if __name__ == "__main__":
    unittest.main()
