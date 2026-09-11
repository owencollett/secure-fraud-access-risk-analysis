import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from src.preprocessing import build_preprocessor


def test_fraud_probability_output():

    data = {
        "Time": [0, 1, 2, 3, 4, 5],
        "Amount": [10, 20, 30, 100, 200, 300],
    }

    for number in range(1, 29):
        data[f"V{number}"] = [
            0.0,
            0.1,
            0.2,
            1.0,
            1.1,
            1.2,
        ]

    X = pd.DataFrame(data)

    y = [0, 0, 0, 1, 1, 1]

    preprocessor = build_preprocessor()

    X_ready = preprocessor.fit_transform(X)

    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )

    model.fit(X_ready, y)

    probabilities = model.predict_proba(
        X_ready
    )[:, 1]

    assert len(probabilities) == len(X)

    assert all(
        0 <= probability <= 1
        for probability in probabilities
    )