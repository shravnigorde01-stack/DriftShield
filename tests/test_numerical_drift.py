import pandas as pd

from monitoring.drift.numerical_drift import detect_numerical_drift


# Original dataset
reference_data = pd.DataFrame({
    "age": [22, 24, 25, 26, 28, 30, 32, 34, 35, 36,
            23, 27, 29, 31, 33, 37, 38, 39, 40, 41]
})

# New dataset with changed values
current_data = pd.DataFrame({
    "age": [45, 48, 50, 52, 55, 57, 60, 62, 65, 68,
            46, 49, 53, 56, 59, 61, 64, 67, 70, 72]
})


results = detect_numerical_drift(
    reference_data,
    current_data
)

print("\nDRIFTSHIELD — NUMERICAL DRIFT REPORT")
print("------------------------------------")

for feature, result in results.items():
    print(f"\nFeature: {feature}")
    for key, value in result.items():
        print(f"{key}: {value}")