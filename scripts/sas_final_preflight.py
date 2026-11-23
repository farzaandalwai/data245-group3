"""Read configuration gates only; never open final data, fit, predict or score."""
import json

import yaml

from src.evaluation_SAS.runs import ROOT


def inspect_final_gates(root=ROOT):
    registration = yaml.safe_load((root / "configs/contract.yaml").read_text())
    required = ("contract_frozen", "initial_validation_parameters_frozen", "new_model_test_evaluation_allowed")
    blocked = [name for name in required if registration.get(name) is not True]
    # No final executor has been reviewed/implemented by this development task.
    blocked.append("reviewed_final_scoring_entry_point_and_validation_freeze_record")
    return {"ready_for_final_scoring": False, "configuration_only": True,
            "final_data_opened": False, "blocking_requirements": blocked,
            "next_action": "Resolve documented decisions and review a final workflow; development commands reject final inputs"}


def main():
    print(json.dumps(inspect_final_gates(), indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
