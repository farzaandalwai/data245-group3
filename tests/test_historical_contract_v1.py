"""Historical V1 reproduction only; these assertions never define active V2."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "docs/history/contract_v1"
spec = importlib.util.spec_from_file_location(
    "historical_v1_audit", HISTORY / "scripts/audit_contract.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


class HistoricalV1Tests(unittest.TestCase):
    def test_exact_snapshot_source_bytes(self):
        manifest = json.loads((HISTORY / "manifest.json").read_text())
        self.assertEqual(manifest["source_commit"], "193958625ead844d243405729298e27d485fc0b5")
        for relative, expected in manifest["files"].items():
            self.assertEqual(hashlib.sha256((HISTORY / relative).read_bytes()).hexdigest(), expected)

    def test_original_four_entry_lock_with_explicit_relocation(self):
        lock = json.loads((HISTORY / "configs/contract.lock.json").read_text())
        self.assertEqual(lock["contract_version"], "1.0.0")
        self.assertEqual(set(lock["sha256"]), {
            "configs/contract.yaml", "docs/contract_audit.json",
            "data/processed/pilot_200_series.csv", "data/manifests/pilot_series_manifest.csv",
        })
        for relative, expected in lock["sha256"].items():
            location = ROOT if relative.startswith("data/") else HISTORY
            self.assertEqual(hashlib.sha256((location / relative).read_bytes()).hexdigest(), expected)

    def test_historical_audit_reproduces_without_output_files_or_scores(self):
        recorded = json.loads((HISTORY / "docs/contract_audit.json").read_text())
        self.assertEqual(legacy.audit(ROOT), recorded)
        self.assertEqual(recorded["slice_6_22_count_mismatches"], 0)
        self.assertEqual([recorded["splits"][s]["eligible"]
                          for s in ("train", "validation", "test")], [3693, 1698, 1747])

    def test_legacy_eligibility_only_in_historical_module(self):
        self.assertEqual(legacy.eligibility_reason(28, 0), "insufficient_28_day_history")
        self.assertEqual(legacy.eligibility_reason(29, 0), "eligible")
        self.assertEqual(legacy.eligibility_reason(29, 1), "target_stockout")

    def test_historical_feature_pairing_and_original_gates(self):
        contract = yaml.safe_load((HISTORY / "configs/contract.yaml").read_text())
        features = contract["features"]
        self.assertEqual(features["feature_sets"]["sales_only"], features["common_predictors"])
        self.assertEqual(features["feature_sets"]["stockout_aware"],
                         features["common_predictors"] + features["stockout_additional_predictors"])
        self.assertFalse(set(features["excluded_source_columns"]) &
                         set(features["feature_sets"]["stockout_aware"]))
        self.assertTrue(contract["eligibility"]["same_target_keys_for_all_conditions_models_windows"])
        self.assertFalse(contract["models"]["ridge_regression"]["enabled"])
        self.assertFalse(contract["models"]["random_forest"]["enabled"])
        self.assertFalse(contract["selection"]["initial_validation_parameters_frozen"])


if __name__ == "__main__":
    unittest.main()
