import csv
from datetime import datetime


class Zookeeper:

    def __init__(self, keeper_id, name, enclosure, feed_am, feed_pm, start_time):
        self.keeper_id = keeper_id
        self.name = name
        self.enclosure = enclosure
        self.feed_am = feed_am
        self.feed_pm = feed_pm
        self.start_time = start_time


class ZooSchedule:

    def __init__(self, csv_file="zoo_schedule.csv"):
        self.keepers = {}
        self.load_schedule(csv_file)

    def load_schedule(self, csv_file):
        """Loads zookeeper schedule from a CSV file."""
        try:
            with open(csv_file, "r") as input_file:
                for line in input_file:
                    line = line.strip()
                    each_line = line.split(';')
                    if len(each_line) < 6:
                        print("Warning: Incomplete upload for line", line)
                        continue

                    keeper_id = each_line[0]
                    self.keepers[keeper_id] = Zookeeper(
                        keeper_id, each_line[1], each_line[2], each_line[3], each_line[4], each_line[5]
                    )
            print("Zoo schedule loaded...")
        except FileNotFoundError:
            print("Error: File 'zoo_schedule.csv' not found")
        except IndexError:
            print("Error: Formatting incorrect for one or more lines")

    def display_schedule(self):
        """Displays the zookeeper schedule."""
        for keeper in self.keepers.values():
            print(
                f"{keeper.name} works in enclosure {keeper.enclosure}. "
                f"Feed times: AM-{keeper.feed_am}, PM-{keeper.feed_pm}. "
                f"Starts work at {keeper.start_time}."
            )

    def get_keeper(self, keeper_id):
        """Fetches a zookeeper by ID."""
        return self.keepers.get(keeper_id, None)


class ZooControl(ZooSchedule):
    """Manages the daily operations of the zoo."""

    def __init__(self, csv_file="zoo_schedule.csv"):
        super().__init__(csv_file)

    def display_feeding_times(self):
        """Displays feeding times for a specific enclosure."""
        enclosure = input("Which enclosure would you like to see the feeding times for? ").lower()
        for keeper in self.keepers.values():
            if keeper.enclosure.lower() == enclosure:
                print(
                    f"The {enclosure} have feeding times at {keeper.feed_am} and {keeper.feed_pm}."
                )
                return
        print(f"Sorry, no {enclosure} at this zoo.")

    def check_in_keeper(self, keeper_id):
        """Processes zookeeper check-in."""
        keeper = self.get_keeper(keeper_id)
        if not keeper:
            print(f"No such zookeeper ID: {keeper_id}")
            return

        check_in_time = input("What time are you checking in? (HH:MM:SS): ")
        if not validate_time(check_in_time):
            print("Invalid time format. Enter as HH:MM:SS.")
            return

        start_time = datetime.strptime(keeper.start_time, '%H:%M:%S').hour
        check_in_hour = datetime.strptime(check_in_time, '%H:%M:%S').hour

        if start_time - check_in_hour < 0:
            log_late_check_in(keeper_id)
        else:
            print("Checked in on time.")

    def report_feeds(self):
        """Records the completion of feedings."""
        enclosure = input("Which enclosure are you reporting feeds completed for? ")
        feed_type = int(input("1. AM or 2. PM feed: "))
        time_feed = "AM" if feed_type == 1 else "PM"

        print(f"Feeding for {enclosure} recorded for {time_feed}.")


def validate_time(check_in_time):
    """Validates the format of a time string."""
    try:
        datetime.strptime(check_in_time, "%H:%M:%S")
        return True
    except ValueError:
        return False


def log_late_check_in(keeper_id, msg="checked in late"):
    """Logs a late check-in to a CSV file."""
    with open("late_checkin.csv", "a") as output_file:
        csv.writer(output_file).writerow([keeper_id, msg])
    print(f"Zookeeper {keeper_id} logged as {msg}")


def main():
    zoo = ZooControl()
    while True:
        choice = int(input(
            "\nZoo Management System\n"
            "1. Show all zookeeper schedules\n"
            "2. Check feeding times for an enclosure\n"
            "3. Zookeeper check-in\n"
            "4. Record feed completion\n"
            "5. Exit\n"
            "Enter your choice: "
        ))
        match choice:
            case 1:
                zoo.display_schedule()
            case 2:
                zoo.display_feeding_times()
            case 3:
                keeper_id = input("Enter the zookeeper ID: ")
                zoo.check_in_keeper(keeper_id)
            case 4:
                zoo.report_feeds()
            case 5:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
