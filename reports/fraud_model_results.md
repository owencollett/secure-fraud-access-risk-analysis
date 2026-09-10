# Fraud Model Results

## Objective

The goal of this phase was to train and compare machine-learning models for detecting fraudulent credit-card transactions.

## Models Tested

### Logistic Regression Baseline

Validation results:

- Precision: 0.8036
- Recall: 0.6081
- F1: 0.6923
- ROC-AUC: 0.9544
- PR-AUC: 0.6705

Confusion matrix:

- True Negatives: 42,636
- False Positives: 11
- False Negatives: 29
- True Positives: 45

### Balanced Logistic Regression

Validation results:

- Precision: 0.0670
- Recall: 0.8784
- F1: 0.1245
- ROC-AUC: 0.9684
- PR-AUC: 0.6275

The balanced model caught more fraudulent transactions, but it also created 905 false positives. Because precision dropped significantly, this model was not selected.

### Random Forest

Validation results:

- Precision: 0.9649
- Recall: 0.7432
- F1: 0.8397
- ROC-AUC: 0.9303
- PR-AUC: 0.8074

The Random Forest provided the strongest overall balance between precision, recall, and F1 score, with only two false positives on the validation set.

## Feature Engineering Experiment

A log-transformed version of the transaction Amount feature was tested.

Validation results:

- Precision: 0.9483
- Recall: 0.7432
- F1: 0.8333
- ROC-AUC: 0.9170
- PR-AUC: 0.8113

The LogAmount feature slightly improved PR-AUC, but precision, F1, and ROC-AUC decreased while recall stayed the same. Because the overall improvement was not strong enough, the original Random Forest was kept.

## Experiment Comparison

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | Notes |
|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | 0.8036 | 0.6081 | 0.6923 | 0.9544 | 0.6705 | Baseline |
| Balanced Logistic Regression | 0.0670 | 0.8784 | 0.1245 | 0.9684 | 0.6275 | Higher recall, far too many false positives |
| Random Forest | 0.9649 | 0.7432 | 0.8397 | 0.9303 | 0.8074 | Selected final model |
| Random Forest + LogAmount | 0.9483 | 0.7432 | 0.8333 | 0.9170 | 0.8113 | Small PR-AUC gain, weaker overall |

## Final Model Selection

The original Random Forest model was selected as the final candidate because it provided the strongest overall validation performance while maintaining very high precision and substantially better recall than the Logistic Regression baseline.

## Final Held-Out Test Results

- Precision: 0.9508
- Recall: 0.7838
- F1: 0.8593
- ROC-AUC: 0.9308
- PR-AUC: 0.8203

Confusion matrix:

- True Negatives: 42,645
- False Positives: 3
- False Negatives: 16
- True Positives: 58

The final model correctly identified 58 fraudulent transactions while producing only 3 false-positive fraud alerts.

## Important Limitation

The V1-V28 variables are anonymized, which makes it difficult to explain their real-world business meaning. The dataset is also historical, so its fraud patterns may not represent future or current fraud behavior.

## Conclusion

Random Forest performed better overall than the Logistic Regression models for this fraud-detection task. The experiments also showed that improving one metric does not necessarily improve the entire model. The final model achieved high precision while detecting most fraudulent transactions in the held-out test set.