from monitoring.performance.performance_metrics import (
    calculate_classification_metrics,
    calculate_regression_metrics
)


def evaluate_model_performance(
    actual,
    predicted,
    model_type
):

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted values must have equal lengths."
        )

    if model_type == "classification":

        results = calculate_classification_metrics(
            actual,
            predicted
        )

    elif model_type == "regression":

        results = calculate_regression_metrics(
            actual,
            predicted
        )

    else:
        raise ValueError(
            "Model type must be classification or regression."
        )

    return {
        "model_type": model_type,
        "total_predictions": len(actual),
        "metrics": results
    }