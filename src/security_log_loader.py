from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "event_id",
    "timestamp",
    "user_id",
    "source_ip",
    "event_type",
    "success",
    "destination_port",
    "protocol",
    "device_id",
    "access_level",
    "required_access_level",
]

VALID_PROTOCOLS = {
    "TCP",
    "UDP",
}

VALID_ACCESS_LEVELS = {
    "standard",
    "elevated",
    "admin",
}


def load_security_logs(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Security log file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Validate timestamps
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="raise"
    )

    # Validate protocol
    df["protocol"] = (
        df["protocol"]
        .astype(str)
        .str.upper()
    )

    invalid_protocols = set(df["protocol"]) - VALID_PROTOCOLS

    if invalid_protocols:
        raise ValueError(
            f"Invalid protocols: {invalid_protocols}"
        )

    # Validate access levels
    access_values = set(df["access_level"])
    required_values = set(df["required_access_level"])

    invalid_access = (
        access_values | required_values
    ) - VALID_ACCESS_LEVELS

    if invalid_access:
        raise ValueError(
            f"Invalid access levels: {invalid_access}"
        )

    # Validate ports
    df["destination_port"] = pd.to_numeric(
        df["destination_port"],
        errors="raise"
    ).astype(int)

    if not df["destination_port"].between(
        1,
        65535
    ).all():
        raise ValueError(
            "Destination ports must be between 1 and 65535."
        )

    # Make sure success contains True/False
    if not pd.api.types.is_bool_dtype(df["success"]):

        converted = (
            df["success"]
            .astype(str)
            .str.lower()
            .map(
                {
                    "true": True,
                    "false": False,
                }
            )
        )

        if converted.isna().any():
            raise ValueError(
                "Success column must contain True or False."
            )

        df["success"] = converted

    return df