"""Validate original SAS/PR6 artifacts and write a separate DEVELOPMENT evaluation."""
import argparse
from pathlib import Path

from src.evaluation_SAS.integration import compare_development, devgru_originals, sas_forest, sas_originals
from src.evaluation_SAS.runs import ROOT, pinned_bundle, read_json

DEFAULT_PIN = "docs/SAS_DEVGRU_PR6_PIN.json"
SAS_ORIGINALS = "artifacts/SAS/development/original-200-series-20261119"
SAS_FOREST = "artifacts/SAS/development/random-forest-200-series-20261120"
BUNDLE_HASH = "043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["verify", "compare"])
    parser.add_argument("--bundle", default="data/processed/feature_bundles/v2-development-200-r2")
    parser.add_argument("--bundle-sha256", default=BUNDLE_HASH)
    parser.add_argument("--sas-originals", default=SAS_ORIGINALS)
    parser.add_argument("--pin", default=DEFAULT_PIN)
    parser.add_argument("--sas-forest", default=SAS_FOREST,
                        help="Shared Random Forest run; pass an empty string to omit it (reproduces r3 scope)")
    parser.add_argument("--devgru-root", help="PR6 package path in an isolated checkout; defaults to merged package path")
    parser.add_argument("--output", help="New separate output directory; overwrite is rejected")
    args = parser.parse_args(argv)
    pin = read_json(ROOT / args.pin)
    devgru = ROOT / args.devgru_root if args.devgru_root else ROOT / pin["package_path"]
    if args.command == "verify":
        tables, _, identity = pinned_bundle(ROOT / args.bundle, args.bundle_sha256)
        _, sas = sas_originals(ROOT / args.sas_originals, identity, tables["observations"],
                               read_json(ROOT / "docs/SAS_INTEGRATION_EVIDENCE.json"))
        _, audit = devgru_originals(devgru, pin, identity, tables["observations"])
        if args.sas_forest:
            sas_forest(ROOT / args.sas_forest, identity, tables["observations"])
        print(f"DEVELOPMENT acceptance: SAS {len(sas['files'])} original files; DEVGRU four prediction files; "
              f"{'forest run; ' if args.sas_forest else ''}exact keys/actuals/splits")
        for finding in audit["original_inventory_discrepancies"]:
            print("PROVENANCE WARNING: PR6 original inventory disagrees with published Git bytes:", finding["file"])
    else:
        if not args.output:
            parser.error("compare requires --output (a new directory)")
        manifest = compare_development(ROOT / args.bundle, args.bundle_sha256, ROOT / args.sas_originals,
                                       devgru, pin, ROOT / args.output,
                                       ROOT / args.sas_forest if args.sas_forest else None)
        print("Saved DEVELOPMENT validation comparison:", ROOT / args.output, manifest["models"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
