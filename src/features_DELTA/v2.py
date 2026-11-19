"""Shared prior-only features adapted from OLD/src/build_features.py.

Legacy grouped shifts/rolling formulas retained; stockout target exclusion removed.
"""
import numpy as np
import pandas as pd

from src.data_preprocessing_DELTA.v2 import KEY, SERIES, CALENDAR, complete_series

COMMON = [f"sales_lag_{n}" for n in (1, 2, 3, 7, 14)] + ["sales_mean_7", "sales_mean_14", "weekday", "is_weekend"]
EXTRA = ["stockout_hours_lag_1", "stockout_hours_mean_7", "stockout_hours_mean_14", "stockout_day_fraction_7", "stockout_day_fraction_14"]


def build_features(frame):
    """Consume validated complete series. Return keyed tables without side effects."""
    frame = frame.sort_values(KEY).reset_index(drop=True)
    _, excluded = complete_series(frame)
    if len(excluded) or frame.empty:
        raise ValueError("Feature generation needs complete nonempty series")
    groups = frame.groupby(SERIES, sort=False)
    out = frame[KEY].copy()
    for lag in (1, 2, 3, 7, 14):
        out[f"sales_lag_{lag}"] = groups.sale_amount.shift(lag)
    for window in (7, 14):
        out[f"sales_mean_{window}"] = groups.sale_amount.transform(lambda s: s.shift(1).rolling(window).mean())
        out[f"stockout_hours_mean_{window}"] = groups.stock_hour6_22_cnt.transform(lambda s: s.shift(1).rolling(window).mean())
        out[f"stockout_day_fraction_{window}"] = groups.stock_hour6_22_cnt.transform(lambda s: s.gt(0).shift(1).rolling(window).mean())
    out["stockout_hours_lag_1"] = groups.stock_hour6_22_cnt.shift(1)
    out["weekday"] = frame.dt.dt.day_of_week.astype("int64")
    out["is_weekend"] = out.weekday.ge(5).astype("int64")
    day = (frame.dt - CALENDAR[0]).dt.days + 1
    splits = np.select([day <= 60, day <= 75], ["train", "validation"], default="test")
    keep = day.ge(15)
    obs = frame.loc[keep, KEY + ["sale_amount"]].rename(columns={"sale_amount": "actual"})
    obs["split"] = splits[keep]
    metadata = frame.loc[keep, KEY].copy()
    metadata["target_stockout_hours"] = frame.loc[keep, "stock_hour6_22_cnt"]
    metadata["target_stockout_group"] = np.where(metadata.target_stockout_hours.eq(0), "fully_stocked", "stockout")
    tables = {"observations": obs, "features_sales_only": out.loc[keep, KEY + COMMON],
              "features_stockout_aware": out.loc[keep, KEY + COMMON + EXTRA], "evaluation_metadata": metadata}
    if not np.isfinite(out.loc[keep, COMMON + EXTRA].to_numpy()).all():
        raise ValueError("Nonfinite retained predictors")
    for name, table in tables.items():
        table = table.reset_index(drop=True)
        table["dt"] = table.dt.dt.strftime("%Y-%m-%d")
        tables[name] = table
    audit = []
    for split in ("train", "validation", "test"):
        candidate = splits == split
        audit.append({"split": split, "source_rows": int(candidate.sum()),
                      "warmup_exclusions": int((candidate & ~keep).sum()), "quality_exclusions": 0,
                      "target_stockout_exclusions": 0, "retained_targets": int((candidate & keep).sum())})
    tables["eligibility_audit"] = pd.DataFrame(audit)
    return tables


def reconstruct(frame, tables):
    """Independent NumPy slices reconstruct EVERY predictor, actual and split."""
    expected = []
    for (store, product), group in frame.groupby(SERIES, sort=True):
        group = group.sort_values("dt")
        sales = group.sale_amount.to_numpy()
        hours = group.stock_hour6_22_cnt.to_numpy()
        for i in range(14, 90):
            dt = group.dt.iloc[i]
            row = [sales[i-k] for k in (1,2,3,7,14)]
            row += [np.mean(sales[i-7:i]), np.mean(sales[i-14:i]), dt.day_of_week, int(dt.day_of_week >= 5)]
            row += [hours[i-1], np.mean(hours[i-7:i]), np.mean(hours[i-14:i]), np.mean(hours[i-7:i]>0), np.mean(hours[i-14:i]>0)]
            expected.append([store, product, dt.strftime("%Y-%m-%d"), sales[i], "train" if i<60 else "validation" if i<75 else "test", *row])
    golden = pd.DataFrame(expected, columns=KEY+["actual","split"]+COMMON+EXTRA)
    pd.testing.assert_frame_equal(golden[KEY+["actual","split"]], tables["observations"], check_dtype=False)
    for condition, names in (("sales_only",COMMON),("stockout_aware",COMMON+EXTRA)):
        pd.testing.assert_frame_equal(golden[KEY], tables[f"features_{condition}"][KEY])
        np.testing.assert_allclose(golden[names], tables[f"features_{condition}"][names], rtol=1e-12, atol=1e-12)
    return {"independent_reconstruction_rows": len(golden), "independent_predictor_values": len(golden)*14}
