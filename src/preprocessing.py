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