# Zookeeper Schedule Manager

[![CI](https://github.com/FuaadBashi/Zoo-Keeper-App/actions/workflows/ci.yml/badge.svg)](https://github.com/FuaadBashi/Zoo-Keeper-App/actions/workflows/ci.yml)

A console tool for running a zoo's day: see every keeper's schedule, look up an enclosure's
feeding times, check keepers in (logging anyone late, to the minute), and record completed feeds.

```
Enter your choice: 3
Zookeeper ID: k001
Check-in time (HH:MM:SS): 08:40:00
Alex is 40 minute(s) late; this has been logged.
```

## Highlights

- **Tolerant loading.** The schedule loader skips an optional header and blank lines. It reports
  bad rows with their line number and keeps going rather than crashing.
- **Typed data.** Keepers are frozen dataclasses holding real `datetime.time` values, parsed once
  at load time rather than re-parsed from strings.
- **Accurate lateness.** Minutes late are computed from the full time, so 08:59 for an 08:00
  start is 59 minutes late.
- **Audit logs.** Late check-ins and completed feeds are appended to CSV files in `logs/`.
- **Separation and tests.** `zoo.py` is pure domain logic. `main.py` is the menu. Tests use
  pytest's `tmp_path`, so they never touch real logs.

## Getting started

Requires Python 3.10+. No third-party packages are needed to run it.

```bash
git clone https://github.com/FuaadBashi/Zoo-Keeper-App.git
cd Zoo-Keeper-App
python3 main.py
```

A sample `zoo_schedule.csv` with five fictional keepers is included. Use `--schedule` to load your
own and `--log-dir` to choose where logs go. The file is semicolon-separated:

```
keeper_id;name;enclosure;feed_am;feed_pm;start_time
K001;Alex;Lions;09:00:00;16:00:00;08:00:00
```

## Tests

```bash
pip install pytest ruff
pytest
ruff format --check . && ruff check .
```
