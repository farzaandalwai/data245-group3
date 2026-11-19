"""V2 pure validation/selection; adapts Timothy Tran's legacy preparation logic."""
from functools import lru_cache
import hashlib

import numpy as np
import pandas as pd

from scripts.audit_contract import parse_stock_status, business_stockout_hours

SERIES = ["store_id", "product_id"]
KEY = SERIES + ["dt"]
REQUIRED = KEY + ["sale_amount", "stock_hour6_22_cnt", "hours_stock_status"]
CALENDAR = pd.date_range("2024-03-28", periods=90)


@lru_cache(maxsize=65536)
def hourly_count(text):
    return business_stockout_hours(parse_stock_status(text))


def validate_records(frame):
    """Reject invalid records; incomplete but otherwise valid series are separate."""
    missing = set(REQUIRED) - set(frame)
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")
    out = frame[REQUIRED].copy()
    if out.isna().any().any():
        raise ValueError("Null required field/key")
    for name in SERIES + ["sale_amount", "stock_hour6_22_cnt"]:
        if out[name].map(lambda x: isinstance(x, (bool, np.bool_))).any():
            raise ValueError(f"Boolean is not a valid numeric value: {name}")
        values = pd.to_numeric(out[name], errors="raise")
        if values.dtype == object:
            raise ValueError(f"Numeric value outside supported range: {name}")
        if not np.isfinite(values).all() or (values < 0).any():
            raise ValueError(f"Nonfinite or negative {name}")
        if name != "sale_amount":
            if (values % 1 != 0).any() or (values >= 2**63).any():
                raise ValueError(f"Expected bounded integer {name}")
            values = values.astype("int64")
        out[name] = values
    if out.stock_hour6_22_cnt.gt(16).any():
        raise ValueError("Stockout count outside [0,16]")
    out["dt"] = pd.to_datetime(out.dt, format="%Y-%m-%d", errors="raise")
    if not out.dt.isin(CALENDAR).all():
        raise ValueError("Dates outside approved exact 90-day calendar")
    if out.duplicated(KEY).any():
        raise ValueError("Duplicate store-product-date keys")
    try:
        counts = out.hours_stock_status.map(hourly_count)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Invalid 24-entry binary hours_stock_status") from exc
    if not counts.eq(out.stock_hour6_22_cnt).all():
        raise ValueError("Hourly vector/count disagreement for indices [6:22]")
    return out.sort_values(KEY, kind="stable").reset_index(drop=True)


def complete_series(frame):
    """Input must be validated: unique dates within the exact 90-date calendar."""
    sizes = frame.groupby(SERIES, sort=True).size().rename("row_count").reset_index()
    excluded = sizes.loc[sizes.row_count.ne(90)].copy()
    excluded["reason"] = "incomplete_90_day_calendar"
    excluded["missing_days"] = 90 - excluded.row_count
    return sizes.loc[sizes.row_count.eq(90), SERIES].reset_index(drop=True), excluded


def select_sample(frame, count=1000, seed=245):
    """Seeded SHA-256 rank of normalized integer keys; no outcome-derived strata.

    Stable across Python/NumPy versions and input ordering. Uniform hash ranking
    avoids small store/product cross-strata. Full calendar eligibility is retrospective.
    """
    eligible, _ = complete_series(frame)
    if isinstance(count, bool) or not isinstance(count, int) or not 0 < count <= len(eligible):
        raise ValueError("Sample size outside eligible population")
    eligible["selection_rank"] = [
        hashlib.sha256(f"v2|{seed}|{s}|{p}".encode("ascii")).hexdigest()
        for s, p in eligible[SERIES].itertuples(index=False, name=None)
    ]
    return eligible.sort_values(["selection_rank", *SERIES]).head(count).sort_values(SERIES).reset_index(drop=True)


def subset(frame, manifest):
    if manifest[SERIES].isna().any().any() or manifest.duplicated(SERIES).any():
        raise ValueError("Invalid/duplicate manifest keys")
    out = frame.merge(manifest[SERIES], on=SERIES, how="inner", validate="many_to_one")
    eligible, excluded = complete_series(out)
    if len(eligible) != len(manifest) or len(excluded):
        raise ValueError("Selected series absent or incomplete")
    return out.sort_values(KEY).reset_index(drop=True)


def coverage(frame, population):
    train = frame.loc[frame.dt <= CALENDAR[59]]
    activity = train.assign(positive=train.stock_hour6_22_cnt.gt(0)).groupby(SERIES).positive.mean()
    return {"series": int(len(activity)), "stores": int(frame.store_id.nunique()),
            "products": int(frame.product_id.nunique()), "eligible_population_series": int(population),
            "series_fraction": len(activity) / population,
            "training_stockout_day_fraction_quantiles": {str(k): float(v) for k, v in activity.quantile([0,.25,.5,.75,1]).items()},
            "training_series_without_stockout": int(activity.eq(0).sum())}
