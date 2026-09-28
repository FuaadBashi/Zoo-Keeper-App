"""Zookeeper schedules, feeding times, check-ins and feed records."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path

TIME_FORMAT = "%H:%M:%S"


def parse_time(text: str) -> time:
    """Parses HH:MM:SS; raises ValueError otherwise."""
    return datetime.strptime(text.strip(), TIME_FORMAT).time()


def minutes_late(start: time, check_in: time) -> int:
    """Whole minutes after the shift start; 0 if on time or early.

    The original compared hours only, so arriving at 08:59 for an 08:00 start counted as on time.
    """
    start_s = start.hour * 3600 + start.minute * 60 + start.second
    check_s = check_in.hour * 3600 + check_in.minute * 60 + check_in.second
    return max(0, (check_s - start_s) // 60)


@dataclass(frozen=True)
class Zookeeper:
    keeper_id: str
    name: str
    enclosure: str
    feed_am: time
    feed_pm: time
    start_time: time


@dataclass
class LoadResult:
    keepers: dict[str, Zookeeper]
    problems: list[str]


def load_schedule(path: Path) -> LoadResult:
    """Reads 'id;name;enclosure;feed_am;feed_pm;start' rows. Bad rows are reported, not fatal."""
    keepers: dict[str, Zookeeper] = {}
    problems: list[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.reader(f, delimiter=";"), start=1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if row[0].strip().lower() == "keeper_id":
                continue  # optional header
            if len(row) != 6:
                problems.append(f"line {line_no}: expected 6 fields, got {len(row)}")
                continue
            keeper_id, name, enclosure, am, pm, start = (cell.strip() for cell in row)
            try:
                keepers[keeper_id] = Zookeeper(
                    keeper_id, name, enclosure, parse_time(am), parse_time(pm), parse_time(start)
                )
            except ValueError:
                problems.append(f"line {line_no}: times must be HH:MM:SS")
    return LoadResult(keepers, problems)


class Zoo:
    def __init__(self, keepers: dict[str, Zookeeper], log_dir: Path):
        self.keepers = keepers
        self.log_dir = log_dir

    def keeper(self, keeper_id: str) -> Zookeeper | None:
        return self.keepers.get(keeper_id.strip().upper())

    def keepers_for(self, enclosure: str) -> list[Zookeeper]:
        wanted = enclosure.strip().lower()
        return [k for k in self.keepers.values() if k.enclosure.lower() == wanted]

    def enclosures(self) -> list[str]:
        return sorted({k.enclosure for k in self.keepers.values()})

    def check_in(self, keeper: Zookeeper, at: time, on: datetime) -> int:
        """Returns minutes late, logging late arrivals to late_checkin.csv."""
        late = minutes_late(keeper.start_time, at)
        if late:
            self._append(
                "late_checkin.csv",
                [on.date().isoformat(), keeper.keeper_id, keeper.name, at.isoformat(), late],
            )
        return late

    def record_feed(self, enclosure: str, session: str, on: datetime) -> None:
        """Appends to feed_log.csv; feeds used to be printed and forgotten."""
        self._append("feed_log.csv", [on.isoformat(timespec="seconds"), enclosure, session])

    def _append(self, filename: str, row: list) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        with (self.log_dir / filename).open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)
