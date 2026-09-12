# Secure Fraud & Access Risk Analysis

This project combines three related pieces of analysis in one Python repository: credit-card fraud detection, rule-based security-event monitoring, and LLM-assisted alert explanations.

The goal was to build a small end-to-end prototype rather than only train a model. The project includes data validation, preprocessing, model comparison, security detection rules, LLM output checks, and automated tests.

> This is an educational prototype using public or synthetic data. It is not intended for real banking, fraud-prevention, or cybersecurity decisions.

## What the project does

### Fraud detection

The fraud workflow loads and validates transaction data, creates stratified train/validation/test splits, preprocesses the features, and compares several models:

- Logistic Regression
- class-balanced Logistic Regression
- Random Forest
- Random Forest with a log-transformed transaction amount

The final Random Forest model produced the strongest overall validation results and was evaluated once on the held-out test set. The test results were:

- Precision: **0.9508**
- Recall: **0.7838**
- F1: **0.8593**
- PR-AUC: **0.8203**

More detail is available in `reports/fraud_model_results.md`.

### Security-event analysis

The security portion uses synthetic authentication and network-style logs. It checks for:

- repeated failed logins
- successful access at unusual hours
- privilege mismatches
- unexpected port or protocol use

The rules create structured alerts for review rather than treating an alert as proof of an incident.

### LLM-assisted explanations

Security alerts can be passed to an LLM through the OpenAI API. The model is instructed to use only the supplied evidence, separate observations from possible explanations, state uncertainty, and leave decisions to a human analyst.

The response is also checked for a required structure before it is accepted. Example outputs are in `reports/llm_examples.md`.

## Project structure

```text
data/
    security_logs.csv
models/
notebooks/
    01_data_exploration.ipynb
reports/
    debugging_story.md
    fraud_model_results.md
    llm_examples.md
    responsible_ai_and_security.md
    security_findings.md
src/
    data_loader.py
    data_splitter.py
    generate_security_logs.py
    llm_analyst.py
    pipeline.py
    preprocessing.py
    run_llm_analysis.py
    run_security_analysis.py
    security_detector.py
    security_log_loader.py
    train_fraud_model.py
    validation.py
tests/
requirements.txt
```

## Testing

The repository includes pytest coverage for data loading, validation, preprocessing, model probability output, security-log validation, detection rules, LLM output structure, and missing API-key handling.

Run the tests with:

```bash
python -m pytest -q
```

## Setup

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

The original credit-card fraud dataset is not committed to the repository. Place it at `data/creditcard.csv` before running the fraud workflow.

To use the LLM component, set an `OPENAI_API_KEY` environment variable before running `src/run_llm_analysis.py`.

## Responsible use

The project uses synthetic security logs and does not contain real customer records, employee data, credentials, or private network data. Model predictions and security alerts are treated as signals for human review rather than automatic decisions.

See `reports/responsible_ai_and_security.md` for the main limitations and safeguards considered in the project.
