from pathlib import Path

from .security_log_loader import load_security_logs
from .security_detector import run_all_detectors
from .llm_analyst import explain_alert


DATA_PATH = Path(
    "data/security_logs.csv"
)

REPORT_PATH = Path(
    "reports/llm_examples.md"
)


def main():

    logs = load_security_logs(
        DATA_PATH
    )

    alerts = run_all_detectors(
        logs
    )

    print(
        f"Loaded {len(alerts)} Phase 4 alerts."
    )

    # Add one deliberately benign-looking case
    # so the LLM must discuss uncertainty.
    benign_example = {
        "alert_id": "alert_benign_example",
        "rule_name": "Unusual Access Time",
        "severity": "low",
        "event_ids": ["evt_benign_001"],
        "evidence": (
            "admin_001 logged in at 5:30 AM. "
            "The event occurred outside the project's "
            "assumed normal working hours."
        ),
        "analyst_note": (
            "Synthetic example representing possible "
            "scheduled maintenance."
        ),
    }

    alerts.append(
        benign_example
    )

    # We need at least five examples.
    selected_alerts = alerts[:5]

    if len(selected_alerts) < 5:
        raise ValueError(
            "Fewer than five alerts are available."
        )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_sections = [
        "# LLM Analyst Examples\n"
    ]

    for number, alert in enumerate(
        selected_alerts,
        start=1
    ):

        print(
            f"Analyzing alert {number} of "
            f"{len(selected_alerts)}..."
        )

        explanation = explain_alert(
            alert
        )

        report_sections.append(
            f"""
## Example {number}

**Alert ID:** {alert.get("alert_id")}

**Rule:** {alert.get("rule_name")}

**Severity:** {alert.get("severity")}

**Original Evidence:**

{alert.get("evidence")}

### LLM Analyst Explanation

{explanation}

---
"""
        )

    REPORT_PATH.write_text(
        "\n".join(report_sections),
        encoding="utf-8"
    )

    print(
        f"\nLLM examples saved to {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()