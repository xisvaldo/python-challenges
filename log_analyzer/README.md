# Log Analyzer

## Overview

**Log Analyzer** is a Python-based tool designed to parse, analyze, and summarize HTTP server logs. The system reads log
entries from a file, validates each log entry against business rules, and counts HTTP error occurrences specifically
from
the client's public IP. The final results are written to a CSV file for further inspection.

Key features:

- Strict validation of log entries (timestamp, IP, HTTP method, endpoint, status code).
- Streaming log parsing to handle large files efficiently without consuming excessive memory.
- Counting HTTP errors per IP, focusing on the client’s public IP.
- Automatic generation of sample log files for testing end-to-end pipelines.
- Logging of all processing steps and errors to separate info and error logs.

---

## Project Structure

```
log_analyzer/
├── models/
├── services/
├── utils/
├── logs/
├── outputs/
├── tests/
├── main.py
├── requeriments.txt
└── README.md
```

- `models/log_entry.py`: Contains the `LogEntry` domain class, which enforces all business validation rules.
- `services/`: Each service has a single responsibility:
    - `file_reader.py`: Streams log lines from a file.
    - `file_writer.py`: Writes log entries to CSV.
    - `get_public_ip.py`: Retrieves the client’s public IP.
    - `log_entry_parser.py`: Parses lines into `LogEntry` objects.
    - `error_counter.py`: Counts HTTP error occurrences for the client IP.
- `utils/logger.py`: Configures logging with separate handlers for info and error messages.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xisvaldo/python-challenges.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

If you have a log file to be processed, you can set the `-i, --input_file` argument with the file path:

```bash
cd python-challenges
python -m log_analyzer.main -i <input_file_path>
```

(Optional)

If you want to generate a random sample file that mixes your actual IP with random data, you can use:

```bash
cd python-challenges
python -m log_analyzer.main --generate_sample_file --sample_size 100000
```

- `--generate_sample_file`: generates a log file (at `/outputs/sample_log.txt`) with valid and intentionally malformed
  data;
- `--sample_size`: number of log entries to be generated (**default if not set: 100.000**).

### Test execution

```bash
cd python-challenges
python -m unittest discover -s log_analyzer/tests
```

---

## Input/Output format

Example input:

```bash
2026-03-17 18:30:00 | 192.168.1.10 | GET /home | 200
2026-03-17 18:31:00 | 192.168.1.10 | POST /login | 401
2026-03-17 18:32:00 | 8.8.8.8 | GET /dashboard | 500
```

Example output (`/outputs/results.csv`):

```bash
ip,status_code
192.168.1.10,200
192.168.1.10,401
8.8.8.8,500
```

---

## Logging

All generated logs are stored within the `/logs` directory.

- `info.log`: Contains general information such as number of lines processed, results written, and pipeline progress.
- `error.log`: Contains validation errors and exceptions, including lines that failed parsing.