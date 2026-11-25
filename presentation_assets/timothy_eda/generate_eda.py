"""Real-export EDA only. No model imports, fitting, scoring, or network access.

Default outputs are exclusive: reruns require --output-dir pointing to a new
directory below this script's directory. Existing figures are never overwritten.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HOME = Path(__file__).resolve().parent
ROOT = HOME.parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(HOME / ".cache" / "matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from PIL import Image
import numpy as np
import pandas as pd

RAW_HASH = "6d956f6cab0094e794beb97872d9047d7c49469d35044930f5d8a96a307110b5"
DOWNLOAD = Path(r"C:\Users\timho\Downloads\data-20261124T182319Z-1-001\data")
HEADER = "city_id store_id management_group_id first_category_id second_category_id third_category_id product_id dt sale_amount hours_sale stock_hour6_22_cnt hours_stock_status discount holiday_flag activity_flag precpt avg_temperature avg_humidity avg_wind_level".split()
KEY = ["store_id", "product_id", "dt"]
SERIES = KEY[:2]
FILES = ["01_sales_vs_stockout_hours.png", "02_stockout_hours_distribution.png",
         "03_sales_by_stockout_status.png", "04_daily_stockout_prevalence.png",
         "05_dataset_validation_and_selection.png"]
C = dict(bg="#091610", panel="#10251B", forest="#24724F", teal="#79DBBB",
         orange="#F5A45D", text="#F0F5EE", muted="#B2C5B9", grid="#294333")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(maxsize=65536)
def stock_hours(text):
    text = text.strip()
    require(text.startswith("[") and text.endswith("]"), "Unbracketed hourly status")
    tokens = re.split(r"[\s,]+", text[1:-1].strip())
    require(len(tokens) == 24 and all(t in {"0", "1"} for t in tokens),
            "hours_stock_status must contain exactly 24 binary entries")
    return sum(int(t) for t in tokens[6:22])


def validate_dataset(raw):
    require(raw.is_file(), f"Original dataset not found: {raw}")
    require(sha256(raw) == RAW_HASH, "Raw SHA-256 differs from registered original; refusing substitute")
    frames = []
    for chunk in pd.read_csv(raw, chunksize=100_000, dtype="string"):
        require(list(chunk.columns) == HEADER, "Expected the registered 19-column source schema")
        require(not chunk.isna().any().any(), "Missing source values in one or more of all 19 columns")
        frame = chunk[KEY + ["sale_amount", "stock_hour6_22_cnt"]].copy()
        for column in SERIES + ["sale_amount", "stock_hour6_22_cnt"]:
            values = pd.to_numeric(frame[column], errors="raise").to_numpy(dtype=float)
            require(np.isfinite(values).all() and (values >= 0).all(), f"Invalid {column}")
            if column != "sale_amount":
                require((values % 1 == 0).all() and (values < 2**31).all(), f"Invalid integer {column}")
            frame[column] = values.astype("float64" if column == "sale_amount" else "int32")
        require(frame.stock_hour6_22_cnt.le(16).all(), "Daily stockout hours outside [0,16]")
        observed = chunk.hours_stock_status.map(stock_hours).astype("int32")
        require(np.array_equal(observed.to_numpy(), frame.stock_hour6_22_cnt.to_numpy()),
                "Stockout count does not equal binary status sum at indices [6:22]")
        frame["dt"] = pd.to_datetime(frame.dt, format="%Y-%m-%d", errors="raise")
        require(frame.dt.isin(pd.date_range("2024-03-28", periods=90)).all(), "Date outside project calendar")
        frames.append(frame)
    data = pd.concat(frames, ignore_index=True)
    require(not data.duplicated(KEY).any(), "Duplicate store-product-date records")
    counts = data.groupby(SERIES, sort=True).size()
    require(len(data) == 1_459_198 and len(counts) == 16_214, "Unexpected raw row/series counts")
    require(counts.eq(90).sum() == 16_213 and counts.eq(28).sum() == 1,
            "Unexpected complete/incomplete series counts")
    eligible = counts[counts.eq(90)].index
    return data, eligible, counts[counts.ne(90)]


def validated_cohorts(base, eligible):
    evidence = json.loads((ROOT / "docs/DELTA_V2_RUN_EVIDENCE.json").read_text())
    cohorts = {}
    identities = {}
    for name, n in [("v2-development-200-r2", 200), ("v2-final-1000-r2", 1000)]:
        directory = base / "processed/feature_bundles" / name
        manifest_path = directory / "bundle_manifest.json"
        require(manifest_path.is_file(), f"Required original cohort manifest missing: {manifest_path}")
        trusted = evidence["bundles"][name]["manifest_sha256"]
        require(sha256(manifest_path) == trusted, f"Untrusted bundle manifest: {name}")
        manifest = json.loads(manifest_path.read_text())
        sample = directory / "sample_manifest.csv"
        require(sha256(sample) == manifest["artifacts"]["sample_manifest.csv"]["sha256"], "Changed cohort sample")
        frame = pd.read_csv(sample)
        keys = set(frame[SERIES].itertuples(index=False, name=None))
        require(len(frame) == len(keys) == n and keys <= set(eligible), "Invalid cohort membership")
        cohorts[name] = keys
        identities[name] = {"bundle_manifest_sha256": trusted, "sample_manifest_sha256": sha256(sample)}
    ranked = sorted(eligible, key=lambda k: (hashlib.sha256(f"v2|245|{k[0]}|{k[1]}".encode("ascii")).hexdigest(), *k))
    require(set(ranked[:1000]) == cohorts["v2-final-1000-r2"], "Final cohort differs from documented hash ranking")
    canonical = ROOT / "archive/original_pilot/data/processed/pilot_series_manifest.csv"
    inherited = set(pd.read_csv(canonical)[SERIES].itertuples(index=False, name=None))
    require(inherited == cohorts["v2-development-200-r2"], "Development cohort differs from inherited pilot")
    return {"identities": identities, "overlap_series": len(set.intersection(*cohorts.values())),
            "development_method": "Preserved inherited 200-series manifest; original pandas sample(n=200, random_state=245)",
            "final_method": "First 1000 complete keys ranked by SHA256 of ASCII v2|245|store_id|product_id; numeric-key tie breaks"}


def summarize(data, eligible, incomplete, cohorts):
    train = data.loc[data.dt.le("2024-05-26")]
    activity = train.groupby(SERIES).agg(sales_sd=("sale_amount", "std"), stock_days=("stock_hour6_22_cnt", lambda s: int(s.gt(0).sum())))
    candidates = activity.loc[(activity.sales_sd.gt(0)) & activity.stock_days.between(1, 59)]
    candidates = [k for k in candidates.index if k in eligible]
    require(bool(candidates), "No complete, variable, mixed-availability training series")
    selected = min(candidates, key=lambda k: (hashlib.sha256(f"eda|245|{k[0]}|{k[1]}".encode("ascii")).hexdigest(), *k))
    example = data.loc[data.store_id.eq(selected[0]) & data.product_id.eq(selected[1])].sort_values("dt")
    require(len(example) == 90 and example.dt.nunique() == 90, "Illustrative series is incomplete")
    pos = data.stock_hour6_22_cnt.gt(0)
    daily = data.assign(positive=pos).groupby("dt").agg(n=("positive", "size"), positive=("positive", "sum"))
    daily["percent"] = 100 * daily.positive / daily.n
    groups = {}
    cap = float(data.sale_amount.quantile(.99))
    for name, mask in [("zero", ~pos), ("positive", pos)]:
        values = data.loc[mask, "sale_amount"].to_numpy()
        q = np.quantile(values, [0, .25, .5, .75, .99, 1])
        groups[name] = {"n": len(values), "min": q[0], "q1": q[1], "median": q[2], "q3": q[3], "p99": q[4], "max": q[5],
                        "above_pooled_p99": int((values > cap).sum())}
    result = {"purpose": "presentation_eda_only", "experiment_version": "V2 context; original-export EDA, not final-model results",
              "raw_records": len(data), "columns": 19, "raw_series": 16214, "complete_series": len(eligible),
              "incomplete": [{"store_id": int(k[0]), "product_id": int(k[1]), "rows": int(v)} for k, v in incomplete.items()],
              "date_min": str(data.dt.min().date()), "date_max": str(data.dt.max().date()), "missing_values": 0,
              "duplicate_keys": 0, "hourly_count_mismatches": 0, "positive_stockout_rows": int(pos.sum()),
              "stockout_percent": float(pos.mean() * 100), "stockout_hour_counts": data.stock_hour6_22_cnt.value_counts().sort_index().to_dict(),
              "sales_groups": groups, "pooled_sales_p99": cap,
              "daily_prevalence_min": float(daily.percent.min()), "daily_prevalence_max": float(daily.percent.max()),
              "daily_min_date": str(daily.percent.idxmin().date()), "daily_max_date": str(daily.percent.idxmax().date()),
              "daily_denominator_min": int(daily.n.min()), "daily_denominator_max": int(daily.n.max()),
              "illustrative_series": {"store_id": int(selected[0]), "product_id": int(selected[1]), "rows": len(example),
                                      "stockout_days": int(example.stock_hour6_22_cnt.gt(0).sum()),
                                      "selection_rule": "Complete raw series; train-only nonzero sales standard deviation and 1-59 positive-stockout dates in first 60 days; minimum SHA256 eda|245|store_id|product_id; no relationship/correlation or model-score filter",
                                      "eligible_example_candidates": len(candidates)}, "cohorts": cohorts}
    return result, example, daily


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16, "text.color": C["text"],
                         "axes.labelcolor": C["text"], "xtick.color": C["muted"], "ytick.color": C["muted"],
                         "axes.edgecolor": C["grid"], "axes.facecolor": C["bg"], "figure.facecolor": C["bg"],
                         "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 18,
                         "axes.labelsize": 17, "xtick.labelsize": 14, "ytick.labelsize": 14, "savefig.facecolor": C["bg"]})


def canvas(number, title, subtitle):
    fig = plt.figure(figsize=(16, 9), dpi=160)
    fig.text(.075, .953, f"DATA 245  /  DELTA     •     ORIGINAL-EXPORT EDA     /     {number:02d}", fontsize=12, color=C["teal"], weight="bold")
    fig.text(.075, .895, title, fontsize=29, weight="bold")
    fig.text(.075, .849, subtitle, fontsize=15, color=C["muted"])
    return fig


def footer(fig, text, note="Population: original export • 1,459,198 records • Mar 28–Jun 25, 2024 • EDA only"):
    fig.text(.075, .10, text, fontsize=13, color=C["text"], linespacing=1.55)
    fig.text(.075, .035, note, fontsize=10.5, color=C["muted"])


def axes_style(ax):
    ax.grid(axis="y", color=C["grid"], linewidth=.7, alpha=.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=10)


def figure_one(example, s):
    k = s["illustrative_series"]
    fig = canvas(1, "Sales and stockout hours in one real series", f"Store {k['store_id']}  •  Product {k['product_id']}  •  March 28–June 25, 2024  •  90 complete daily records")
    ax = fig.add_axes([.09, .475, .82, .30]); bx = fig.add_axes([.09, .235, .82, .17], sharex=ax)
    ax.plot(example.dt, example.sale_amount, color=C["teal"], lw=2.5, marker="o", ms=2.7)
    ax.set_ylabel("Recorded sales\n(normalized)", labelpad=17); ax.set_ylim(bottom=0)
    bx.bar(example.dt, example.stock_hour6_22_cnt, color=C["orange"], width=.8)
    bx.set_ylabel("Annotated\nstockout hours", labelpad=17); bx.set_ylim(0, 17); bx.set_yticks([0, 8, 16])
    bx.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2)); bx.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.tick_params(labelbottom=False); ax.margins(x=.01)
    for a in [ax, bx]: axes_style(a)
    footer(fig, "Availability can constrain recorded sales; this paired timeline does not establish causation.\nDeterministic example selected using training-period eligibility, then hash rank—not association strength.",
           "Population: one illustrative raw-export series, not a representative sample • Same-day stockout labels are descriptive only")
    return fig


def figure_two(data, s):
    fig = canvas(2, "Recorded stockout hours range from 0 to 16", "Daily count of hours marked stockout during 06:00–22:00; integer values from 0 to 16")
    counts = pd.Series({int(k): v for k, v in s["stockout_hour_counts"].items()}).reindex(range(17), fill_value=0)
    for x, label, lo, hi in [(.09, "ZERO HOURS", 0, 0), (.35, "1–4 HOURS", 1, 4), (.60, "5–16 HOURS", 5, 16)]:
        pct = counts.loc[lo:hi].sum() / s["raw_records"] * 100
        fig.text(x, .77, f"{pct:.1f}%", fontsize=25, weight="bold", color=C["teal"] if lo == 0 else C["orange"])
        fig.text(x, .733, label, fontsize=11, color=C["muted"])
    ax = fig.add_axes([.09, .245, .82, .43]); ax.bar(counts.index, counts / s["raw_records"] * 100, color=[C["teal"]] + [C["orange"]] * 16, width=.76)
    ax.set_xticks(range(17)); ax.set_xlabel("Annotated stockout hours in the daily 16-hour interval", labelpad=12)
    ax.set_ylabel("Share of source records (%)", labelpad=14); axes_style(ax)
    footer(fig, "Zero means no annotated stockout in this interval; it does not prove unrestricted availability.\nThe 24-entry binary status vector reconciles with the daily count for every record.")
    return fig


def box_stats(values, label, full=False):
    q1, median, q3 = np.quantile(values, [.25, .5, .75]); iqr = q3 - q1
    return dict(label=label, q1=q1, med=median, q3=q3,
                whislo=values.min() if full else values[values >= q1 - 1.5 * iqr].min(),
                whishi=values.max() if full else values[values <= q3 + 1.5 * iqr].max(), fliers=[])


def figure_three(data, s):
    fig = canvas(3, "Recorded sales differ by annotated availability", "Descriptive comparison of source records; group differences do not identify a causal stockout effect")
    positive = data.stock_hour6_22_cnt.gt(0)
    vals = [data.loc[~positive, "sale_amount"].to_numpy(), data.loc[positive, "sale_amount"].to_numpy()]
    labels = [f"Zero annotated hours\nn = {len(vals[0]):,}", f"Positive annotated hours\nn = {len(vals[1]):,}"]
    left = fig.add_axes([.09, .29, .47, .445]); right = fig.add_axes([.68, .29, .23, .445])
    for ax, full in [(left, False), (right, True)]:
        artists = ax.bxp([box_stats(v, label, full) for v, label in zip(vals, labels)], patch_artist=True,
                         showfliers=False, widths=.48, medianprops={"color": C["text"], "linewidth": 2.4},
                         whiskerprops={"color": C["muted"], "linewidth": 1.4}, capprops={"color": C["muted"]})
        for patch, color in zip(artists["boxes"], [C["teal"], C["orange"]]): patch.set(facecolor=color, alpha=.65, edgecolor=color)
        axes_style(ax)
    left.set_ylim(0, s["pooled_sales_p99"]); left.set_ylabel("Recorded sales (normalized)", labelpad=16)
    left.set_title("Detail: up to pooled 99th percentile", loc="left", pad=20, color=C["text"], fontsize=17)
    right.set_yscale("symlog", linthresh=1); right.set_ylim(0, max(v.max() for v in vals) * 1.3)
    right.set_title("Full range: symlog scale", loc="left", pad=20, color=C["text"], fontsize=17)
    right.set_ylabel("Recorded sales (normalized)", labelpad=12); right.set_xticklabels(["Zero hours", "Positive hours"], fontsize=12)
    for i, v in enumerate(vals, 1): right.annotate(f"max {v.max():.2f}", (i, v.max()), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=12)
    n = sum(g["above_pooled_p99"] for g in s["sales_groups"].values())
    footer(fig, f"Detail axis ends at {s['pooled_sales_p99']:.3f}; {n:,} higher records remain in all statistics and the full-range view.\nBoxes: Q1–Q3 with median. Left whiskers: 1.5×IQR; right whiskers: actual minimum–maximum.")
    return fig


def figure_four(daily, s):
    fig = canvas(4, "Stockout prevalence varies across the calendar", "Share of all source store-product records with positive annotated stockout hours, calculated separately each date")
    ax = fig.add_axes([.09, .25, .82, .50])
    ax.plot(daily.index, daily.percent, color=C["orange"], lw=2.8)
    ax.fill_between(daily.index, 0, daily.percent.to_numpy(), color=C["orange"], alpha=.10)
    ax.axhline(s["stockout_percent"], color=C["teal"], linestyle=(0, (5, 4)), lw=1.7, label=f"All-record share: {s['stockout_percent']:.1f}%")
    ax.set_ylim(0, min(100, np.ceil(daily.percent.max() / 10) * 10 + 10))
    ax.set_ylabel("Records with stockout hours (%)", labelpad=16); ax.set_xlabel("Calendar date", labelpad=12)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    axes_style(ax); ax.legend(frameon=False, labelcolor=C["text"], fontsize=14, loc="lower left")
    ax.margins(x=.01)
    footer(fig, f"Daily share ranges from {s['daily_prevalence_min']:.1f}% to {s['daily_prevalence_max']:.1f}%; no causal explanation or fitted trend is implied.\nEach date uses its observed denominator ({s['daily_denominator_min']:,}–{s['daily_denominator_max']:,} records); incomplete-series records remain included.")
    return fig


def figure_five(s):
    fig = canvas(5, "One eligible population, two separate cohorts", "Validation and cohort selection follow the preserved DELTA data contract; development is not a required subset of final")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for x, value, label in [(.075, "1,459,198", "SOURCE RECORDS"), (.37, "0", "MISSING SOURCE VALUES"), (.685, "0", "DUPLICATE DATE KEYS")]:
        ax.text(x, .767, value, fontsize=24, weight="bold", color=C["teal"])
        ax.text(x, .729, label, fontsize=11, color=C["muted"])
    def box(x, y, w, h, number, label, detail, color=C["teal"]):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.012", facecolor=C["panel"], edgecolor=C["grid"], linewidth=1.2))
        ax.text(x + .017, y + h - .058, number, fontsize=27, weight="bold", color=color)
        ax.text(x + .017, y + h - .098, label, fontsize=14, weight="bold")
        ax.text(x + .017, y + .022, detail, fontsize=11.5, color=C["muted"], linespacing=1.45)
    box(.075, .443, .217, .227, "16,214", "Raw series", "Store–product keys\n90-day source calendar")
    box(.377, .443, .217, .227, "16,213", "Complete series", "All 90 dates present\nRetrospective eligibility")
    box(.715, .530, .205, .180, "200", "Development", "Preserved inherited pilot\nOriginal random_state=245", C["teal"])
    box(.715, .315, .205, .180, "1,000", "Final", "SHA-256 key ranking\nSeed 245; first 1,000", C["orange"])
    for start, end in [((.302, .557), (.36, .557)), ((.604, .57), (.698, .635)), ((.604, .54), (.698, .41))]:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, color=C["muted"], linewidth=1.7))
    ax.text(.334, .352, "1 incomplete series excluded\n28 dates present; 62 absent", ha="center", fontsize=12.5, color=C["orange"], linespacing=1.55)
    ax.text(.075, .262, "CHRONOLOGICAL DESIGN  /  TARGETS START ON DAY 15", fontsize=11, color=C["muted"], weight="bold")
    x = .075
    for n, label, color in [(14, "14 warmup", C["grid"]), (46, "46 train targets", C["forest"]), (15, "15 validation", "#346C61"), (15, "15 test", "#775536")]:
        w = .845 * n / 90
        ax.add_patch(Rectangle((x, .195), w - .003, .043, facecolor=color)); ax.text(x + w / 2, .216, label, ha="center", va="center", fontsize=11.5); x += w
    footer(fig, "Cohorts are selected separately from the same eligible population; overlap is not a nesting rule.\nFull-horizon completeness uses future availability of records and is disclosed as retrospective selection.",
           "Counts above: raw export and complete-series population • Cohorts: preserved V2 r2 manifests • No experiment executed")
    return fig


def save_exclusive(fig, path):
    # Render-boundary check catches clipped titles, captions, tick labels, legends.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    width, height = fig.canvas.get_width_height()
    for text in fig.findobj(matplotlib.text.Text):
        if text.get_visible() and text.get_text():
            b = text.get_window_extent(renderer)
            require(b.x0 >= -2 and b.y0 >= -2 and b.x1 <= width + 2 and b.y1 <= height + 2,
                    f"Clipped text in {path.name}: {text.get_text()!r}")
    with path.open("xb") as f:
        fig.savefig(f, format="png", dpi=160, metadata={"Title": path.stem, "Description": "V2 context; original-export descriptive EDA only; no model scoring"})
    plt.close(fig)
    with Image.open(path) as im:
        require(im.size == (2560, 1440), f"Unexpected image resolution: {im.size}")


def write_readme(out, s, raw):
    k = s["illustrative_series"]; g = s["sales_groups"]
    text = f"""# Timothy / DELTA presentation EDA

