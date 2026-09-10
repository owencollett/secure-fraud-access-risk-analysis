import numpy as np
import pandas as pd
import pytest

from src.pipeline import prepare_data
from src.validation import validate_transactions


def make_sample_dataset(rows=200):
    """
    Create a small valid transaction dataset for testing.
    """

    data = {
        "Time": np.arange(rows, dtype=float),
    }

    for number in range(1, 29):
        data[f"V{number}"] = (
            np.linspace(-1, 1, rows)
            + number * 0.01
        )

    data["Amount"] = np.linspace(
        1.00,
        500.00,
        rows,
    )

    # Create 180 legitimate and 20 fraudulent rows
    classes = np.zeros(rows, dtype=int)
    classes[:20] = 1
    data["Class"] = classes

    return pd.DataFrame(data)


def test_valid_dataset_passes_validation():
    df = make_sample_dataset()

    report = validate_transactions(df)

    assert report["rows"] == 200
    assert report["columns"] == 31
    assert report["fraud_count"] == 20
    assert report["legitimate_count"] == 180


def test_missing_column_fails_validation():
    df = make_sample_dataset()
    df = df.drop(columns=["Amount"])

    with pytest.raises(
        ValueError,
        match="Missing columns",
    ):
        validate_transactions(df)


def test_negative_amount_fails_validation():
    df = make_sample_dataset()
    df.loc[0, "Amount"] = -50.00

    with pytest.raises(
        ValueError,
        match="negative values",
    ):
        validate_transactions(df)


def test_pipeline_is_reproducible(tmp_path):
    df = make_sample_dataset()

    data_path = tmp_path / "transactions.csv"
    preprocessor_path = (
        tmp_path / "preprocessor.joblib"
    )

    df.to_csv(data_path, index=False)

    first_run = prepare_data(
        data_path=data_path,
        preprocessor_path=preprocessor_path,
        random_state=42,
    )

    second_run = prepare_data(
        data_path=data_path,
        random_state=42,
    )

    assert first_run["X_train"].shape == (140, 30)
    assert first_run["X_validation"].shape == (30, 30)
    assert first_run["X_test"].shape == (30, 30)

    assert first_run["X_train"].index.equals(
        second_run["X_train"].index
    )

    assert first_run["X_validation"].index.equals(
        second_run["X_validation"].index
    )

    assert first_run["X_test"].index.equals(
        second_run["X_test"].index
    )

    np.testing.assert_allclose(
        first_run["X_train"],
        second_run["X_train"],
    )

    assert preprocessor_path.exists()