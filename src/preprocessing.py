import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


SCALED_FEATURES = ["Time", "Amount"]

PCA_FEATURES = [
    f"V{i}" for i in range(1, 29)
]


def build_preprocessor():
    """
    Create the transaction preprocessing pipeline.

    Time and Amount are standardized.
    V1 through V28 pass through without modification.
    """

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "scaled_features",
                StandardScaler(),
                SCALED_FEATURES,
            ),
            (
                "pca_features",
                "passthrough",
                PCA_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return preprocessor

def add_log_amount(df):
    df = df.copy()
    df["LogAmount"] = np.log1p(df["Amount"])
    return df


def build_log_amount_preprocessor():

    column_transformer = ColumnTransformer(
        transformers=[
            (
                "scaled_features",
                StandardScaler(),
                ["Time", "Amount", "LogAmount"],
            ),
            (
                "pca_features",
                "passthrough",
                PCA_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    preprocessor = Pipeline(
        steps=[
            (
                "add_log_amount",
                FunctionTransformer(add_log_amount),
            ),
            (
                "transform_columns",
                column_transformer,
            ),
        ]
    )

    return preprocessor