Purpose: **original-export descriptive EDA only**, in the V2 project context.
These figures are not final-model results and do not change the November 24 experiment.

## Inputs and integrity

- Exact source: `{raw}` (read only).
- SHA-256: `{RAW_HASH}`; 323,577,557 bytes. Identity checked before and after analysis.
- Original export: **1,459,198 rows, 19 columns, 16,214 store-product series**, March 28–June 25, 2024.
- **16,213 complete 90-day series**, one 28-day series (store {s['incomplete'][0]['store_id']}, product {s['incomplete'][0]['product_id']}) with 62 absent dates.
- All 19 source columns checked: **zero missing values**. **Zero duplicate store-product-date keys**.
- Every 24-entry binary `hours_stock_status` vector reconciles with `stock_hour6_22_cnt` at indices [6:22].
- Count means annotated stockout hours in [06:00,22:00), with 1=stockout. Zero annotations do not prove unrestricted availability. Scaling coefficient, original export lineage and undocumented closed/missing-hour semantics remain provisional.
- Raw Figures 2–4 retain the 28 valid records of the incomplete series. They are not restricted to development or final samples.

## 01 — Sales versus stockout hours

`01_sales_vs_stockout_hours.png`: 90 real daily observations for store **{k['store_id']}**, product **{k['product_id']}**, March 28–June 25, 2024. Teal sales and orange annotated stockout hours use aligned panels with independent, explicit units.

