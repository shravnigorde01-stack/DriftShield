from monitoring.drift.drift_detector import detect_data_drift

from monitoring.performance.performance_detector import (
    evaluate_model_performance
)


def run_monitoring(
    reference_df,
    current_df,
    actual=None,
    predicted=None,
    model_type=None
):

    # Step 1: Detect data drift
    drift_results = detect_data_drift(
        reference_df,
        current_df
    )

    # Step 2: Evaluate model performance if labels are available
    performance_results = None

    if actual is not None and predicted is not None:

        if model_type is None:
            raise ValueError(
                "Model type is required for performance evaluation."
            )

        performance_results = evaluate_model_performance(
            actual,
            predicted,
            model_type
        )

    elif actual is not None or predicted is not None:
        raise ValueError(
            "Both actual and predicted values are required."
        )

    # Step 3: Generate combined monitoring report
    return {
        "data_drift": drift_results,
        "performance": performance_results,
        "performance_status": (
            "Available"
            if performance_results is not None
            else "Pending ground-truth labels"
        )
    }