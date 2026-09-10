from pathlib import Path

import pandas as pd
from joblib import dump

from .data_loader import load_transactions
from .data_splitter import split_transactions
from .preprocessing import build_preprocessor


def prepare_data(
    data_path,
    preprocessor_path=None,
    random_state=42,
):
    """
    Run the complete reproducible data-preparation pipeline.

    Steps:
        1. Load the raw CSV file.
        2. Validate its schema and values.
        3. Create stratified train/validation/test splits.
        4. Fit preprocessing on training data only.
        5. Transform all three datasets.
        6. Optionally save the fitted preprocessor.
    """

    df, validation_report = load_transactions(
        data_path
    )

    (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test,
    ) = split_transactions(
        df,
        random_state=random_state,
    )

    preprocessor = build_preprocessor()

    X_train_array = preprocessor.fit_transform(
        X_train
    )

    X_validation_array = preprocessor.transform(
        X_validation
    )

    X_test_array = preprocessor.transform(X_test)

    feature_names = (
        preprocessor.get_feature_names_out()
    )

    X_train_processed = pd.DataFrame(
        X_train_array,
        columns=feature_names,
        index=X_train.index,
    )

    X_validation_processed = pd.DataFrame(
        X_validation_array,
        columns=feature_names,
        index=X_validation.index,
    )

    X_test_processed = pd.DataFrame(
        X_test_array,
        columns=feature_names,
        index=X_test.index,
    )

    if preprocessor_path is not None:
        preprocessor_path = Path(preprocessor_path)
        preprocessor_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dump(preprocessor, preprocessor_path)

    return {
        "validation_report": validation_report,
        "preprocessor": preprocessor,
        "X_train": X_train_processed,
        "X_validation": X_validation_processed,
        "X_test": X_test_processed,
        "y_train": y_train,
        "y_validation": y_validation,
        "y_test": y_test,
    }