from monitoring.performance.performance_detector import (
    evaluate_model_performance
)


# CLASSIFICATION TEST

actual_classification = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]

predicted_classification = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]


classification_results = evaluate_model_performance(
    actual_classification,
    predicted_classification,
    "classification"
)


# REGRESSION TEST

actual_regression = [100, 200, 300, 400, 500]

predicted_regression = [110, 190, 310, 380, 510]


regression_results = evaluate_model_performance(
    actual_regression,
    predicted_regression,
    "regression"
)


# DISPLAY RESULTS

print("\n====================================")
print(" DRIFTSHIELD PERFORMANCE REPORT")
print("====================================")


print("\nCLASSIFICATION RESULTS")

for key, value in classification_results.items():
    print(f"{key}: {value}")


print("\nREGRESSION RESULTS")

for key, value in regression_results.items():
    print(f"{key}: {value}")