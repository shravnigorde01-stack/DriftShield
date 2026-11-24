import pandas as pd

from monitoring.monitoring_engine import run_monitoring


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


# Incoming dataset
current_data = pd.DataFrame({
    "age": [45, 48, 50, 52, 55, 57, 60, 62, 65, 68,
            46, 49, 53, 56, 59, 61, 64, 67, 70, 72],

    "city": (
        ["Mumbai"] * 2 +
        ["Pune"] * 4 +
        ["Delhi"] * 14
    )
})


# Run central monitoring
results = run_monitoring(
    reference_df=reference_data,
    current_df=current_data
)


print("\n====================================")
print("     DRIFTSHIELD MONITORING REPORT")
print("====================================")

print("\nDATA DRIFT:")
print(results["data_drift"])

print("\nPERFORMANCE:")
print(results["performance_status"])