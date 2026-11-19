import pandas as pd

# Login using e.g. `huggingface-cli login` to access this dataset
splits = {"train": "data/train.parquet", "eval": "data/eval.parquet"}
df = pd.read_parquet("hf://datasets/Dingdong-Inc/FreshRetailNet-50K/" + splits["train"])
df.to_csv("data/freshretail.csv", index=False)
