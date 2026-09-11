from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd


OUTPUT_PATH = Path("data/security_logs.csv")

random.seed(42)

USERS = [
    ("user_001", "standard", "device_001"),
    ("user_002", "standard", "device_002"),
    ("user_003", "standard", "device_003"),
    ("analyst_001", "elevated", "device_004"),
    ("admin_001", "admin", "device_005"),
]


def main():
    events = []

    def add_event(
        timestamp,
        user_id,
        source_ip,
        event_type,
        success,
        destination_port,
        protocol,
        device_id,
        access_level,
        required_access_level,
    ):
        events.append(
            {
                "event_id": f"evt_{len(events) + 1:04d}",
                "timestamp": timestamp.isoformat(),
                "user_id": user_id,
                "source_ip": source_ip,
                "event_type": event_type,
                "success": success,
                "destination_port": destination_port,
                "protocol": protocol,
                "device_id": device_id,
                "access_level": access_level,
                "required_access_level": required_access_level,
            }
        )

    base_date = datetime(2026, 9, 1)

    # Create normal activity
    for _ in range(120):
        user_id, access_level, device_id = random.choice(USERS)

        timestamp = base_date + timedelta(
            days=random.randint(0, 2),
            hours=random.randint(8, 17),
            minutes=random.randint(0, 59),
        )

        event_type = random.choice(
            ["login", "api_request", "data_view"]
        )

        success = True

        if event_type == "login" and random.random() < 0.05:
            success = False

        add_event(
            timestamp=timestamp,
            user_id=user_id,
            source_ip=f"10.0.0.{random.randint(10, 60)}",
            event_type=event_type,
            success=success,
            destination_port=443,
            protocol="TCP",
            device_id=device_id,
            access_level=access_level,
            required_access_level="standard",
        )

    # Suspicious example 1:
    # repeated failed logins
    failed_login_start = datetime(2026, 9, 2, 21, 30)

    for minute in range(6):
        add_event(
            timestamp=failed_login_start + timedelta(minutes=minute),
            user_id="user_003",
            source_ip="203.0.113.50",
            event_type="login",
            success=False,
            destination_port=443,
            protocol="TCP",
            device_id="device_003",
            access_level="standard",
            required_access_level="standard",
        )

    # Suspicious example 2:
    # successful login at an unusual time
    add_event(
        timestamp=datetime(2026, 9, 3, 2, 15),
        user_id="user_002",
        source_ip="198.51.100.77",
        event_type="login",
        success=True,
        destination_port=443,
        protocol="TCP",
        device_id="device_002",
        access_level="standard",
        required_access_level="standard",
    )

    # Suspicious example 3:
    # standard user attempts admin action
    add_event(
        timestamp=datetime(2026, 9, 3, 14, 0),
        user_id="user_001",
        source_ip="10.0.0.25",
        event_type="admin_action",
        success=False,
        destination_port=443,
        protocol="TCP",
        device_id="device_001",
        access_level="standard",
        required_access_level="admin",
    )

    # Suspicious example 4:
    # unusual destination port
    add_event(
        timestamp=datetime(2026, 9, 3, 15, 30),
        user_id="analyst_001",
        source_ip="10.0.0.30",
        event_type="network_connection",
        success=True,
        destination_port=23,
        protocol="TCP",
        device_id="device_004",
        access_level="elevated",
        required_access_level="standard",
    )

    df = pd.DataFrame(events)

    df = df.sort_values("timestamp")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"Created {len(df)} synthetic security events."
    )

    print(
        f"Saved to {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()