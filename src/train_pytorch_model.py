from pathlib import Path

import torch
from torch import nn
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
)

from .data_loader import load_transactions
from .data_splitter import split_transactions
from .preprocessing import build_preprocessor


DATA_PATH = Path("data/creditcard.csv")


def main():
    # Keep results reproducible
    torch.manual_seed(42)

    # Step 1: Load and split the transaction data
    df, _ = load_transactions(DATA_PATH)

    (
        X_train,
        X_validation,
        _,
        y_train,
        y_validation,
        _,
    ) = split_transactions(df)

    # Step 2: Reuse the same preprocessing as the other fraud models
    preprocessor = build_preprocessor()

    X_train_ready = preprocessor.fit_transform(X_train)
    X_validation_ready = preprocessor.transform(X_validation)

    # Step 3: Convert the data into PyTorch tensors
    X_train_tensor = torch.tensor(
        X_train_ready,
        dtype=torch.float32,
    )
    y_train_tensor = torch.tensor(
        y_train.to_numpy(),
        dtype=torch.float32,
    ).reshape(-1, 1)

    X_validation_tensor = torch.tensor(
        X_validation_ready,
        dtype=torch.float32,
    )

    # Step 4: Build a small neural network
    model = nn.Sequential(
        nn.Linear(X_train_tensor.shape[1], 32),
        nn.ReLU(),
        nn.Linear(32, 1),
    )

    # Step 5: Choose the loss function and optimizer
    loss_function = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001,
    )

    # Step 6: Train the network
    epochs = 10

    for epoch in range(epochs):
        model.train()

        logits = model(X_train_tensor)
        loss = loss_function(logits, y_train_tensor)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(
            f"Epoch {epoch + 1}/{epochs} - "
            f"Loss: {loss.item():.4f}"
        )

    # Step 7: Make predictions on the validation data
    model.eval()

    with torch.no_grad():
        validation_logits = model(X_validation_tensor)

        probabilities = torch.sigmoid(
            validation_logits
        ).squeeze().numpy()

    predictions = (
        probabilities >= 0.5
    ).astype(int)

    # Step 8: Evaluate with the same metrics as the other models
    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0,
    )
    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0,
    )
    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0,
    )
    roc_auc = roc_auc_score(
        y_validation,
        probabilities,
    )
    pr_auc = average_precision_score(
        y_validation,
        probabilities,
    )

    print("\nPYTORCH NEURAL NETWORK RESULTS")
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)
    print("ROC-AUC:", roc_auc)
    print("PR-AUC:", pr_auc)


if __name__ == "__main__":
    main()
