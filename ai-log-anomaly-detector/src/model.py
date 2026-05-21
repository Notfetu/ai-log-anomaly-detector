from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.features import get_model_columns


def detect_anomalies(
    features: pd.DataFrame,
    contamination: float = 0.08,
    random_state: int = 42,
) -> pd.DataFrame:
    """Run Isolation Forest and return features with anomaly labels.

    contamination means the expected percentage of anomalies.
    Example:
        0.08 means roughly 8% of rows may be flagged as unusual.
    """
    if features.empty:
        return features.copy()

    model_columns = get_model_columns()
    missing = [col for col in model_columns if col not in features.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    X = features[model_columns].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
    )

    predictions = model.fit_predict(X_scaled)
    scores = model.decision_function(X_scaled)

    results = features.copy()
    results["anomaly_score"] = scores
    results["is_anomaly"] = predictions == -1

    return results.sort_values(["is_anomaly", "anomaly_score"], ascending=[False, True])
