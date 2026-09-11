import pandas as pd
import pytest

from src.data_loader import load_transactions


def make_valid_fraud_data():
    data = {
        "Time": [0.0, 1.0],
        "Amount": [10.0, 20.0],
        "Class": [0, 1],
    }

    for number in range(1, 29):
        data[f"V{number}"] = [0.0, 0.1]

    return pd.DataFrame(data)


def test_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_transactions(missing_file)


def test_valid_file(tmp_path):
    df = make_valid_fraud_data()

    file_path = tmp_path / "valid.csv"
    df.to_csv(file_path, index=False)

    loaded_df, report = load_transactions(file_path)

    assert len(loaded_df) == 2
    assert "Class" in loaded_df.columns


def test_missing_required_column(tmp_path):
    df = make_valid_fraud_data()

    df = df.drop(columns=["Class"])

    file_path = tmp_path / "invalid.csv"
    df.to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        load_transactions(file_path)
        