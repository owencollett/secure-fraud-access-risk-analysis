import pandas as pd
import pytest

from src.security_log_loader import load_security_logs


def make_valid_security_log():

    return pd.DataFrame(
        [
            {
                "event_id": "evt_001",
                "timestamp": "2026-09-01T12:00:00",
                "user_id": "user_001",
                "source_ip": "10.0.0.10",
                "event_type": "login",
                "success": True,
                "destination_port": 443,
                "protocol": "TCP",
                "device_id": "device_001",
                "access_level": "standard",
                "required_access_level": "standard",
            }
        ]
    )


def test_valid_security_log(tmp_path):

    df = make_valid_security_log()

    file_path = tmp_path / "security.csv"

    df.to_csv(
        file_path,
        index=False
    )

    loaded = load_security_logs(
        file_path
    )

    assert len(loaded) == 1


def test_missing_column(tmp_path):

    df = make_valid_security_log()

    df = df.drop(
        columns=["source_ip"]
    )

    file_path = tmp_path / "security.csv"

    df.to_csv(
        file_path,
        index=False
    )

    with pytest.raises(ValueError):
        load_security_logs(file_path)


def test_invalid_protocol(tmp_path):

    df = make_valid_security_log()

    df.loc[0, "protocol"] = "BAD"

    file_path = tmp_path / "security.csv"

    df.to_csv(
        file_path,
        index=False
    )

    with pytest.raises(ValueError):
        load_security_logs(file_path)


def test_bad_timestamp(tmp_path):

    df = make_valid_security_log()

    df.loc[0, "timestamp"] = "not-a-date"

    file_path = tmp_path / "security.csv"

    df.to_csv(
        file_path,
        index=False
    )

    with pytest.raises(ValueError):
        load_security_logs(file_path)