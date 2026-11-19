"""Migration path/contract checks without importing or running legacy producers."""

import ast
import json
import subprocess
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def assignments(source):
    return {node.targets[0].id: node.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)}


def resolve_path(node, root):
    """Interpret only ROOT, string literals, and path division; never eval code."""
    if isinstance(node, ast.Name) and node.id == "ROOT":
        return root
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return resolve_path(node.left, root) / resolve_path(node.right, root)
    raise ValueError(f"Unexpected path expression: {ast.dump(node)}")


class RepositoryLayoutTests(unittest.TestCase):
    def test_working_scripts_resolve_root_and_protect_canonical_evidence(self):
        folder = ROOT / "src/data_preprocessing_DELTA"
        for name in ("prepare_and_baselines.py", "data_explore.py"):
            values = assignments((folder / name).read_text())
            self.assertEqual(ast.unparse(values["ROOT"]), "Path(__file__).resolve().parents[2]")
            self.assertEqual((folder / name).resolve().parents[2], ROOT)
        values = assignments((folder / "prepare_and_baselines.py").read_text())
        expected = {
            "INPUT": "data/raw/freshretail.csv",
            "PROCESSED": "data/processed/reproduction",
            "MANIFESTS": "data/manifests/reproduction",
            "RESULTS": "results/baselines_DELTA/reproduction",
        }
        for name, relative in expected.items():
            self.assertEqual(resolve_path(values[name], ROOT), ROOT / relative)
        downloader = assignments((folder / "data_explore.py").read_text())
        self.assertEqual(resolve_path(downloader["OUTPUT"], ROOT), ROOT / "data/raw/freshretail.csv")

    def test_working_notebook_has_isolated_outputs_and_cleared_execution(self):
        notebook = json.loads((ROOT / "notebooks/DELTA_data/prepare_and_baselines.ipynb").read_text())
        code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        for cell in code:
            self.assertEqual(cell["outputs"], [])
            self.assertIsNone(cell["execution_count"])
            ast.parse("".join(cell["source"]))
        config_source = next("".join(cell["source"]) for cell in code
                             if "DATA_PATH =" in "".join(cell["source"]))
        values = assignments(config_source)
        for name, relative in {
            "DATA_PATH": "data/raw/freshretail.csv",
            "PROCESSED_DIR": "data/processed/reproduction",
            "MANIFESTS_DIR": "data/manifests/reproduction",
            "RESULTS_DIR": "results/baselines_DELTA/reproduction",
        }.items():
            self.assertEqual(resolve_path(values[name], ROOT), ROOT / relative)
        self.assertIn("AGENTS.md", ast.unparse(values["ROOT"]))
        self.assertIn("pyproject.toml", ast.unparse(values["ROOT"]))

    def test_configuration_paths_and_owners_agree_with_workspace(self):
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["data245"]
        self.assertEqual(set(metadata["active_owners"]), {"DELTA", "DEVGRU", "SAS"})
        for name in ("requirements_file", "protocol_file", "owner_map_file"):
            self.assertTrue((ROOT / metadata[name]).is_file())
        configs = {}
        for relative in metadata["config_files"]:
            configs[Path(relative).stem] = yaml.safe_load((ROOT / relative).read_text())
        data = configs["dataset"]
        for name in ("pilot", "manifest", "exclusions", "import_manifest"):
            self.assertTrue((ROOT / data[name]).is_file(), data[name])
        self.assertEqual(data["raw"], "data/raw/freshretail.csv")
        ignored = subprocess.run(["git", "check-ignore", "--no-index", "-q", data["raw"]], cwd=ROOT)
        self.assertEqual(ignored.returncode, 0, "Raw data must stay excluded from Git")
        self.assertEqual(data["pilot_rows"], 18000)
        self.assertEqual(data["pilot_series"], 200)
        experiments = configs["experiments"]
        self.assertEqual([experiments["splits"][s]["original_rows"]
                          for s in ("train", "validation", "test")], [12000, 3000, 3000])
        self.assertIsInstance(experiments["contract_frozen"], bool)
        for model, owner in {
            "persistence": "DELTA", "recent_avg_7": "DELTA",
            "linear_regression": "DEVGRU", "ridge_regression": "DEVGRU",
            "decision_tree": "SAS", "random_forest": "SAS",
        }.items():
            self.assertEqual(configs["models"]["models"][model]["owner"], owner)
        manifest = json.loads((ROOT / data["import_manifest"]).read_text())
        for record in manifest:
            self.assertTrue((ROOT / record["current_original_destination"]).is_file())
            self.assertTrue((ROOT / record["working_destination"]).is_file())


if __name__ == "__main__":
    unittest.main()
