"""Path-adapted historical downloader by Timothy Tran; not run in migration.

A current upstream download is not the specific inherited local export.
Use the Drive acquisition instructions for an authorized reproduction.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data" / "raw" / "freshretail.csv"


def main():
    # Original source behavior retained; remote dataset access is intentional.
    splits = {"train": "data/train.parquet", "eval": "data/eval.parquet"}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("hf://datasets/Dingdong-Inc/FreshRetailNet-50K/" + splits["train"])
    df.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
