# Secure Fraud & Access Risk Analysis System

A Python-based portfolio project that combines fraud detection, cybersecurity log analysis, and LLM-assisted analyst explanations with responsible AI, privacy, and human-review controls.

This project was built as preparation for entry-level AI engineering and cybersecurity roles.

---

## Project Overview

The Secure Fraud & Access Risk Analysis System contains three main components:

1. A machine-learning system for detecting potentially fraudulent credit-card transactions.
2. A rule-based cybersecurity system for detecting suspicious authentication and access behavior.
3. An LLM-assisted analyst tool that explains security alerts using supplied evidence.

The project also documents responsible AI risks, security limitations, privacy considerations, and human escalation requirements.

This is an educational prototype.

It is not intended for real banking, fraud-prevention, or cybersecurity decisions.

# Testing and Quality Assurance

The project includes automated testing using pytest.

Tests cover:

- Fraud data loading
- Missing and malformed fraud data
- Fraud preprocessing
- Feature engineering
- Fraud model probability outputs
- Security-log validation
- Invalid protocols
- Invalid timestamps
- Repeated failed-login detection
- Unusual access-time detection
- Privilege mismatch detection
- Unusual network-context detection
- LLM output structure
- Missing API-key handling

Run the complete test suite with:

```bash
python -m pytest -q

## Current Project Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Repository setup and fraud data exploration | Complete |
| Phase 2 | Data validation and preprocessing pipeline | Complete |
| Phase 3 | Machine-learning model training and evaluation | Complete |
| Phase 4 | Cybersecurity log analysis and detection rules | Complete |
| Phase 5 | LLM-assisted security alert explanations | Complete |
| Phase 6 | Responsible AI, security, privacy, and escalation | Complete |
| Phase 7 | Testing, debugging, and final portfolio polish | Complete |

---

# System Architecture

```mermaid
flowchart TD

    A[Credit Card Fraud Dataset] --> B[Data Validation]
    B --> C[Train / Validation / Test Split]
    C --> D[Preprocessing]
    D --> E[Logistic Regression]
    D --> F[Random Forest]
    E --> G[Model Evaluation]
    F --> G
    G --> H[Final Fraud Prediction Results]

    I[Synthetic Security Logs] --> J[Security Log Validation]
    J --> K[Rule-Based Detection]
    K --> L[Structured Security Alerts]
    L --> M[LLM Analyst Explanation]
    M --> N[Human Analyst Review]

    O[Responsible AI / Security Controls] --> H
    O --> L
    O --> M
    O --> N