# Responsible AI, Privacy, and Security Notes

This project is an educational prototype, so I kept the automated parts intentionally limited. Neither the fraud model nor the security rules should be treated as a final decision-maker.

## Fraud-model limitations

The fraud dataset is historical and highly imbalanced. The V1-V28 features are anonymized, which also limits how much business meaning can be attached to individual model inputs.

A high fraud probability does not prove that a transaction is fraudulent. In a real system, model output would need to be combined with additional context and reviewed under the organization's fraud procedures.

I compared precision and recall because the tradeoff matters in this problem. Missing fraud is costly, but generating too many false positives can also create unnecessary customer friction and analyst workload.

## Security-alert limitations

The security logs are synthetic and the detection thresholds are project assumptions. The rules are designed to surface activity for review, not confirm that an account or device is compromised.

Each rule can have a benign explanation, so the alert output includes evidence and an analyst note rather than an automatic remediation action.

## LLM boundaries

The LLM receives only the structured alert information supplied by the program. The prompt tells it to:

- use only the provided evidence
- avoid claiming that fraud or compromise is confirmed
- separate observations from possible explanations
- state uncertainty and limitations
- recommend analyst checks rather than automatic blocking or account actions

The program also validates that the response contains the required sections before saving it.

## Human review

The project keeps a human in the decision loop. A model score, rule-based alert, or LLM explanation should be treated as supporting information for an analyst, not as authorization to block a transaction, disable an account, or take another high-impact action.

## Privacy and secrets

The repository uses synthetic security events and does not include real customer or employee data. API keys are read from an environment variable and are excluded from version control through `.gitignore`.