Selection: consider complete series only; on the first 60 training dates require nonzero sales standard deviation and 1–59 positive-stockout dates. Rank the {k['eligible_example_candidates']:,} qualifying series by SHA-256 of ASCII `eda|245|store_id|product_id`, break ties by numeric keys, choose the minimum. No sales-stockout correlation, apparent relationship, validation/test outcome or model score selects the example. The displayed full calendar includes validation/test dates for descriptive illustration, not tuning. There are **{k['stockout_days']} positive-stockout dates** in this example.

Presentation: “This is one deterministically selected, complete store-product timeline. Stockout annotations help motivate historical availability features, but this plot does not establish why sales changed.”

Limitation: illustrative, not representative; association cannot establish constrained latent demand or causality. Same-day annotations shown here are not approved model predictors.

## 02 — Distribution of stockout hours

`02_stockout_hours_distribution.png`: integer-centered histogram of daily annotated stockout hours, all 1,459,198 source rows. Vertical axis is percent of source records; all bins 0–16 are retained. **{s['positive_stockout_rows']:,} records ({s['stockout_percent']:.4f}%)** have positive annotated hours.

Presentation: “Recorded stockout annotations occur on {s['stockout_percent']:.1f}% of source records. The bars distinguish days with no annotated hours from short and longer annotated periods.”

