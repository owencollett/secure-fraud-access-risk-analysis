import pytest

from src.llm_analyst import (
    validate_llm_output,
    explain_alert,
)


VALID_OUTPUT = """
Summary
Test summary.

Evidence
Test evidence.

Possible Explanations
Test explanation.

Recommended Analyst Checks
Test checks.

Uncertainty / Limitations
Test limitations.
"""


def test_valid_llm_output():

    result = validate_llm_output(
        VALID_OUTPUT
    )

    assert "Summary" in result

    assert (
        "Uncertainty / Limitations"
        in result
    )


def test_missing_llm_section():

    bad_output = """
Summary
Test summary.

Evidence
Test evidence.
"""

    with pytest.raises(ValueError):
        validate_llm_output(
            bad_output
        )


def test_missing_api_key(monkeypatch):

    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False
    )

    alert = {
        "rule_name": "Test Alert",
        "severity": "low",
        "event_ids": ["evt_001"],
        "evidence": "Test evidence.",
        "analyst_note": "Test.",
    }

    with pytest.raises(ValueError):
        explain_alert(alert)