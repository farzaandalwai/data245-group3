"""Export labeled development figures; no fitting or data selection."""
import os
from pathlib import Path
import tempfile


def development_figures(summary, intervals, destination):
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "data245-mpl-cache"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    destination = Path(destination)
    names = {"linear_regression": "Linear", "ridge_regression": "Ridge", "decision_tree": "Decision Tree",
             "persistence": "Persistence", "recent_avg_7": "7-day mean"}
    colors = {"sales_only": "#777777", "stockout_aware": "#236b8e", "common_reference": "#333333"}
    ordered = summary.sort_values(["model", "feature_set"]).reset_index(drop=True)
    labels = [names[r.model] + (" · sales" if r.feature_set == "sales_only" else " · + stockout" if r.feature_set == "stockout_aware" else "")
              for r in ordered.itertuples()]
    fig, ax = plt.subplots(figsize=(8, 5.3), layout="constrained")
    bars = ax.barh(labels, ordered.MAE, color=[colors[c] for c in ordered.feature_set])
    ax.invert_yaxis()
    ax.bar_label(bars, fmt="%.6f", padding=4, fontsize=9)
    ax.set_xlim(0, ordered.MAE.max() * 1.25)
    ax.set_xlabel("Validation MAE (normalized recorded sales; lower is better)")
    ax.set_ylabel("Model and feature condition")
    ax.set_title("DEVELOPMENT — Validation MAE", loc="left", fontsize=14)
    fig.legend(handles=[Patch(color=c, label=l) for c, l in [(colors["sales_only"], "Sales only"),
              (colors["stockout_aware"], "Stockout aware"), (colors["common_reference"], "Common baseline")]],
              loc="outside lower center", ncol=3, fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    counts = f"{int(summary.n_observations.iloc[0]):,} matched validation rows · {int(summary.n_stores.iloc[0])} stores"
    fig.suptitle("Source: exact DELTA development r2 + original predictions · 2024-05-27 to 2024-06-10\n"
                 + counts + " · provisional selected models · NOT FINAL TEST",
                 fontsize=8)
    for extension in ("png", "svg"):
        fig.savefig(destination / f"development_mae.{extension}", dpi=170,
                    metadata={"Date": None} if extension == "svg" else None)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
    ordered = intervals.sort_values("model").reset_index(drop=True)
    for index, row in enumerate(ordered.itertuples()):
        # Draw endpoints directly: percentile intervals need not contain the estimate.
        ax.hlines(index, row.ci_lower, row.ci_upper, color="#236b8e", linewidth=2)
        ax.plot([row.ci_lower, row.ci_upper], [index, index], "|", color="#236b8e", markersize=9)
        ax.plot(row.MAE_difference, index, "o", color="#222222", markersize=5)
    ax.axvline(0, linestyle="--", linewidth=1, color="#777777")
    ax.set_yticks(range(len(ordered)), [names[m] for m in ordered.model])
    ax.invert_yaxis()
    ax.set_xlabel("MAE difference: stockout-aware − sales-only (normalized recorded sales)\nNegative favors stockout-aware")
    ax.set_ylabel("Model")
    ax.set_title("DEVELOPMENT — Paired MAE differences with 95% intervals", loc="left", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Source: " + counts + " · 2024-05-27 to 2024-06-10\n"
                 "Whole-store percentile bootstrap · 2,000 replicates · seed 245 · no refitting · NOT FINAL TEST", fontsize=8)
    for extension in ("png", "svg"):
        fig.savefig(destination / f"development_mae_differences.{extension}", dpi=170,
                    metadata={"Date": None} if extension == "svg" else None)
    plt.close(fig)
