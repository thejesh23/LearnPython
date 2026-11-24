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
from datetime import date, datetime, timedelta
from datetime import datetime
from datetime import datetime, timedelta, timezone


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


def arithmetic_demo() -> None:
    # Subtracting two dates gives a timedelta; adding a timedelta moves a date.
    start = date(2024, 1, 1)
    end = date(2024, 12, 25)
    gap = end - start
    print(f"days from {start} to {end}: {gap.days}")
    print(f"100 days after {start}: {start + timedelta(days=100)}")

    shift = timedelta(hours=7, minutes=30)
    clock_in = datetime(2024, 3, 1, 22, 0)
    print(f"a {shift} shift from {clock_in:%H:%M} ends {clock_in + shift}")
    print(f"total seconds in the shift: {shift.total_seconds():.0f}")

    # timedelta has no "months": months have different lengths, so
    # "one month later" is a calendar rule you must decide on yourself.


def formatting_demo() -> None:
    moment = datetime(2024, 7, 4, 9, 5)
    # strftime = "string from time"; % codes pick the pieces.
    print(f"{moment:%d %B %Y, %I:%M %p}")
    print(f"{moment:%Y-%m-%d %H:%M}")

    # strptime = "string parse time": the format must match exactly.
    parsed = datetime.strptime("25/12/2023 18:30", "%d/%m/%Y %H:%M")
    print(f"parsed: {parsed!r}")

    # ISO 8601 is the unambiguous format to store and exchange.
    text = moment.isoformat()
    print(f"isoformat: {text}, round trip ok: {datetime.fromisoformat(text) == moment}")


def timezone_demo() -> None:
    utc_moment = datetime(2024, 6, 1, 12, 0, tzinfo=timezone.utc)
    india = timezone(timedelta(hours=5, minutes=30), "IST")
    new_york = timezone(timedelta(hours=-4), "EDT")

    # astimezone shows the *same instant* on a different clock.
    print(f"UTC:      {utc_moment}")
    print(f"India:    {utc_moment.astimezone(india)}")
    print(f"New York: {utc_moment.astimezone(new_york)}")
    print(f"same instant: {utc_moment == utc_moment.astimezone(india)}")

    # Mixing naive and aware datetimes is an error, which is a good thing.
    naive = datetime(2024, 6, 1, 12, 0)
    try:
        _ = utc_moment - naive
    except TypeError as exc:
        print(f"aware - naive: {exc}")
    # Real zones with daylight saving rules live in zoneinfo, e.g.
    # ZoneInfo("Europe/London"); fixed offsets keep this demo portable.


def main() -> None:
    creating_demo()
    print()
    arithmetic_demo()
    print()
    formatting_demo()
    print()
    timezone_demo()


if __name__ == "__main__":
    main()
