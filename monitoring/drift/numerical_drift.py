import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def calculate_psi(reference, current, bins=10):

    reference = np.asarray(reference, dtype=float)
    current = np.asarray(current, dtype=float)

    reference = reference[np.isfinite(reference)]
    current = current[np.isfinite(current)]

    if len(reference) == 0 or len(current) == 0:
        return None

    if np.min(reference) == np.max(reference):
        edges = [-np.inf, reference[0], np.inf]
    else:
        quantiles = np.linspace(0, 1, bins + 1)[1:-1]
        internal_edges = np.unique(
            np.quantile(reference, quantiles)
        )
        edges = np.concatenate(
            ([-np.inf], internal_edges, [np.inf])
        )

    reference_counts, _ = np.histogram(reference, bins=edges)
    current_counts, _ = np.histogram(current, bins=edges)

    reference_pct = reference_counts / len(reference)
    current_pct = current_counts / len(current)

    epsilon = 0.0001

    reference_pct = np.maximum(reference_pct, epsilon)
    current_pct = np.maximum(current_pct, epsilon)

    psi = np.sum(
        (current_pct - reference_pct)
        * np.log(current_pct / reference_pct)
    )

    return float(psi)


def detect_numerical_drift(
    reference_df,
    current_df,
    psi_threshold=0.2,
    ks_threshold=0.05
):

    results = {}

    numerical_columns = reference_df.select_dtypes(
        include=np.number
    ).columns

    for column in numerical_columns:

        if column not in current_df.columns:
            results[column] = {
                "status": "Missing column",
                "drift_detected": True
            }
            continue

        reference = pd.to_numeric(
            reference_df[column], errors="coerce"
        ).dropna()

        current = pd.to_numeric(
            current_df[column], errors="coerce"
        ).dropna()

        if len(reference) == 0 or len(current) == 0:
            results[column] = {
                "status": "Insufficient data",
                "drift_detected": None
            }
            continue

        ks_result = ks_2samp(reference, current)

        psi_score = calculate_psi(reference, current)

        drift_detected = (
            psi_score >= psi_threshold
            or ks_result.pvalue < ks_threshold
        )

        results[column] = {
            "psi_score": round(psi_score, 4),
            "ks_statistic": round(float(ks_result.statistic), 4),
            "ks_p_value": round(float(ks_result.pvalue), 4),
            "drift_detected": bool(drift_detected),
            "status": (
                "Drift Detected" if drift_detected else "Stable"
            )
        }

    return results