from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.features import build_features
from src.model import detect_anomalies
from src.parser import load_logs


SAMPLE_DATA_PATH = Path("data/sample_logs.csv")


st.set_page_config(
    page_title="AI Log Anomaly Detector",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI Log Anomaly Detector")
st.write(
    "Upload a CSV log file or use the included sample data to detect suspicious activity."
)

with st.sidebar:
    st.header("Settings")
    contamination = st.slider(
        "Expected anomaly percentage",
        min_value=1,
        max_value=25,
        value=8,
        help="Higher values flag more rows as suspicious.",
    ) / 100

    uploaded_file = st.file_uploader("Upload log CSV", type=["csv"])

try:
    if uploaded_file is not None:
        logs = load_logs(uploaded_file)
        st.success("Uploaded log file loaded successfully.")
    else:
        logs = load_logs(SAMPLE_DATA_PATH)
        st.info("Using included sample log data.")

    features = build_features(logs)
    results = detect_anomalies(features, contamination=contamination)
    anomalies = results[results["is_anomaly"]].copy()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw log rows", f"{len(logs):,}")
    col2.metric("Grouped windows", f"{len(features):,}")
    col3.metric("Anomalies found", f"{len(anomalies):,}")
    col4.metric("Unique IPs", f"{logs['ip'].nunique():,}")

    st.divider()

    st.subheader("Anomaly Results")
    st.write(
        "Rows marked `True` are suspicious time-window/IP combinations based on unusual behavior."
    )

    display_columns = [
        "minute",
        "ip",
        "request_count",
        "error_count",
        "failed_login_count",
        "avg_response_time_ms",
        "p95_response_time_ms",
        "unique_endpoints",
        "error_rate",
        "failed_login_rate",
        "anomaly_score",
        "is_anomaly",
    ]

    st.dataframe(
        results[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    report_csv = anomalies.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download anomaly report",
        data=report_csv,
        file_name="anomaly_report.csv",
        mime="text/csv",
    )

    st.divider()

    st.subheader("Traffic Over Time")
    traffic_by_minute = (
        logs.groupby("minute")
        .size()
        .reset_index(name="request_count")
        .sort_values("minute")
    )

    fig, ax = plt.subplots()
    ax.plot(traffic_by_minute["minute"], traffic_by_minute["request_count"])
    ax.set_xlabel("Time")
    ax.set_ylabel("Requests")
    ax.set_title("Requests Per Minute")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    st.subheader("Top Suspicious IPs")
    if anomalies.empty:
        st.write("No anomalies found with the current settings.")
    else:
        suspicious_ips = (
            anomalies.groupby("ip")
            .size()
            .reset_index(name="anomaly_count")
            .sort_values("anomaly_count", ascending=False)
        )

        st.bar_chart(suspicious_ips.set_index("ip"))

    with st.expander("View raw logs"):
        st.dataframe(logs, use_container_width=True, hide_index=True)

except Exception as exc:
    st.error(f"Something went wrong: {exc}")
    st.write(
        "Check that your CSV has the required columns listed in the README."
    )
