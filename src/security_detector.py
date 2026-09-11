from datetime import timedelta


ACCESS_LEVELS = {
    "standard": 1,
    "elevated": 2,
    "admin": 3,
}


def detect_failed_login_bursts(
    df,
    threshold=5,
    window_minutes=10,
):
    alerts = []

    failed = df[
        df["success"] == False
    ].sort_values("timestamp")

    grouped = failed.groupby(
        ["user_id", "source_ip"]
    )

    for (user_id, source_ip), group in grouped:

        group = group.sort_values("timestamp")

        times = group["timestamp"].tolist()

        left = 0

        for right in range(len(times)):

            while (
                times[right] - times[left]
                > timedelta(minutes=window_minutes)
            ):
                left += 1

            count = right - left + 1

            if count >= threshold:

                matching_events = group.iloc[
                    left:right + 1
                ]

                alerts.append(
                    {
                        "rule_name": "Repeated Failed Logins",
                        "severity": "high",
                        "evidence": (
                            f"{count} failed logins for "
                            f"{user_id} from {source_ip} "
                            f"within {window_minutes} minutes."
                        ),
                        "event_ids": matching_events[
                            "event_id"
                        ].tolist(),
                        "analyst_note": (
                            "Investigate account activity "
                            "and source IP."
                        ),
                    }
                )

                break

    return alerts


def detect_unusual_access_time(df):
    alerts = []

    successful_events = df[
        df["success"] == True
    ]

    for _, row in successful_events.iterrows():

        hour = row["timestamp"].hour

        if hour < 6 or hour >= 22:

            alerts.append(
                {
                    "rule_name": "Unusual Access Time",
                    "severity": "medium",
                    "evidence": (
                        f"{row['user_id']} successfully "
                        f"accessed the system at "
                        f"{row['timestamp']}."
                    ),
                    "event_ids": [
                        row["event_id"]
                    ],
                    "analyst_note": (
                        "Verify whether off-hours "
                        "activity was expected."
                    ),
                }
            )

    return alerts


def detect_privilege_mismatch(df):
    alerts = []

    for _, row in df.iterrows():

        user_level = ACCESS_LEVELS[
            row["access_level"]
        ]

        required_level = ACCESS_LEVELS[
            row["required_access_level"]
        ]

        if user_level < required_level:

            alerts.append(
                {
                    "rule_name": "Privilege Mismatch",
                    "severity": "high",
                    "evidence": (
                        f"{row['user_id']} has "
                        f"{row['access_level']} access but "
                        f"attempted an action requiring "
                        f"{row['required_access_level']} access."
                    ),
                    "event_ids": [
                        row["event_id"]
                    ],
                    "analyst_note": (
                        "Review account permissions "
                        "and attempted activity."
                    ),
                }
            )

    return alerts


def detect_unusual_network_context(df):
    alerts = []

    for _, row in df.iterrows():

        expected_port = 443
        expected_protocol = "TCP"

        if (
            row["destination_port"] != expected_port
            or row["protocol"] != expected_protocol
        ):

            alerts.append(
                {
                    "rule_name": "Unusual Network Context",
                    "severity": "medium",
                    "evidence": (
                        f"Connection used port "
                        f"{row['destination_port']} "
                        f"with protocol "
                        f"{row['protocol']}."
                    ),
                    "event_ids": [
                        row["event_id"]
                    ],
                    "analyst_note": (
                        "Determine whether the network "
                        "connection was authorized."
                    ),
                }
            )

    return alerts


def run_all_detectors(df):

    alerts = []

    alerts.extend(
        detect_failed_login_bursts(df)
    )

    alerts.extend(
        detect_unusual_access_time(df)
    )

    alerts.extend(
        detect_privilege_mismatch(df)
    )

    alerts.extend(
        detect_unusual_network_context(df)
    )

    for number, alert in enumerate(
        alerts,
        start=1
    ):
        alert["alert_id"] = (
            f"alert_{number:03d}"
        )

    return alerts