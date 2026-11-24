from monitoring.drift.numerical_drift import detect_numerical_drift
from monitoring.drift.categorical_drift import detect_categorical_drift


def detect_data_drift(reference_df, current_df):

    numerical_results = detect_numerical_drift(
        reference_df,
        current_df
    )

    categorical_results = detect_categorical_drift(
        reference_df,
        current_df
    )

    combined_results = {
        **numerical_results,
        **categorical_results
    }

    total_features = len(combined_results)

    drifted_features = sum(
        1
        for result in combined_results.values()
        if result.get("drift_detected") is True
    )

    stable_features = sum(
        1
        for result in combined_results.values()
        if result.get("drift_detected") is False
    )

    return {
        "total_features": total_features,
        "drifted_features": drifted_features,
        "stable_features": stable_features,
        "feature_results": combined_results
    }