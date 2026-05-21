from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


REQUIRED_COLUMNS = {
    "timestamp",
    "ip",
    "method",
    "endpoint",
    "status_code",
    "response_time_ms",
    "bytes_sent",
    "user_agent",
    "event_type",
}


def load_logs(file_path_or_buffer: Union[str, Path, object]) -> pd.DataFrame:
    """Load log data from a CSV file path or uploaded file buffer.

    Expected columns:
        timestamp, ip, method, endpoint, status_code,
        response_time_ms, bytes_sent, user_agent, event_type
    """
    df = pd.read_csv(file_path_or_buffer)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce")
    df["response_time_ms"] = pd.to_numeric(df["response_time_ms"], errors="coerce")
    df["bytes_sent"] = pd.to_numeric(df["bytes_sent"], errors="coerce")

    df = df.dropna(
        subset=[
            "timestamp",
            "ip",
            "status_code",
            "response_time_ms",
            "bytes_sent",
        ]
    )

    df["status_code"] = df["status_code"].astype(int)
    df["response_time_ms"] = df["response_time_ms"].astype(float)
    df["bytes_sent"] = df["bytes_sent"].astype(float)

    df["minute"] = df["timestamp"].dt.floor("min")
    df["is_error"] = df["status_code"] >= 400
    df["is_failed_login"] = (
        df["endpoint"].str.contains("login", case=False, na=False)
        & df["status_code"].isin([401, 403])
    )

    return df.sort_values("timestamp").reset_index(drop=True)
