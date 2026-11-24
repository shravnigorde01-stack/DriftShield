from monitoring.performance.performance_metrics import (
    calculate_classification_metrics
)

# Actual results
actual = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]

# Model predictions
predicted = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]

# Calculate performance
results = calculate_classification_metrics(
    actual,
    predicted
)

print("\nDRIFTSHIELD — CLASSIFICATION PERFORMANCE")
print("----------------------------------------")

for metric, value in results.items():
    print(f"{metric}: {value}")