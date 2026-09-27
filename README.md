# Zookeeper Schedule Manager

A Python console application for staff schedules, enclosure feeding times, keeper check-in, and feeding reports. The implementation models zookeepers and schedules.

## Run locally

Requires Python 3.10 or later. No third-party packages are needed.

```bash
git clone https://github.com/FuaadBashi/Zoo-Keeper-App.git
cd Zoo-Keeper-App
```

Create `zoo_schedule.csv` beside `main.py` with semicolon-separated rows and **no header**. For example, this fictional record contains keeper ID, name, enclosure, morning feed, afternoon feed, and shift start:

```text
K001;Alex;Lions;09:00:00;16:00:00;08:00:00
```

Then run:

```bash
python3 main.py
```

## Code to explore

[main.py](main.py) contains `Zookeeper`, `ZooSchedule`, and `ZooControl`, plus time validation and late-check-in logging.

## Current behavior

- Schedules are loaded from the local file; it is not included in the repository.
- Late check-ins append to `late_checkin.csv`.
- Lateness currently compares the hour component only.
- Feeding reports print a confirmation; they are not persisted.

These boundaries make the project suitable for exploring file input, inheritance, and console workflows.
