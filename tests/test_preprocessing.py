import numpy as np
import pandas as pd

from src.preprocessing import (
    build_preprocessor,
    build_log_amount_preprocessor,
)


def make_feature_data():
    data = {
        "Time": [0.0, 100.0, 200.0],
        "Amount": [10.0, 50.0, 100.0],
    }

    for number in range(1, 29):
        data[f"V{number}"] = [0.0, 0.1, 0.2]

    return pd.DataFrame(data)


def test_preprocessor():
    df = make_feature_data()

    preprocessor = build_preprocessor()

    transformed = preprocessor.fit_transform(df)

    assert transformed.shape[0] == 3
    assert transformed.shape[1] == 30
    assert np.isfinite(transformed).all()


def test_log_amount_preprocessor():
    df = make_feature_data()

    preprocessor = build_log_amount_preprocessor()

    transformed = preprocessor.fit_transform(df)

    assert transformed.shape[0] == 3
    assert transformed.shape[1] == 31
    assert np.isfinite(transformed).all()
    