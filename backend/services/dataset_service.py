import pandas as pd


def validate_dataset(file_path):

    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Check whether dataset is empty
        if df.empty:
            return {
                "valid": False,
                "message": "Dataset is empty."
            }

        # Check whether columns exist
        if len(df.columns) == 0:
            return {
                "valid": False,
                "message": "Dataset has no columns."
            }

        # Check duplicate column names
        if df.columns.duplicated().any():
            return {
                "valid": False,
                "message": "Dataset contains duplicate column names."
            }

        # Collect dataset information
        return {
            "valid": True,
            "message": "Dataset validated successfully.",
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum())
        }

    except Exception as error:
        return {
            "valid": False,
            "message": f"Unable to read dataset: {str(error)}"
        }