from monitoring.performance.performance_metrics import (
    calculate_regression_metrics
)

# Actual values
actual = [100, 200, 300, 400, 500]

# Model predictions
predicted = [110, 190, 310, 380, 510]

# Calculate performance
results = calculate_regression_metrics(
    actual,
    predicted
)

print("\nDRIFTSHIELD — REGRESSION PERFORMANCE")
print("------------------------------------")

for metric, value in results.items():
    print(f"{metric}: {value}")