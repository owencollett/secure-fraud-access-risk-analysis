import numpy as np
import pandas as pd


EXPECTED_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount", "Class"]
)


def validate_transactions(df: pd.DataFrame) -> dict:
    """
    Validate the fraud transaction dataset.

    Raises:
        ValueError: If the dataset contains invalid data.

    Returns:
        dict: A summary of the validated dataset.
    """
    errors = []

    # Check that the dataset is not empty
    if df.empty:
        errors.append("The dataset contains no rows.")

    # Check for duplicated column names
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()

    if duplicate_columns:
        errors.append(
            f"Duplicated column names found: {duplicate_columns}"
        )

    # Check the expected schema
    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")

    if unexpected_columns:
        errors.append(f"Unexpected columns: {unexpected_columns}")

    # Only run column-level checks when all expected columns exist
    if not missing_columns:
        non_numeric_columns = [
            column for column in EXPECTED_COLUMNS
            if not pd.api.types.is_numeric_dtype(df[column])
        ]

        if non_numeric_columns:
            errors.append(
                f"Columns expected to be numeric: {non_numeric_columns}"
            )

        missing_value_count = int(
            df[EXPECTED_COLUMNS].isna().sum().sum()
        )

        if missing_value_count > 0:
            errors.append(
                f"Found {missing_value_count:,} missing values."
            )

        numeric_values = df[EXPECTED_COLUMNS].to_numpy()

        if not np.isfinite(numeric_values).all():
            errors.append(
                "The dataset contains infinite or non-finite values."
            )

        class_values = set(df["Class"].dropna().unique())

        if not class_values.issubset({0, 1}):
            errors.append(
                f"Class must contain only 0 and 1. Found: {class_values}"
            )

        if class_values != {0, 1}:
            errors.append(
                "The dataset must contain both legitimate and fraudulent transactions."
            )

        if (df["Amount"] < 0).any():
            errors.append("Amount contains negative values.")

        if (df["Time"] < 0).any():
            errors.append("Time contains negative values.")

    # Stop immediately if validation failed
    if errors:
        error_message = "\n- ".join(errors)

        raise ValueError(
            f"Dataset validation failed:\n- {error_message}"
        )

    fraud_count = int(df["Class"].sum())
    duplicate_row_count = int(df.duplicated().sum())

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "fraud_count": fraud_count,
        "legitimate_count": len(df) - fraud_count,
        "fraud_rate": df["Class"].mean(),
        "duplicate_rows": duplicate_row_count,
    }