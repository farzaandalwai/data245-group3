"""95% paired store-cluster percentile intervals on development splits only."""
import numpy as np
import pandas as pd


BOOTSTRAP_SPEC = {
    "method": "paired_store_cluster_percentile",
    "estimand": "row_weighted_MAE_stockout_aware_minus_sales_only",
    "confidence_level": 0.95, "replicates": 2000, "seed": 245,
    "rng": "numpy.Generator(PCG64)", "quantile_method": "linear",
    "cluster_unit": "store_id", "scope": "development_train_validation_only",
    "limitations": [
        "Conditional on this sample, fitted models and validation-selected settings; no refitting",
        "Validation selection can make validation comparisons optimistic",
        "Few stores can produce unstable or degenerate percentile intervals",
        "Assumes independent stores; shared calendar shocks and cross-store dependence are not addressed",
        "Observed-store resampling does not establish population representativeness",
        "Historical holdout exposure and retrospective series completeness remain limitations",
        "Training intervals are descriptive diagnostics, not held-out performance",
    ],
}
INTERVAL_COLUMNS = ["model", "split", "n_observations", "n_stores", "MAE_difference",
                    "ci_lower", "ci_upper", "confidence_level", "replicates", "seed",
                    "status", "limitations"]


def paired_store_intervals(predictions, observations, *, purpose, models, splits=("validation",)):
    """Resample S whole stores S times with replacement in each of 2,000 draws.

    Sums/counts are sufficient statistics for concatenating complete clusters,
    including repeated copies of a selected store. The denominator is the draw's
    total row count, never an unweighted mean of store MAEs. Pairing is validated
    before any resampling. Sorted keys/stores make input row order irrelevant.
    """
    from src.data_preprocessing_DELTA.v2 import KEY
    from src.evaluation_SAS.v2 import BASELINES, development_gate, validate_predictions

    development_gate(purpose, splits)
    validate_predictions(predictions, observations, models, splits)
    rows = []
    for model in models:
        if model in BASELINES:
            continue
        for split in splits:
            frame = predictions.loc[predictions.model.eq(model) & predictions.split.eq(split)]
            sales = frame.loc[frame.feature_set.eq("sales_only"), KEY + ["actual", "prediction"]]
            aware = frame.loc[frame.feature_set.eq("stockout_aware"), KEY + ["prediction"]]
            paired = sales.merge(aware, on=KEY, validate="one_to_one", suffixes=("_sales", "_aware"))
            paired = paired.sort_values(KEY).reset_index(drop=True)
            with np.errstate(over="raise", invalid="raise"):
                paired["difference"] = (np.abs(paired.prediction_aware - paired.actual)
                                        - np.abs(paired.prediction_sales - paired.actual))
                clusters = paired.groupby("store_id", sort=True).difference.agg(["sum", "size"])
                point = float(clusters["sum"].sum() / clusters["size"].sum())
            n_stores = len(clusters)
            low, high, status = None, None, "insufficient_stores"
            if n_stores >= 2:
                rng = np.random.Generator(np.random.PCG64(245))
                sums, counts = clusters["sum"].to_numpy(), clusters["size"].to_numpy()
                # Bounded chunks avoid materializing a 2000 x S matrix for large S.
                draws = []
                for start in range(0, 2000, 100):
                    indices = rng.integers(n_stores, size=(min(100, 2000-start), n_stores))
                    with np.errstate(over="raise", invalid="raise"):
                        draws.extend((sums[indices].sum(axis=1) / counts[indices].sum(axis=1)).tolist())
                low, high = map(float, np.quantile(draws, [0.025, 0.975], method="linear"))
                status = "ok" if low != high else "degenerate_interval"
            rows.append({"model": model, "split": split, "n_observations": len(paired),
                         "n_stores": n_stores, "MAE_difference": point,
                         "ci_lower": low, "ci_upper": high, "confidence_level": .95,
                         "replicates": 2000 if n_stores >= 2 else 0, "seed": 245,
                         "status": status, "limitations": "; ".join(BOOTSTRAP_SPEC["limitations"])})
    return pd.DataFrame(rows, columns=INTERVAL_COLUMNS)
