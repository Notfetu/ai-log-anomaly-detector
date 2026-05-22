# AI Log Anomaly Detector

A Python project that analyzes server/application logs and flags suspicious behavior using machine learning.

This project is built to show practical skills in:

- Python programming
- Data cleaning with Pandas
- Feature engineering
- Machine learning with Scikit-learn
- Security/DevOps thinking
- Dashboard building with Streamlit

## Project Overview

The app reads log data, groups activity by IP address and time window, creates security-focused features, and uses an Isolation Forest model to detect abnormal behavior.

Example suspicious patterns:

- Sudden traffic spikes
- Too many failed login attempts
- High error rates
- Slow response times
- Unusual IP behavior

## Features

- Load sample log data or upload your own CSV
- Parse timestamps, IPs, status codes, endpoints, and event types
- Build features by `timestamp minute + IP address`
- Run anomaly detection with Isolation Forest
- View summary metrics
- Display suspicious log windows
- Download an anomaly report as CSV
- Includes a sample data generator

## Project Structure

```text
ai-log-anomaly-detector/
│
├── app.py
├── generate_sample_data.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── sample_logs.csv
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── features.py
│   ├── model.py
│   └── report.py
│
└── tests/
    └── test_features.py
```

## Setup

### 1. Create a virtual environment

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Generate sample data

The repo already includes sample data, but you can regenerate it:

```powershell
python generate_sample_data.py
```

### 4. Run the dashboard

```powershell
python -m streamlit run app.py
```

## Expected CSV Format

Your CSV should include these columns:

```text
timestamp, ip, method, endpoint, status_code, response_time_ms, bytes_sent, user_agent, event_type
```

Example:

```csv
timestamp,ip,method,endpoint,status_code,response_time_ms,bytes_sent,user_agent,event_type
2026-05-21 10:00:00,192.168.1.10,GET,/login,200,123,5420,Mozilla/5.0,normal
```

## How the Model Works

The project uses `IsolationForest`, an unsupervised anomaly detection algorithm. Instead of needing labeled examples of attacks, it learns what normal behavior usually looks like and flags rows that are statistically unusual.

The model looks at features such as:

- Number of requests per minute
- Error count
- Failed login count
- Average response time
- 95th percentile response time
- Total bytes sent
- Number of unique endpoints
- Error rate
- Failed login rate

## Future Improvements

Good next steps for this project:

- Add support for Apache/Nginx raw log parsing
- Add user authentication to the dashboard
- Add Docker support
- Store reports in SQLite
- Add more charts
- Compare multiple anomaly detection models
- Send email alerts for high-risk anomalies
