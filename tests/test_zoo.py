from datetime import datetime, time

import pytest

from zoo import Zoo, load_schedule, minutes_late


@pytest.fixture
def schedule(tmp_path):
    path = tmp_path / "schedule.csv"
    path.write_text(
        "keeper_id;name;enclosure;feed_am;feed_pm;start_time\n"
        "K001;Alex;Lions;09:00:00;16:00:00;08:00:00\n"
        "\n"
        "K002;Priya;Penguins;08:30:00;15:30:00;07:30:00\n"
    )
    return path


@pytest.fixture
def zoo(schedule, tmp_path):
    return Zoo(load_schedule(schedule).keepers, tmp_path / "logs")


def test_arriving_within_the_first_hour_still_counts_as_late():
    assert minutes_late(time(8, 0), time(8, 59)) == 59


def test_arriving_early_or_exactly_on_time_is_not_late():
    assert minutes_late(time(8, 0), time(7, 45)) == 0
    assert minutes_late(time(8, 0), time(8, 0)) == 0


def test_the_schedule_skips_the_header_and_blank_lines(schedule):
    result = load_schedule(schedule)

    assert set(result.keepers) == {"K001", "K002"}
    assert result.keepers["K001"].start_time == time(8, 0)
    assert result.problems == []


def test_malformed_rows_are_reported_without_stopping_the_load(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "K001;Alex;Lions;09:00:00;16:00:00\nK002;Priya;Penguins;8am;15:30:00;07:30:00\n"
    )

    result = load_schedule(path)

    assert result.keepers == {}
    assert result.problems == [
        "line 1: expected 6 fields, got 5",
        "line 2: times must be HH:MM:SS",
    ]


def test_keeper_ids_and_enclosures_are_matched_without_regard_to_case(zoo):
    assert zoo.keeper(" k001 ").name == "Alex"
    assert [k.name for k in zoo.keepers_for("PENGUINS")] == ["Priya"]


def test_a_late_check_in_is_logged_with_the_minutes_late(zoo, tmp_path):
    late = zoo.check_in(zoo.keeper("K001"), time(8, 20), datetime(2025, 3, 1, 8, 20))

    assert late == 20
    log = (tmp_path / "logs" / "late_checkin.csv").read_text().splitlines()
    assert log == ["2025-03-01,K001,Alex,08:20:00,20"]


def test_an_on_time_check_in_is_not_logged(zoo, tmp_path):
    assert zoo.check_in(zoo.keeper("K001"), time(7, 55), datetime(2025, 3, 1, 7, 55)) == 0
    assert not (tmp_path / "logs" / "late_checkin.csv").exists()


def test_completed_feeds_are_recorded(zoo, tmp_path):
    zoo.record_feed("Lions", "AM", datetime(2025, 3, 1, 9, 5))

    log = (tmp_path / "logs" / "feed_log.csv").read_text().splitlines()
    assert log == ["2025-03-01T09:05:00,Lions,AM"]


def test_the_bundled_sample_schedule_loads_cleanly():
    from pathlib import Path

    result = load_schedule(Path(__file__).resolve().parent.parent / "zoo_schedule.csv")

    assert len(result.keepers) == 5
    assert result.problems == []