Limitation: annotations describe the 16-hour operational interval, not exact unmet demand or independently verified business closures.

## 03 — Sales by availability annotation

`03_sales_by_stockout_status.png`: same all-export population, partitioned by zero versus positive annotated hours. Group sizes are **{g['zero']['n']:,}** and **{g['positive']['n']:,}**; medians are **{g['zero']['median']:.6f}** and **{g['positive']['median']:.6f}** normalized sales, respectively.

Detail uses the pooled sales 99th percentile (**{s['pooled_sales_p99']:.6f}**) as its axis limit; **{sum(v['above_pooled_p99'] for v in g.values()):,}** larger values remain in every statistic and in the adjacent full-range view. Detail boxes use Q1/median/Q3, whiskers end at observed values within 1.5 IQR, and individual outlier dots are suppressed. Full-range boxes show observed min/max whiskers and all-data quartiles, on a symmetric-log axis that is linear through sales=1 and logarithmic above it. No values are deleted or winsorized. Original maxima: zero group **{g['zero']['max']:.6f}**, positive group **{g['positive']['max']:.6f}**.

Presentation: “The two annotation groups have different recorded-sales distributions. This pooled comparison mixes stores, products and dates, so it is descriptive rather than a causal stockout effect.”

## 04 — Daily stockout prevalence

