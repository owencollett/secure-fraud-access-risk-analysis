import pandas as pd

from src.security_detector import (
    detect_failed_login_bursts,
    detect_unusual_access_time,
    detect_privilege_mismatch,
    detect_unusual_network_context,
)


def test_failed_login_detection():

    events = []

    for number in range(5):
        events.append(
            {
                "event_id": f"evt_{number}",
                "timestamp": pd.Timestamp(
                    "2026-09-01 12:00:00"
                )
                + pd.Timedelta(
                    minutes=number
                ),
                "user_id": "user_001",
                "source_ip": "10.0.0.10",
                "success": False,
            }
        )

    df = pd.DataFrame(events)

    alerts = detect_failed_login_bursts(df)

    assert len(alerts) >= 1

    assert (
        alerts[0]["rule_name"]
        == "Repeated Failed Logins"
    )


def test_unusual_access_time():

    df = pd.DataFrame(
        [
            {
                "event_id": "evt_001",
                "timestamp": pd.Timestamp(
                    "2026-09-01 02:00:00"
                ),
                "user_id": "user_001",
                "success": True,
            }
        ]
    )

    alerts = detect_unusual_access_time(df)

    assert len(alerts) == 1


def test_privilege_mismatch():

    df = pd.DataFrame(
        [
            {
                "event_id": "evt_001",
                "user_id": "user_001",
                "access_level": "standard",
                "required_access_level": "admin",
            }
        ]
    )

    alerts = detect_privilege_mismatch(df)

    assert len(alerts) == 1

    assert (
        alerts[0]["rule_name"]
        == "Privilege Mismatch"
    )


def test_unusual_network_context():

    df = pd.DataFrame(
        [
            {
                "event_id": "evt_001",
                "destination_port": 23,
                "protocol": "TCP",
            }
        ]
    )

    alerts = detect_unusual_network_context(df)

    assert len(alerts) == 1

    assert (
        alerts[0]["rule_name"]
        == "Unusual Network Context"
    )