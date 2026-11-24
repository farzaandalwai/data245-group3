"""Read configuration gates only; never open final data, fit, predict or score."""
import json

import yaml

from src.evaluation_SAS.runs import ROOT


def inspect_final_gates(root=ROOT):
    registration = yaml.safe_load((root / "configs/contract.yaml").read_text())
    required = ("contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed")
    blocked = [name for name in required if registration.get(name) is not True]
    # The reviewed entry point is scripts/sas_final_evaluation.py; the legacy
    # scripts/final_evaluation.py (91fab8d) is not accepted as an entry point.
    entry_point = root / "scripts/sas_final_evaluation.py"
    if not entry_point.is_file():
        blocked.append("reviewed_final_scoring_entry_point")
    from src.evaluation_SAS.final import inspect_final_readiness
    for item in inspect_final_readiness(root)["blocking_requirements"]:
        if item not in blocked:
            blocked.append(item)
    return {"ready_for_final_scoring": not blocked, "configuration_only": True,
            "final_data_opened": False, "blocking_requirements": blocked,
            "next_action": "Run the frozen final evaluator once" if not blocked else "Resolve remaining final-scoring gates"}


def main():
    result = inspect_final_gates()
    print(json.dumps(result, indent=2))
    return 0 if result["ready_for_final_scoring"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
