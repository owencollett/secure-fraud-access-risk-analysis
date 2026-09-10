import pandas as pd
from sklearn.model_selection import train_test_split


def split_transactions(
    df: pd.DataFrame,
    target_column: str = "Class",
    random_state: int = 42,
):
    """
    Split transaction data into training, validation, and test sets.

    The split is:
        70% training
        15% validation
        15% testing

    Stratification preserves the fraud rate in every split.
    """

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' was not found."
        )

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # First split: 70% training and 30% temporary data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=random_state,
        stratify=y,
    )

    # Second split: divide temporary data into 15% validation
    # and 15% testing
    X_validation, X_test, y_validation, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=random_state,
        stratify=y_temp,
    )

    return (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test,
    )