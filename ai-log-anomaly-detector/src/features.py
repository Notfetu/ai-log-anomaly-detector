from __future__ import annotations

import pandas as pd


def build_features(logs: pd.DataFrame) -> pd.DataFrame:
    """Create model-ready features grouped by minute and IP address."""
    if logs.empty:
        return pd.DataFrame()

    grouped = (
        logs.groupby(["minute", "ip"])
        .agg(
            request_count=("ip", "size"),
            error_count=("is_error", "sum"),
            failed_login_count=("is_failed_login", "sum"),
            avg_response_time_ms=("response_time_ms", "mean"),
            p95_response_time_ms=("response_time_ms", lambda x: x.quantile(0.95)),
            total_bytes_sent=("bytes_sent", "sum"),
            unique_endpoints=("endpoint", "nunique"),
        )
        .reset_index()
    )

    grouped["error_rate"] = grouped["error_count"] / grouped["request_count"]
    grouped["failed_login_rate"] = grouped["failed_login_count"] / grouped["request_count"]

    numeric_columns = [
        "request_count",
        "error_count",
        "failed_login_count",
        "avg_response_time_ms",
        "p95_response_time_ms",
        "total_bytes_sent",
        "unique_endpoints",
        "error_rate",
        "failed_login_rate",
    ]

    grouped[numeric_columns] = grouped[numeric_columns].fillna(0)

    return grouped


def get_model_columns() -> list[str]:
    """Columns used by the anomaly detection model."""
    return [
        "request_count",
        "error_count",
        "failed_login_count",
        "avg_response_time_ms",
        "p95_response_time_ms",
        "total_bytes_sent",
        "unique_endpoints",
        "error_rate",
        "failed_login_rate",
    ]
