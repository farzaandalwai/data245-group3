"""Synthetic regressions for owned packaging, isolation and fitted-state exports."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from scripts.delta_v2 import fixture
from scripts.verify_devgru import verify_files
from src.data_preprocessing_DELTA.v2 import validate_records, SERIES
from src.evaluation_SAS.runs import load_prediction_run
from src.features_DELTA.bundle import publish_bundle, sha256
from src.features_DELTA.v2 import build_features
from src.models.baselines_DELTA import v2 as baselines
from src.models.linear_regression_DEVGRU.artifacts import model_from_state
from src.models.linear_regression_DEVGRU.core import feature_names, keyed_observations
from src.models.linear_regression_DEVGRU.development import run_development


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.raw = validate_records(fixture())
        self.tables = build_features(self.raw)

    def bundle(self, purpose="synthetic_test_only"):
        directory = self.root / purpose
        publish_bundle(directory, self.tables, self.raw[SERIES].drop_duplicates(), {},
                       {"purpose": purpose, "source_sha256": "synthetic", "bundle_id": "synthetic",
                        "configuration_snapshot": {"synthetic": True}})
        manifest = json.loads((directory / "bundle_manifest.json").read_text())
        identity = {k: manifest[k] for k in ("purpose", "protocol_version", "producer_contract_version", "sample_sha256")}
        identity["bundle_manifest_sha256"] = sha256(directory / "bundle_manifest.json")
        return directory, identity

    def test_baseline_runner_never_materializes_test_predictions_and_sas_accepts(self):
        bundle, identity = self.bundle("development_debugging")
        original = baselines.predictions
        def observe(tables, run_id):
            self.assertEqual(set(tables["observations"].split), {"train", "validation"})
            return original(tables, run_id)
        destination = self.root / "baseline"
        with patch.object(baselines, "predictions", side_effect=observe):
            baselines.run_development(bundle, destination, "synthetic-baseline",
                                     expected_manifest_sha256=identity["bundle_manifest_sha256"])
        predicted, manifest = load_prediction_run(destination, identity, self.tables["observations"])
        self.assertEqual(len(predicted), 244)
        self.assertFalse(manifest["test_scored"])
        self.assertEqual(set(pd.read_csv(destination / "metrics.csv").split), {"train", "validation"})

    def test_baseline_final_rejected_before_outcomes_and_failed_publish_is_atomic(self):
        final, final_identity = self.bundle("final_experiment")
        with patch.object(baselines, "load_bundle", side_effect=AssertionError("outcomes opened")):
            with self.assertRaises(ValueError):
                baselines.run_development(final, self.root / "blocked", "blocked",
                                         expected_manifest_sha256=final_identity["bundle_manifest_sha256"])
        bundle, identity = self.bundle("development_debugging")
        destination = self.root / "failed"
        with patch.object(baselines, "write_csv", side_effect=OSError("synthetic disk failure")):
            with self.assertRaises(OSError):
                baselines.run_development(bundle, destination, "synthetic-failure",
                                         expected_manifest_sha256=identity["bundle_manifest_sha256"])
        self.assertFalse(destination.exists())
        self.assertFalse(list(self.root.glob(".delta-devgru-*")))

    def test_untrusted_baseline_and_nonprotocol_bootstrap_rejected_before_loading(self):
        bundle, identity = self.bundle("development_debugging")
        with patch.object(baselines, "load_bundle", side_effect=AssertionError("untrusted load")):
            with self.assertRaises(ValueError):
                baselines.run_development(bundle, self.root / "blocked", "blocked",
                                         expected_manifest_sha256="0" * 64)
        for options in ({"seed": 246}, {"bootstrap_repetitions": 20}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                run_development(bundle, identity["bundle_manifest_sha256"], self.root / "blocked",
                                "blocked", **options)
        self.assertFalse((self.root / "blocked").exists())

    def test_devgru_new_run_roundtrip_without_refit_and_shared_reader(self):
        bundle, identity = self.bundle()
        destination = self.root / "new-devgru"
        run_development(bundle, identity["bundle_manifest_sha256"], destination, "synthetic-devgru")
        predicted, manifest = load_prediction_run(destination, identity, self.tables["observations"])
        self.assertEqual(len(predicted), 488)
        self.assertEqual(set(predicted.run_id), {"synthetic-devgru"})
        self.assertFalse(manifest["test_scored"])
        self.assertEqual(manifest["evidence_status"], "SYNTHETIC_NOT_RESEARCH")
        self.assertEqual(manifest["uncertainty"]["cluster_unit"], "store_id")
        self.assertEqual(manifest["uncertainty"]["seed"], 245)
        self.assertEqual(manifest["uncertainty"]["replicates"], 2000)
        for model in ("linear_regression", "ridge_regression"):
            for condition in ("sales_only", "stockout_aware"):
                state = json.loads((destination / f"{model}.{condition}.model.json").read_text())
                restored = model_from_state(state)
                joined = keyed_observations(self.tables, condition)
                rows = joined.loc[joined.split.isin(["train", "validation"])]
                original = predicted.loc[predicted.model.eq(model) & predicted.feature_set.eq(condition)]
                with patch.object(restored, "fit", side_effect=AssertionError("reload fitted")):
                    np.testing.assert_allclose(restored.predict(rows[feature_names(condition)]),
                                               original.prediction, rtol=1e-14, atol=1e-14)
        with self.assertRaises(FileExistsError):
            run_development(bundle, identity["bundle_manifest_sha256"], destination, "synthetic-devgru")

    def test_devgru_final_and_unpinned_inputs_rejected_before_loading(self):
        bundle, identity = self.bundle("final_experiment")
        with patch("src.models.linear_regression_DEVGRU.development.load_bundle",
                   side_effect=AssertionError("outcomes opened")):
            with self.assertRaises(ValueError):
                run_development(bundle, identity["bundle_manifest_sha256"], self.root / "blocked", "blocked")
            with self.assertRaises(ValueError):
                run_development(bundle, "", self.root / "blocked", "blocked")
        self.assertFalse((self.root / "blocked").exists())

    def test_devgru_exports_reject_invalid_feature_order_and_scaler_state(self):
        width = len(feature_names("sales_only"))
        state = {"format": "devgru-numeric-model-1", "model": "linear_regression",
                 "feature_set": "sales_only", "feature_names": feature_names("sales_only"),
                 "preprocessing_policy": "standardize", "intercept": 0.0,
                 "coefficients": [1.0] * width, "alpha": None,
                 "preprocessor": {"mean": [0.0] * width, "scale": [1.0] * width}}
        invalid = []
        wrong = copy.deepcopy(state); wrong["feature_names"][0] = "target_stockout_hours"; invalid.append(wrong)
        wrong = copy.deepcopy(state); wrong["preprocessor"]["scale"][0] = 0; invalid.append(wrong)
        wrong = copy.deepcopy(state); wrong["coefficients"][0] = float("nan"); invalid.append(wrong)
        wrong = copy.deepcopy(state); wrong["coefficients"][0] = True; invalid.append(wrong)
        wrong = copy.deepcopy(state); wrong["preprocessor"] = None; invalid.append(wrong)
        for wrong in invalid:
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):
                model_from_state(wrong)

    def test_output_inside_bundle_rejected_and_partial_devgru_run_removed(self):
        bundle, identity = self.bundle()
        with self.assertRaises(ValueError):
            run_development(bundle, identity["bundle_manifest_sha256"], bundle / "illegal", "synthetic")
        destination = self.root / "failed"
        with patch("src.models.linear_regression_DEVGRU.development.write_json", side_effect=OSError("disk")):
            with self.assertRaises(OSError):
                run_development(bundle, identity["bundle_manifest_sha256"], destination, "synthetic")
        self.assertFalse(destination.exists())
        self.assertFalse(list(self.root.glob(".delta-devgru-*")))

    def test_explicit_lf_crlf_evidence_identity_and_tamper_rejection(self):
        import hashlib
        lf = b"a,b\n1,2\n"
        crlf = b"a,b\r\n1,2\r\n"
        identity = lambda b: {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        record = {"example.csv": {**identity(lf), "windows_crlf": identity(crlf)}}
        p = self.root / "example.csv"
        for payload, label in [(lf, "published_LF_bytes"), (crlf, "registered_CRLF_representation_NOT_original_byte_identity")]:
            p.write_bytes(payload)
            self.assertEqual(verify_files(self.root, record)["example.csv"], label)
            self.assertEqual(p.read_bytes(), payload)
        p.write_bytes(b"a,b\n1,9\n")
        with self.assertRaises(ValueError):
            verify_files(self.root, record)
        with self.assertRaises(ValueError):
            verify_files(self.root, {"../escape.csv": identity(lf)})


if __name__ == "__main__":
    unittest.main()
