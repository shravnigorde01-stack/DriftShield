import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def calculate_classification_metrics(
    actual,
    predicted
):

    accuracy = accuracy_score(actual, predicted)

    precision = precision_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )

    matrix = confusion_matrix(
        actual,
        predicted
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": matrix.tolist()
    }


def calculate_regression_metrics(
    actual,
    predicted
):

    mae = mean_absolute_error(actual, predicted)

    mse = mean_squared_error(actual, predicted)

    rmse = np.sqrt(mse)

    r2 = r2_score(actual, predicted)

    return {
        "mae": round(float(mae), 4),
        "mse": round(float(mse), 4),
        "rmse": round(float(rmse), 4),
        "r2_score": round(float(r2), 4)
    }