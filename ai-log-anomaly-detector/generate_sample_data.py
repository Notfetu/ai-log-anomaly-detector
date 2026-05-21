from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_PATH = Path("data/sample_logs.csv")


def random_ip() -> str:
    return f"192.168.1.{random.randint(2, 240)}"


def generate_sample_logs(rows: int = 1200) -> list[dict]:
    random.seed(42)

    start = datetime(2026, 5, 21, 9, 0, 0)
    endpoints = ["/", "/login", "/dashboard", "/api/users", "/api/orders", "/settings"]
    methods = ["GET", "POST"]
    user_agents = ["Mozilla/5.0", "Chrome/120.0", "Safari/17.0", "curl/8.0"]

    logs = []

    for i in range(rows):
        timestamp = start + timedelta(seconds=random.randint(0, 7200))
        ip = random_ip()
        endpoint = random.choice(endpoints)
        method = random.choice(methods)

        status_code = random.choices(
            [200, 201, 204, 301, 400, 401, 403, 404, 500],
            weights=[55, 8, 5, 5, 6, 5, 3, 8, 5],
            k=1,
        )[0]

        response_time = max(20, random.gauss(180, 70))
        bytes_sent = max(300, random.gauss(5000, 1700))
        event_type = "normal"

        logs.append(
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": ip,
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time_ms": round(response_time, 2),
                "bytes_sent": round(bytes_sent, 2),
                "user_agent": random.choice(user_agents),
                "event_type": event_type,
            }
        )

    # Inject anomaly 1: brute-force login behavior.
    attacker_ip = "10.10.10.99"
    attack_start = start + timedelta(minutes=47)
    for i in range(90):
        timestamp = attack_start + timedelta(seconds=i * 2)
        logs.append(
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": attacker_ip,
                "method": "POST",
                "endpoint": "/login",
                "status_code": random.choice([401, 403]),
                "response_time_ms": round(random.gauss(90, 20), 2),
                "bytes_sent": round(random.gauss(900, 120), 2),
                "user_agent": "python-requests/2.31",
                "event_type": "failed_login_burst",
            }
        )

    # Inject anomaly 2: traffic spike from one IP.
    spike_ip = "172.16.50.20"
    spike_start = start + timedelta(minutes=83)
    for i in range(140):
        timestamp = spike_start + timedelta(seconds=i)
        logs.append(
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": spike_ip,
                "method": "GET",
                "endpoint": random.choice(["/api/users", "/api/orders", "/dashboard"]),
                "status_code": random.choice([200, 200, 200, 500]),
                "response_time_ms": round(random.gauss(450, 140), 2),
                "bytes_sent": round(random.gauss(11000, 2500), 2),
                "user_agent": "curl/8.0",
                "event_type": "traffic_spike",
            }
        )

    # Inject anomaly 3: slow error-heavy behavior.
    bad_service_ip = "203.0.113.77"
    slow_start = start + timedelta(minutes=105)
    for i in range(60):
        timestamp = slow_start + timedelta(seconds=i * 3)
        logs.append(
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": bad_service_ip,
                "method": "GET",
                "endpoint": "/api/orders",
                "status_code": random.choice([500, 500, 502, 503]),
                "response_time_ms": round(random.gauss(1400, 220), 2),
                "bytes_sent": round(random.gauss(2500, 400), 2),
                "user_agent": "Mozilla/5.0",
                "event_type": "server_error_burst",
            }
        )

    return sorted(logs, key=lambda row: row["timestamp"])


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    logs = generate_sample_logs()
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(logs[0].keys()))
        writer.writeheader()
        writer.writerows(logs)

    print(f"Generated {len(logs)} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
