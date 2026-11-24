import pandas as pd

from monitoring.drift.categorical_drift import detect_categorical_drift


# Original dataset
reference_data = pd.DataFrame({
    "city": (
        ["Mumbai"] * 70 +
        ["Pune"] * 20 +
        ["Delhi"] * 10
    )
})

# New dataset with changed category distribution
current_data = pd.DataFrame({
    "city": (
        ["Mumbai"] * 10 +
        ["Pune"] * 20 +
        ["Delhi"] * 70
    )
})


results = detect_categorical_drift(
    reference_data,
    current_data
)

print("\nDRIFTSHIELD — CATEGORICAL DRIFT REPORT")
print("--------------------------------------")

for feature, result in results.items():
    print(f"\nFeature: {feature}")

    for key, value in result.items():
        print(f"{key}: {value}")
        