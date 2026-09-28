"""Console front end for the zookeeper schedule manager."""

import argparse
from datetime import datetime
from pathlib import Path

from zoo import Zoo, load_schedule, parse_time

HERE = Path(__file__).resolve().parent

MENU = """
Zoo Management System
1. Show all zookeeper schedules
2. Check feeding times for an enclosure
3. Zookeeper check-in
4. Record feed completion
5. Exit
"""


def fmt(t) -> str:
    return t.strftime("%H:%M")


def show_schedule(zoo: Zoo) -> None:
    for k in zoo.keepers.values():
        print(
            f"  {k.keeper_id}  {k.name:<10} {k.enclosure:<10} "
            f"feeds {fmt(k.feed_am)} & {fmt(k.feed_pm)}, starts {fmt(k.start_time)}"
        )


def show_feeding_times(zoo: Zoo) -> None:
    enclosure = input(f"Which enclosure? ({', '.join(zoo.enclosures())}) ")
    keepers = zoo.keepers_for(enclosure)
    if not keepers:
        print(f"Sorry, there's no {enclosure.strip()} enclosure at this zoo.")
    for k in keepers:
        print(f"The {k.enclosure} are fed at {fmt(k.feed_am)} and {fmt(k.feed_pm)} by {k.name}.")


def check_in(zoo: Zoo) -> None:
    keeper = zoo.keeper(input("Zookeeper ID: "))
    if keeper is None:
        print("No zookeeper has that ID.")
        return
    try:
        at = parse_time(input("Check-in time (HH:MM:SS): "))
    except ValueError:
        print("Invalid time. Enter it as HH:MM:SS.")
        return
    late = zoo.check_in(keeper, at, datetime.now())
    if late:
        print(f"{keeper.name} is {late} minute(s) late; this has been logged.")
    else:
        print(f"{keeper.name} checked in on time.")


def record_feed(zoo: Zoo) -> None:
    enclosure = input(f"Which enclosure? ({', '.join(zoo.enclosures())}) ")
    if not zoo.keepers_for(enclosure):
        print(f"Sorry, there's no {enclosure.strip()} enclosure at this zoo.")
        return
    session = {"1": "AM", "2": "PM"}.get(input("1. AM or 2. PM feed: ").strip())
    if session is None:
        print("Please enter 1 or 2.")
        return
    zoo.record_feed(zoo.keepers_for(enclosure)[0].enclosure, session, datetime.now())
    print(f"{session} feed for the {enclosure.strip()} recorded.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule", type=Path, default=HERE / "zoo_schedule.csv")
    parser.add_argument("--log-dir", type=Path, default=HERE / "logs")
    args = parser.parse_args()

    try:
        loaded = load_schedule(args.schedule)
    except FileNotFoundError:
        raise SystemExit(f"Schedule file not found: {args.schedule}") from None
    for problem in loaded.problems:
        print(f"Skipped {problem}")
    zoo = Zoo(loaded.keepers, args.log_dir)
    print(f"Loaded {len(zoo.keepers)} zookeepers.")

    actions = {"1": show_schedule, "2": show_feeding_times, "3": check_in, "4": record_feed}
    while True:
        try:
            choice = input(MENU + "Enter your choice: ").strip()
        except EOFError:
            break
        if choice == "5":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Please enter a number from 1 to 5.")
            continue
        try:
            action(zoo)
        except EOFError:
            break


if __name__ == "__main__":
    main()
