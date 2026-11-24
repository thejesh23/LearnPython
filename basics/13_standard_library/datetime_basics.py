"""`datetime` — dates, times, durations and time zones.

    date        a calendar day (year, month, day)
    time        a time of day
    datetime    a date and a time together
    timedelta   a duration: the difference between two moments

The most important habit: store and compute in UTC with *aware* datetimes
(ones that carry a time zone), and convert to local time only for display.
A "naive" datetime has no zone, so Python cannot know which moment it means.
"""

from datetime import date, datetime


def creating_demo() -> None:
    launch = date(1969, 7, 20)
    print(f"date: {launch}, weekday: {launch.strftime('%A')}")
    print(f"year {launch.year}, month {launch.month}, day {launch.day}")

    moment = datetime(2024, 2, 29, 13, 45, 30)
    print(f"datetime: {moment}, just the date: {moment.date()}")

    # Invalid dates are rejected when they are created, not later.
    try:
        date(2023, 2, 29)
    except ValueError as exc:
        print(f"date(2023, 2, 29): {exc}")


def main() -> None:
    creating_demo()


if __name__ == "__main__":
    main()
