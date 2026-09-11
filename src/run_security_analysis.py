from pathlib import Path

import pandas as pd

from .security_log_loader import load_security_logs
from .security_detector import run_all_detectors


DATA_PATH = Path(
    "data/security_logs.csv"
)

OUTPUT_PATH = Path(
    "reports/security_alerts.csv"
)


def main():

    logs = load_security_logs(
        DATA_PATH
    )

    print(
        f"Loaded {len(logs)} security events."
    )

    alerts = run_all_detectors(
        logs
    )

    print(
        f"Detected {len(alerts)} alerts."
    )

    for alert in alerts:

        print(
            f"\n{alert['alert_id']} | "
            f"{alert['rule_name']} | "
            f"{alert['severity']}"
        )

        print(
            f"Evidence: {alert['evidence']}"
        )

    alert_df = pd.DataFrame(alerts)

    if not alert_df.empty:

        alert_df["event_ids"] = (
            alert_df["event_ids"]
            .apply(
                lambda values: ", ".join(values)
            )
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    alert_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nAlerts saved to {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()