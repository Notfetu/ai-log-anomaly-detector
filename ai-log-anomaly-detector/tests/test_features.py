import pandas as pd

from src.features import build_features


def test_build_features_groups_by_minute_and_ip():
    logs = pd.DataFrame(
        {
            "minute": pd.to_datetime(
                [
                    "2026-05-21 09:00:00",
                    "2026-05-21 09:00:00",
                    "2026-05-21 09:01:00",
                ]
            ),
            "ip": ["1.1.1.1", "1.1.1.1", "2.2.2.2"],
            "is_error": [False, True, False],
            "is_failed_login": [False, True, False],
            "response_time_ms": [100, 300, 200],
            "bytes_sent": [1000, 2000, 1500],
            "endpoint": ["/", "/login", "/dashboard"],
        }
    )

    features = build_features(logs)

    assert len(features) == 2

    first_group = features[features["ip"] == "1.1.1.1"].iloc[0]
    assert first_group["request_count"] == 2
    assert first_group["error_count"] == 1
    assert first_group["failed_login_count"] == 1
    assert first_group["error_rate"] == 0.5
