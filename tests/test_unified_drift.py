import pandas as pd

from monitoring.drift.drift_detector import detect_data_drift


# Original dataset
reference_data = pd.DataFrame({
    "age": [22, 24, 25, 26, 28, 30, 32, 34, 35, 36,
            23, 27, 29, 31, 33, 37, 38, 39, 40, 41],

    "city": (
        ["Mumbai"] * 14 +
        ["Pune"] * 4 +
        ["Delhi"] * 2
    )
})


# New dataset
current_data = pd.DataFrame({
    "age": [45, 48, 50, 52, 55, 57, 60, 62, 65, 68,
            46, 49, 53, 56, 59, 61, 64, 67, 70, 72],

    "city": (
        ["Mumbai"] * 2 +
        ["Pune"] * 4 +
        ["Delhi"] * 14
    )
})


# Run unified drift detection
results = detect_data_drift(
    reference_data,
    current_data
)


print("\n====================================")
print("       DRIFTSHIELD DRIFT REPORT")
print("====================================")

print("Total Features:", results["total_features"])
print("Drifted Features:", results["drifted_features"])
print("Stable Features:", results["stable_features"])

print("\nFEATURE-LEVEL RESULTS")
print("------------------------------------")

for feature, details in results["feature_results"].items():

    print(f"\nFeature: {feature}")

    for key, value in details.items():
        print(f"{key}: {value}")