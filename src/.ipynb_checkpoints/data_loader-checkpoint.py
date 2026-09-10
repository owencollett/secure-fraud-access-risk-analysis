from pathlib import Path

import pandas as pd

from .validation import validate_transactions


def load_transactions(file_path):
    """
    Load and validate the credit-card transaction dataset.

    Args:
        file_path: Path to the CSV dataset.

    Returns:
        tuple: The validated DataFrame and validation report.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path.resolve()}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            f"Expected a CSV file, but received: {file_path.suffix}"
        )

    try:
        df = pd.read_csv(file_path)
    except Exception as error:
        raise ValueError(
            f"Unable to read the dataset: {error}"
        ) from error

    validation_report = validate_transactions(df)

    return df, validation_report