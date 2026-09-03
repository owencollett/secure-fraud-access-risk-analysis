import pandas as pd

# Load the dataset
df = pd.read_csv("data/creditcard.csv")

# Preview the data
print("First 5 rows:")
print(df.head())

# Dataset structure
print("\nDataset information:")
df.info()

# Summary statistics
print("\nSummary statistics:")
print(df.describe())

# Check class imbalance
print("\nFraud vs legitimate transactions:")
print(df["Class"].value_counts())

print("\nClass percentages:")
print(df["Class"].value_counts(normalize=True) * 100)

# Filter fraudulent transactions
fraud_df = df[df["Class"] == 1]

# Filter legitimate transactions
legit_df = df[df["Class"] == 0]

print("\nFraudulent transactions:")
print(fraud_df.head())

# Compare transaction amounts
print("\nLegitimate transaction amounts:")
print(legit_df["Amount"].describe())

print("\nFraudulent transaction amounts:")
print(fraud_df["Amount"].describe())