`04_daily_stockout_prevalence.png`: for each of 90 dates, 100 × number of source rows with positive hours / all rows on that date. Denominators vary from **{s['daily_denominator_min']:,} to {s['daily_denominator_max']:,}** because the incomplete series remains included where observed. Daily prevalence ranges from **{s['daily_prevalence_min']:.4f}% ({s['daily_min_date']})** to **{s['daily_prevalence_max']:.4f}% ({s['daily_max_date']})**. Dashed reference is the row-weighted all-export prevalence, not a model prediction or fitted trend.

Presentation: “The share with recorded stockout hours changes over the 90-day calendar, between {s['daily_prevalence_min']:.1f}% and {s['daily_prevalence_max']:.1f}%. The chart documents that variation without attributing it to a particular cause.”

Limitation: daily pooled percentages do not track a guaranteed constant set of all raw series and do not control for common calendar effects.

## 05 — Validation and separate cohort selection

`05_dataset_validation_and_selection.png`: raw 16,214 series → 16,213 eligible complete series → **separate branches** to 200 development and 1,000 final. One incomplete 28-day series is excluded from complete-series eligibility; there is no exclusion solely for stockout status.

- Development: preserve the inherited canonical 200-series manifest. Historical source uses pandas `sample(n=200, random_state=245)` on complete series; this task verifies manifest identity rather than silently reselection under another environment.
- Final: SHA-256 rank of ASCII `v2|245|integer_store|integer_product`, ascending digest then numeric keys, first 1,000. Membership independently checked against the preserved final r2 manifest.
- Actual cohort overlap: **{s['cohorts']['overlap_series']} series**; membership is not guaranteed nested or disjoint.
- Split strip: first 14 days warm up history; retained targets give 46 train / 15 validation / 15 test dates per series. This corresponds to final **46,000 / 15,000 / 15,000** rows, distinct from raw-export EDA counts. No target rows or model predictions were regenerated.

