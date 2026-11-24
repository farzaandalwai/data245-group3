"""Reviewed SAS final entry point: `--check` reads configuration only; `run` needs every gate open.

Supersedes `scripts/final_evaluation.py` (commit 91fab8d), which is kept unchanged
as evidence for the audit of its Nov 20 run. This script never changes approval flags.
"""
import argparse
import json

from src.evaluation_SAS.final import SETTINGS_PATH, inspect_final_readiness, run_final
from src.evaluation_SAS.runs import ROOT


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Report gate status; opens no outcome data")
    check.add_argument("--bundle", help="Optional bundle directory; only its manifest header is read")
    run = sub.add_parser("run", help="Single final run with frozen settings (blocked until approved)")
    run.add_argument("--bundle", required=True)
    run.add_argument("--output", required=True, help="New directory; overwrite is refused")
    run.add_argument("--run-id", required=True)
    for command in (check, run):
        command.add_argument("--settings", default=str(SETTINGS_PATH))
    args = parser.parse_args(argv)
    if args.command == "check":
        result = inspect_final_readiness(ROOT, args.settings, ROOT / args.bundle if args.bundle else None)
        result.pop("settings")
        print(json.dumps(result, indent=2))
        return 0 if result["ready_for_final_scoring"] else 2
    manifest = run_final(ROOT / args.bundle, ROOT / args.output, args.run_id, settings_path=args.settings)
    print("Saved final run:", ROOT / args.output, manifest["models"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
