"""Synthetic acceptance failures plus integrity checks on tracked original SAS files.

No real model fitting, no final bundle, and no reproduction of test outcomes.
"""
import copy
import json
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from scripts.sas_final_preflight import inspect_final_gates
from src.evaluation_SAS.integration import (
    FOREST_RUN_MANIFEST_SHA256, compare_development, devgru_originals, relative_mae_improvement,
    sas_forest, validation_baselines, verify_files,
)
from src.evaluation_SAS.runs import ROOT, pinned_bundle, read_json
from src.evaluation_SAS.v2 import CONDITIONS, PREDICTION_COLUMNS, regression_metrics
from src.features_DELTA.bundle import sha256, write_csv, write_json
from src.features_DELTA.v2 import COMMON, EXTRA
from tests.test_sas_v2 import shared_tables


class IncomingArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.tables = shared_tables()
        self.identity = {"purpose": "synthetic_test_only", "protocol_version": "2.0",
                         "bundle_manifest_sha256": "a" * 64}
        self.meta = {**self.identity, "preprocessing_policy": "standardize", "prediction_postprocessing": "none",
                     "feature_sets": {"sales_only": COMMON, "stockout_aware": COMMON + EXTRA},
                     "models": ["linear_regression", "ridge_regression"], "run_id": "fixture-parent",
                     "ridge_alpha_candidates": [.01, 1.], "selected_ridge_alphas": dict.fromkeys(CONDITIONS, 1.),
                     "source_git_revision": "fixture-base-not-execution-proof",
                     "bootstrap": {"repetitions": 2000, "seed_by_model": {"linear_regression": 245, "ridge_regression": 246}},
                     "experiments": []}
        metrics, tuning, intervals = [], [], []
        for model in self.meta["models"]:
            for condition in CONDITIONS:
                frame = self.tables["observations"].query('split != "test"').copy()
                frame["prediction"] = frame.actual + (.5 if condition == "sales_only" else .25)
                frame["model"], frame["feature_set"], frame["run_id"] = model, condition, f"fixture-{model}-{condition}"
                frame = frame[PREDICTION_COLUMNS]
                folder = self.root / model
                folder.mkdir(exist_ok=True)
                write_csv(folder / f"{condition}.predictions.csv", frame)
                self.meta["experiments"].append({"model_name": model, "feature_set": condition,
                    "run_id": frame.run_id.iloc[0], "prediction_rows": len(frame), "split_coverage": ["train", "validation"],
                    "bundle_manifest_sha256": self.identity["bundle_manifest_sha256"]})
                for split in ("train", "validation"):
                    part = frame.loc[frame.split.eq(split)]
                    scores = regression_metrics(part.actual, part.prediction)
                    metrics.append({"model": model, "feature_set": condition, "split": split,
                                    "rows": len(part), **{n: scores[n] for n in ("MAE", "RMSE", "signed_bias")}})
                if model == "ridge_regression":
                    score = .5 if condition == "sales_only" else .25
                    tuning.extend([{"feature_set": condition, "alpha": .01, "validation_mae": score + .25},
                                   {"feature_set": condition, "alpha": 1., "validation_mae": score}])
            intervals.append({"model": model, "MAE_difference_stockout_aware_minus_sales_only": -.25,
                              "bootstrap_ci_lower": -.25, "bootstrap_ci_upper": -.25,
                              "bootstrap_repetitions": 2000, "bootstrap_seed": 245 if model == "linear_regression" else 246,
                              "resampled_series": 2, "bootstrap_unit": "store-product series"})
        write_csv(self.root / "validation_metrics.csv", pd.DataFrame(metrics))
        write_csv(self.root / "ridge_alpha_selection.csv", pd.DataFrame(tuning))
        write_csv(self.root / "paired_validation_comparison.csv", pd.DataFrame(intervals))
        (self.root / "INVENTORY.md").write_text('| `run_metadata.json` | 5 | `' + 'b'*64 + '` |\n'
              '| `paired_validation_comparison.csv` | 5 | `' + 'c'*63 + '` |\n')
        self.save_metadata()

    def repin(self):
        self.pin = {"commit": "fixture-explicit-not-real-evidence", "pr_url": "fixture",
                    "files": {p.relative_to(self.root).as_posix(): {"sha256": sha256(p), "bytes": p.stat().st_size}
                              for p in self.root.rglob('*') if p.is_file()}}

    def save_metadata(self):
        write_json(self.root / "run_metadata.json", self.meta)
        self.repin()

    def accept(self):
        return devgru_originals(self.root, self.pin, self.identity, self.tables["observations"])

    def test_metadata_adapter_preserves_originals_and_normalizes_only_run_labels(self):
        before = copy.deepcopy(self.pin)
        frame, audit = self.accept()
        self.assertEqual(len(frame), 488)
        self.assertEqual(set(frame.split), {"train", "validation"})
        self.assertEqual(frame.groupby('model').run_id.nunique().tolist(), [1, 1])
        self.assertEqual(len(audit['run_id_mapping']), 4)
        self.assertEqual(len(audit['original_bootstrap_audit']), 2)
        self.assertEqual({r['file'] for r in audit['original_inventory_discrepancies']},
                         {'run_metadata.json', 'paired_validation_comparison.csv'})
        self.repin()
        self.assertEqual(before, self.pin)

    def test_tampered_published_file_is_rejected(self):
        with (self.root / 'linear_regression/sales_only.predictions.csv').open('a') as handle:
            handle.write('tamper\n')
        with self.assertRaises(ValueError):
            self.accept()

    def test_invalid_source_coverage_actuals_and_labels_are_rejected_even_with_new_pin(self):
        path = self.root / 'linear_regression/sales_only.predictions.csv'
        original = pd.read_csv(path, converters={'actual': float, 'prediction': float})
        wrong_actual = original.copy(); wrong_actual.loc[0, 'actual'] += .01
        wrong_split = original.copy(); wrong_split.loc[0, 'split'] = 'test'
        wrong_condition = original.copy(); wrong_condition.loc[0, 'feature_set'] = 'unknown'
        nonfinite = original.copy(); nonfinite.loc[0, 'prediction'] = np.inf
        for frame in [original.iloc[1:], pd.concat([original, original.iloc[:1]]),
                      wrong_actual, wrong_split, wrong_condition, nonfinite]:
            write_csv(path, frame); self.repin()
            with self.subTest(rows=len(frame)), self.assertRaises(ValueError):
                self.accept()
        write_csv(path, original)

    def test_incompatible_bundle_clipping_and_preprocessing_declarations_rejected(self):
        original = copy.deepcopy(self.meta)
        for field, value in [('bundle_manifest_sha256', '0'*64), ('preprocessing_policy', 'none'),
                             ('prediction_postprocessing', 'clip_nonnegative')]:
            self.meta = dict(original, **{field: value}); self.save_metadata()
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.accept()

    def test_selected_alpha_and_stored_metrics_must_match_original_predictions(self):
        self.meta['selected_ridge_alphas']['sales_only'] = .01
        self.save_metadata()
        with self.assertRaises(ValueError):
            self.accept()
        self.meta['selected_ridge_alphas']['sales_only'] = 1.
        self.save_metadata()
        path = self.root / 'validation_metrics.csv'
        metrics = pd.read_csv(path); metrics.loc[0, 'MAE'] += .1
        write_csv(path, metrics); self.repin()
        with self.assertRaises(ValueError):
            self.accept()

    def test_original_interval_mismatch_is_not_silently_harmonized(self):
        path = self.root / 'paired_validation_comparison.csv'
        frame = pd.read_csv(path); frame.loc[0, 'bootstrap_ci_lower'] -= .1
        write_csv(path, frame); self.repin()
        with self.assertRaises(ValueError):
            self.accept()

    def test_validation_baselines_never_receive_or_emit_test_rows(self):
        from src.models.baselines_DELTA.v2 import predictions
        with patch('src.models.baselines_DELTA.v2.predictions', wraps=predictions) as call:
            frame = validation_baselines(self.tables, 'test-fixture-baselines')
        self.assertEqual(set(call.call_args.args[0]['observations'].split), {'validation'})
        self.assertEqual(set(frame.split), {'validation'})
        self.assertEqual(len(frame), 60)
        features = self.tables['features_sales_only']
        for model, col in [('persistence', 'sales_lag_1'), ('recent_avg_7', 'sales_mean_7')]:
            actual = frame.loc[frame.model.eq(model)].merge(features, on=['store_id', 'product_id', 'dt'])
            np.testing.assert_array_equal(actual.prediction, actual[col])


