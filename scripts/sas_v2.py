"""Local SAS consumers: python -m scripts.sas_v2 --help (no publication)."""
import argparse

from src.evaluation_SAS.runs import ROOT, evaluate_runs, train_tree_run
from src.evaluation_SAS.v2 import BASELINES, LEARNED_MODELS


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("train-tree", "evaluate"):
        command = sub.add_parser(name)
        command.add_argument("--bundle", required=True)
        command.add_argument("--manifest-sha256", required=True,
                             help="Trusted hash from DELTA's handoff, not an untrusted incoming file")
        command.add_argument("--run-id", required=True)
        if name == "train-tree":
            command.add_argument("--policy", default="src/models/decision_tree_SAS/development_policy.json")
        else:
            command.add_argument("--run", action="append", required=True,
                                 help="Prediction-run directory; repeat for each producer")
            command.add_argument("--models", nargs="+", required=True, choices=BASELINES + LEARNED_MODELS)
            command.add_argument("--splits", nargs="+", default=["validation"], choices=["train", "validation"])
    args = parser.parse_args(argv)
    if args.command == "train-tree":
        from src.evaluation_SAS.runs import checked_id
        checked_id(args.run_id)
        destination = ROOT / "results/decision_tree_SAS/v2" / args.run_id
        manifest = train_tree_run(ROOT / args.bundle, args.manifest_sha256, destination,
                                  args.run_id, ROOT / args.policy)
    else:
        from src.evaluation_SAS.runs import checked_id
        checked_id(args.run_id)
        destination = ROOT / "results/comparisons_SAS/v2" / args.run_id
        manifest = evaluate_runs(ROOT / args.bundle, args.manifest_sha256,
                                 [ROOT / path for path in args.run], destination,
                                 args.run_id, args.models, args.splits)
    print(f"Saved local {manifest['evidence_status']} run: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