Presentation: “We excluded one incomplete series, then used the preserved development cohort and a separately hash-ranked final cohort. Both follow the same chronological design and past-only feature contract.”

Limitation: eligibility based on all 90 dates is retrospective availability selection; neither cohort is claimed representative of the full dataset or wider retail population.

## Reproduce without overwriting

Interpreter used: `{sys.executable}`. Exact installed packages are in `requirements-eda-freeze.txt`.

```powershell
& '{sys.executable}' -B '{HOME / 'generate_eda.py'}' --input '{raw}' --data-root '{raw.parent.parent}' --output-dir '{HOME / 'regenerated_01'}'
```

The requested output folder must remain below `presentation_assets/timothy_eda`. The script refuses existing PNGs, README or summary; select a new child directory for a fresh rendering. No hidden download, model import, training, tuning or scoring occurs. Caches and the dedicated environment stay under this presentation-assets directory.

## Files and QA

Five 2560 × 1440 PNGs (16:9), `generate_eda.py`, this README, `eda_summary.json`, `requirements-eda-freeze.txt`, saved task request and workspace preservation evidence. JSON contains exact plotted summaries, input identities, selection rule, cohort hashes and figure hashes. Rendering verifies resolution and all text boundaries; separate visual review is recorded in `qa_report.json`.

