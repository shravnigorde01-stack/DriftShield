import pandas as pd
from scipy.stats import chi2_contingency


def detect_categorical_drift(
    reference_df,
    current_df,
    p_value_threshold=0.05
):

    results = {}

    categorical_columns = reference_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns:

        if column not in current_df.columns:
            results[column] = {
                "status": "Missing column",
                "drift_detected": True
            }
            continue

        reference = reference_df[column].fillna("Missing").astype(str)
        current = current_df[column].fillna("Missing").astype(str)

        categories = sorted(
            set(reference.unique()) | set(current.unique())
        )

        reference_counts = reference.value_counts()
        current_counts = current.value_counts()

        contingency_table = [
            [reference_counts.get(category, 0) for category in categories],
            [current_counts.get(category, 0) for category in categories]
        ]

        # Chi-square test requires at least two categories
        if len(categories) < 2:
            results[column] = {
                "status": "Insufficient categories",
                "drift_detected": None
            }
            continue

        try:
            chi2, p_value, dof, expected = chi2_contingency(
                contingency_table
            )

            drift_detected = p_value < p_value_threshold

            results[column] = {
                "chi2_statistic": round(float(chi2), 4),
                "p_value": round(float(p_value), 4),
                "degrees_of_freedom": int(dof),
                "drift_detected": bool(drift_detected),
                "status": (
                    "Drift Detected"
                    if drift_detected
                    else "Stable"
                )
            }

        except ValueError:
            results[column] = {
                "status": "Unable to calculate",
                "drift_detected": None
            }

    return results