class PreservationAndFinalGateTests(unittest.TestCase):
    def test_only_reviewed_artifact_CSVs_are_publishable_and_local_READMEs_stay_ignored(self):
        for name, ignored in [
            ('runs/SAS/incoming/example/README.md', True),
            ('outputs/example/README.md', True),
            ('data/raw/freshretail.csv', True),
            ('artifacts/SAS/development/unreviewed/predictions.csv', True),
            ('artifacts/SAS/development/original-200-series-20261119/decision_tree/predictions.csv', False),
            ('artifacts/SAS/development/harmonized-200-series-20261120-r3/development_comparison.csv', False),
            ('artifacts/SAS/development/random-forest-200-series-20261120/predictions.csv', False),
            ('artifacts/SAS/development/harmonized-200-series-20261123-r4/development_comparison.csv', False),
            ('artifacts/SAS/development/harmonized-200-series-20261123-r4/unreviewed.csv', True),
        ]:
            result = subprocess.run(['git', 'check-ignore', '--no-index', '-q', name], cwd=ROOT)
            self.assertIn(result.returncode, (0, 1))
            self.assertEqual(result.returncode == 0, ignored, name)

    def test_shared_original_SAS_files_match_prior_committed_evidence(self):
        evidence = read_json(ROOT / 'docs/SAS_INTEGRATION_EVIDENCE.json')
        package = ROOT / 'artifacts/SAS/development/original-200-series-20261119'
        expected = {}
        for key, folder in [('real_tree', 'decision_tree'), ('real_validation', 'comparison')]:
            record = evidence['runs'][key]
            expected[f"{folder}/{Path(record['path']).name}"] = {'sha256': record['sha256']}
            expected.update({folder+'/'+name: info for name, info in record['artifact_hashes'].items()})
        self.assertEqual(len(expected), 16)
        verify_files(package, expected)

    def test_shared_forest_run_matches_recorded_identity_and_SHA256SUMS(self):
        package = ROOT / 'artifacts/SAS/development/random-forest-200-series-20261120'
        self.assertEqual(sha256(package / 'run_manifest.json'), FOREST_RUN_MANIFEST_SHA256)
        sums = dict(reversed(line.split('  ', 1)) for line in (package / 'SHA256SUMS').read_text().splitlines())
        self.assertEqual(len(sums), 6)
        verify_files(package, {name: {'sha256': digest} for name, digest in sums.items()})
        manifest = read_json(package / 'run_manifest.json')
        self.assertEqual((manifest['models'], manifest['test_scored']), (['random_forest'], False))
        registered = {name: record['sha256'] for name, record in manifest['artifacts'].items()}
        self.assertEqual(registered, {name: digest for name, digest in sums.items() if name != 'run_manifest.json'})

    def test_forest_with_unrecorded_manifest_is_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            write_json(path / 'run_manifest.json', {'models': ['random_forest']})
            with patch('src.evaluation_SAS.integration.load_prediction_run',
                       side_effect=AssertionError('must not load')) as loader:
                with self.assertRaises(ValueError):
                    sas_forest(path, {}, None)
                loader.assert_not_called()

    def test_relative_mae_improvement_definition_and_zero_denominator(self):
        summary = pd.DataFrame({
            'model': ['a', 'a', 'b', 'b', 'persistence'],
            'feature_set': ['sales_only', 'stockout_aware', 'sales_only', 'stockout_aware', 'common_reference'],
            'MAE': [0.5, 0.4, 0.0, 0.1, 0.9]})
        result = relative_mae_improvement(summary)
        self.assertAlmostEqual(result['a'], 20.0)
        self.assertTrue(np.isnan(result['b']))
        self.assertNotIn('persistence', result.index)

    def test_unsafe_artifact_paths_and_original_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                verify_files(folder, {'../outside': {'sha256': '0'*64}})
            with self.assertRaises(ValueError):
                compare_development(Path(folder)/'bundle', '0'*64, Path(folder)/'original',
                                    Path(folder)/'devgru', {}, Path(folder)/'original'/'new')

    def test_final_manifest_is_rejected_before_any_outcome_loader(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            write_json(path/'bundle_manifest.json', {'purpose': 'final_experiment'})
            with patch('src.evaluation_SAS.runs.load_bundle', side_effect=AssertionError('must not load')) as loader:
                with self.assertRaises(ValueError):
                    pinned_bundle(path, sha256(path/'bundle_manifest.json'))
                loader.assert_not_called()

    def test_final_preflight_does_not_open_data_or_turn_flags_into_authorization(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root/'configs').mkdir()
            # JSON is valid YAML; even all flags true are insufficient for a final executor.
            (root/'configs/contract.yaml').write_text(json.dumps(dict.fromkeys(
                ['contract_frozen', 'initial_validation_parameters_frozen', 'new_model_test_evaluation_allowed'], True)))
            result = inspect_final_gates(root)
            self.assertFalse(result['ready_for_final_scoring'])
            self.assertFalse(result['final_data_opened'])
            self.assertIn('reviewed_final_scoring_entry_point', result['blocking_requirements'])
            self.assertIn('missing_final_settings_file', result['blocking_requirements'])


if __name__ == '__main__':
    unittest.main()
