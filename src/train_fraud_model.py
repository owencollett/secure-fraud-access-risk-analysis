import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
)

from .data_loader import load_transactions
from .data_splitter import split_transactions
from .preprocessing import (
    build_preprocessor,
    build_log_amount_preprocessor,
)


# Location of the fraud dataset
DATA_PATH = Path("data/creditcard.csv")


def main():
    # Step 1: Load the transaction data
    df, validation_report = load_transactions(DATA_PATH)

    print("Data loaded successfully.")
    print(f"Total transactions: {len(df)}")


    # Step 2: Split the data into training, validation, and testing groups
    (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test,
    ) = split_transactions(df)

    print(f"Training transactions: {len(X_train)}")
    print(f"Validation transactions: {len(X_validation)}")
    print(f"Test transactions: {len(X_test)}")


    # Step 3: Prepare the transaction information
    preprocessor = build_preprocessor()

    X_train_ready = preprocessor.fit_transform(X_train)
    X_validation_ready = preprocessor.transform(X_validation)

    print("Data preprocessing complete.")


    # Step 4: Create the machine-learning model
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )


    # Step 5: Teach the model using the training data
    model.fit(X_train_ready, y_train)

    print("Model training complete.")


    # Step 6: Let the model guess fraud on the validation data
    probabilities = model.predict_proba(X_validation_ready)[:, 1]

    predictions = (probabilities >= 0.5).astype(int)


    # Step 7: See how well it did
    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_validation,
        probabilities
    )

    pr_auc = average_precision_score(
        y_validation,
        probabilities
    )

    matrix = confusion_matrix(
        y_validation,
        predictions
    )

    print("\nRESULTS")
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)
    print("ROC-AUC:", roc_auc)
    print("PR-AUC:", pr_auc)
    print("Confusion Matrix:")
    print(matrix)

    # Step 8: Train a class-balanced Logistic Regression model
    balanced_model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        class_weight="balanced"
    )

    balanced_model.fit(X_train_ready, y_train)

    balanced_probabilities = balanced_model.predict_proba(
        X_validation_ready
    )[:, 1]

    balanced_predictions = (
        balanced_probabilities >= 0.5
    ).astype(int)

    balanced_precision = precision_score(
        y_validation,
        balanced_predictions,
        zero_division=0
    )

    balanced_recall = recall_score(
        y_validation,
        balanced_predictions,
        zero_division=0
    )

    balanced_f1 = f1_score(
        y_validation,
        balanced_predictions,
        zero_division=0
    )

    balanced_roc_auc = roc_auc_score(
        y_validation,
        balanced_probabilities
    )

    balanced_pr_auc = average_precision_score(
        y_validation,
        balanced_probabilities
    )

    balanced_matrix = confusion_matrix(
        y_validation,
        balanced_predictions
    )

    print("\nBALANCED MODEL RESULTS")
    print("Precision:", balanced_precision)
    print("Recall:", balanced_recall)
    print("F1:", balanced_f1)
    print("ROC-AUC:", balanced_roc_auc)
    print("PR-AUC:", balanced_pr_auc)
    print("Confusion Matrix:")
    print(balanced_matrix)

    # Step 9: Train a Random Forest model
    random_forest = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    random_forest.fit(X_train_ready, y_train)

    rf_probabilities = random_forest.predict_proba(
        X_validation_ready
    )[:, 1]

    rf_predictions = (
        rf_probabilities >= 0.5
    ).astype(int)

    rf_precision = precision_score(
        y_validation,
        rf_predictions,
        zero_division=0
    )

    rf_recall = recall_score(
        y_validation,
        rf_predictions,
        zero_division=0
    )

    rf_f1 = f1_score(
        y_validation,
        rf_predictions,
        zero_division=0
    )

    rf_roc_auc = roc_auc_score(
        y_validation,
        rf_probabilities
    )

    rf_pr_auc = average_precision_score(
        y_validation,
        rf_probabilities
    )

    rf_matrix = confusion_matrix(
        y_validation,
        rf_predictions
    )

    print("\nRANDOM FOREST RESULTS")
    print("Precision:", rf_precision)
    print("Recall:", rf_recall)
    print("F1:", rf_f1)
    print("ROC-AUC:", rf_roc_auc)
    print("PR-AUC:", rf_pr_auc)
    print("Confusion Matrix:")
    print(rf_matrix)

    # Step 10: Test a new LogAmount feature
    log_preprocessor = build_log_amount_preprocessor()

    X_train_log = log_preprocessor.fit_transform(X_train)
    X_validation_log = log_preprocessor.transform(X_validation)

    log_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    log_model.fit(X_train_log, y_train)

    log_probabilities = log_model.predict_proba(
        X_validation_log
    )[:, 1]

    log_predictions = (
        log_probabilities >= 0.5
    ).astype(int)

    log_precision = precision_score(
        y_validation,
        log_predictions,
        zero_division=0
    )

    log_recall = recall_score(
        y_validation,
        log_predictions,
        zero_division=0
    )

    log_f1 = f1_score(
        y_validation,
        log_predictions,
        zero_division=0
    )

    log_roc_auc = roc_auc_score(
        y_validation,
        log_probabilities
    )

    log_pr_auc = average_precision_score(
        y_validation,
        log_probabilities
    )

    print("\nLOG AMOUNT EXPERIMENT")
    print("Precision:", log_precision)
    print("Recall:", log_recall)
    print("F1:", log_f1)
    print("ROC-AUC:", log_roc_auc)
    print("PR-AUC:", log_pr_auc)

    # Step 11: Final evaluation on the test data
    X_test_ready = preprocessor.transform(X_test)

    test_probabilities = random_forest.predict_proba(
        X_test_ready
    )[:, 1]

    test_predictions = (
        test_probabilities >= 0.5
    ).astype(int)

    test_precision = precision_score(
        y_test,
        test_predictions,
        zero_division=0
    )

    test_recall = recall_score(
        y_test,
        test_predictions,
        zero_division=0
    )

    test_f1 = f1_score(
        y_test,
        test_predictions,
        zero_division=0
    )

    test_roc_auc = roc_auc_score(
        y_test,
        test_probabilities
    )

    test_pr_auc = average_precision_score(
        y_test,
        test_probabilities
    )

    test_matrix = confusion_matrix(
        y_test,
        test_predictions
    )

    print("\nFINAL TEST RESULTS")
    print("Precision:", test_precision)
    print("Recall:", test_recall)
    print("F1:", test_f1)
    print("ROC-AUC:", test_roc_auc)
    print("PR-AUC:", test_pr_auc)
    print("Confusion Matrix:")
    print(test_matrix)

    # Step 12: Create precision-recall curve
    curve_precision, curve_recall, _ = precision_recall_curve(
        y_validation,
        rf_probabilities
    )

    figure_folder = Path("reports/figures")
    figure_folder.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.plot(curve_recall, curve_precision)

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Random Forest Precision-Recall Curve")

    plt.tight_layout()

    plt.savefig(
        figure_folder / "fraud_precision_recall_curve.png",
        dpi=300
    )

    plt.close()

    print("\nPrecision-recall curve saved.")

if __name__ == "__main__":

    main()