Recommended two slides: **01** for feature-engineering motivation and **05** for DELTA validation/cohort/chronology responsibilities. No model-performance or sustainability outcome is inferred.
"""
    with (out / "README.md").open("x", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=HOME)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    require(out == HOME or HOME in out.parents, "Outputs must stay below presentation_assets/timothy_eda")
    out.mkdir(parents=True, exist_ok=True)
    for name in FILES + ["README.md", "eda_summary.json"]:
        require(not (out / name).exists(), f"Refusing overwrite: {out / name}; use a new --output-dir")
    candidates = [ROOT / "data/raw/freshretail.csv", DOWNLOAD / "raw/freshretail.csv"]
    raw = args.input.resolve() if args.input else next((p for p in candidates if p.is_file()), candidates[0])
    base = args.data_root.resolve() if args.data_root else raw.parent.parent
    print(f"Validating original export: {raw}", flush=True)
    data, eligible, incomplete = validate_dataset(raw)
    print("Raw validation passed; checking preserved cohort identities", flush=True)
    cohorts = validated_cohorts(base, eligible)
    stats, example, daily = summarize(data, eligible, incomplete, cohorts)
    stats.update({"source_path": str(raw), "source_sha256": RAW_HASH, "source_bytes": raw.stat().st_size,
                  "interpreter": sys.executable, "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__},
                  "source_code_sha256": sha256(Path(__file__))})
    style()
    producers = [lambda: figure_one(example, stats), lambda: figure_two(data, stats), lambda: figure_three(data, stats),
                 lambda: figure_four(daily, stats), lambda: figure_five(stats)]
    for name, produce in zip(FILES, producers):
        save_exclusive(produce(), out / name)
        print(f"Saved {name} (2560 x 1440)", flush=True)
    require(sha256(raw) == RAW_HASH, "Original dataset changed during analysis")
    stats["figures"] = {name: {"sha256": sha256(out / name), "pixels": [2560, 1440]} for name in FILES}
    with (out / "eda_summary.json").open("x", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    write_readme(out, stats, raw)
    print(json.dumps({"status": "PASS", "output": str(out), "example": stats["illustrative_series"], "stockout_percent": stats["stockout_percent"]}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError) as error:
        raise SystemExit(f"EDA validation failed: {error}") from error
