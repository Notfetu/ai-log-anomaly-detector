from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_anomaly_report(results: pd.DataFrame, output_path: str | Path) -> Path:
    """Save only anomalous rows to a CSV report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    anomalies = results[results["is_anomaly"]].copy()
    anomalies.to_csv(output_path, index=False)

    return output_path
