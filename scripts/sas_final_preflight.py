"""Read configuration gates only; never open final data, fit, predict or score."""
import json

import yaml

from src.evaluation_SAS.runs import ROOT


def inspect_final_gates(root=ROOT):
    registration = yaml.safe_load((root / "configs/contract.yaml").read_text())
    required = ("contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed")
    blocked = [name for name in required if registration.get(name) is not True]
    entry_point = root / "scripts/final_evaluation.py"
    if not entry_point.is_file():
        blocked.append("reviewed_final_scoring_entry_point_and_validation_freeze_record")
    return {"ready_for_final_scoring": not blocked, "configuration_only": True,
            "final_data_opened": False, "blocking_requirements": blocked,
            "next_action": "Run the frozen final evaluator once" if not blocked else "Resolve remaining final-scoring gates"}


def main():
    result = inspect_final_gates()
    print(json.dumps(result, indent=2))
    return 0 if result["ready_for_final_scoring"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
