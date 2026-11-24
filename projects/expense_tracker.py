"""Project: an expense tracker backed by a SQLite database.

You build it in four steps:

    1. storage       a database file with a categories table and an expenses
                     table, written to with parameterized queries
    2. categories    reject unknown categories, total spending per category
    3. reports       group by month in SQL with SUM, COUNT, AVG and MAX
    4. a session     load three months of sample spending and print a monthly
                     report as a formatted table

`sqlite3` ships with Python and stores a whole database in one file, so it is
a good first database: no server to install, real SQL to learn. Money is
stored as whole cents (an INTEGER), never as a float, because 0.1 + 0.2 is not
exactly 0.3 in floating point and rounding errors add up across many rows.

Uses:
    02_types               int vs float, Decimal for parsing money
    04_strings             f-string alignment for the table
    09_classes             a class wrapping the connection
    11_errors              custom exceptions
    12_modules_io          context managers, temp files
    13_standard_library    datetime, random with a seed
    18_data_and_storage    sqlite3 connections, queries, GROUP BY
"""

import random
import sqlite3
import tempfile
from datetime import date
from datetime import timedelta
from decimal import Decimal
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY,
    spent_on    TEXT    NOT NULL,          -- ISO date, e.g. 2026-03-14
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    note        TEXT    NOT NULL DEFAULT ''
);
"""


class ExpenseError(Exception):
    """Input the tracker refuses, like a negative amount."""


def to_cents(amount: str) -> int:
    # Decimal("12.30") is exact, unlike float("12.30").
    cents = Decimal(amount) * 100
    if cents != cents.to_integral_value():
        raise ExpenseError(f"{amount} has more than two decimal places")
    return int(cents)


def money(cents: int) -> str:
    return f"{cents / 100:,.2f}"


class Tracker:
    def __init__(self, path: str | Path) -> None:
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA foreign_keys = ON")  # off by default in SQLite
        self.db.executescript(SCHEMA)

    def close(self) -> None:
        self.db.close()

    def add_category(self, name: str) -> None:
        # INSERT OR IGNORE: adding a category twice is harmless.
        with self.db:  # commits on success, rolls back on error
            self.db.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)",
                            (name.lower(),))

    def add(self, spent_on: date, amount: str, category: str, note: str = "") -> int:
        # The ? placeholders let sqlite3 quote values safely. Never build SQL
        # with f-strings: a note like "'); DROP TABLE expenses; --" would run.
        with self.db:
            cur = self.db.execute(
                "INSERT INTO expenses (spent_on, amount_cents, category_id, note) "
                "SELECT ?, ?, id, ? FROM categories WHERE name = ?",
                (spent_on.isoformat(), to_cents(amount), note, category.lower()))
        # rowcount is 0 when the SELECT found no such category.
        return cur.lastrowid if cur.rowcount == 1 and cur.lastrowid else 0


def storage_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "expenses.db"
        tracker = Tracker(path)
        tracker.add_category("food")
        tracker.add(date(2026, 3, 2), "12.30", "food", "lunch")
        tracker.add(date(2026, 3, 3), "4.05", "Food", "coffee")
        tracker.close()

        # Reopen the file: the rows were saved to disk.
        tracker = Tracker(path)
        rows = tracker.db.execute(
            "SELECT spent_on, amount_cents, note FROM expenses ORDER BY id")
        for spent_on, cents, note in rows:
            print(f"{spent_on}  {money(cents):>7}  {note}")
        tracker.close()
    for bad in ["1.005", "-3"]:
        try:
            cents = to_cents(bad)
            print(f"{bad} -> {cents} cents (the database CHECK will refuse it)")
        except ExpenseError as exc:
            print(f"ExpenseError: {exc}")


def add_checked(tracker: Tracker, spent_on: date, amount: str, category: str,
                note: str = "") -> int:
    """Like Tracker.add, but explain what went wrong in plain words."""
    try:
        row_id = tracker.add(spent_on, amount, category, note)
    except sqlite3.IntegrityError as exc:  # the CHECK constraint fired
        raise ExpenseError(f"amount must be positive, got {amount}") from exc
    if row_id == 0:  # the SELECT found no category, so nothing was inserted
        raise ExpenseError(f"unknown category {category!r}")
    return row_id


def totals_by_category(tracker: Tracker) -> list[tuple[str, int, int]]:
    # LEFT JOIN keeps categories with no expenses (their SUM is NULL -> 0).
    return tracker.db.execute("""
        SELECT c.name, COUNT(e.id), COALESCE(SUM(e.amount_cents), 0)
        FROM categories c LEFT JOIN expenses e ON e.category_id = c.id
        GROUP BY c.id ORDER BY 3 DESC, c.name
    """).fetchall()


def category_demo() -> None:
    tracker = Tracker(":memory:")  # a throwaway database in RAM
    for name in ["food", "transport", "fun"]:
        tracker.add_category(name)
    add_checked(tracker, date(2026, 3, 1), "30.00", "food")
    add_checked(tracker, date(2026, 3, 2), "2.75", "transport", "bus")
    add_checked(tracker, date(2026, 3, 4), "18.20", "food")
    for amount, category in [("9.99", "games"), ("-5", "fun")]:
        try:
            add_checked(tracker, date(2026, 3, 5), amount, category)
        except ExpenseError as exc:
            print(f"ExpenseError: {exc}")
    for name, count, cents in totals_by_category(tracker):
        print(f"{name:<10} n={count}  total {money(cents):>6}")
    tracker.close()


def monthly_summary(tracker: Tracker) -> list[sqlite3.Row]:
    # substr(spent_on, 1, 7) turns "2026-03-14" into the month "2026-03".
    tracker.db.row_factory = sqlite3.Row  # rows readable by column name
    try:
        return tracker.db.execute("""
            SELECT substr(spent_on, 1, 7)    AS month,
                   COUNT(*)                  AS n,
                   SUM(amount_cents)         AS total,
                   CAST(AVG(amount_cents) AS INTEGER) AS average,
                   MAX(amount_cents)         AS largest
            FROM expenses GROUP BY month ORDER BY month
        """).fetchall()
    finally:
        tracker.db.row_factory = None


def month_by_category(tracker: Tracker, month: str) -> dict[str, int]:
    rows = tracker.db.execute("""
        SELECT c.name, SUM(e.amount_cents)
        FROM expenses e JOIN categories c ON c.id = e.category_id
        WHERE substr(e.spent_on, 1, 7) = ?
        GROUP BY c.name
    """, (month,))
    return dict(rows.fetchall())


def report_demo() -> None:
    tracker = Tracker(":memory:")
    for name in ["food", "rent"]:
        tracker.add_category(name)
    tracker.add(date(2026, 1, 1), "900", "rent")
    tracker.add(date(2026, 1, 9), "45.10", "food")
    tracker.add(date(2026, 2, 1), "900", "rent")
    tracker.add(date(2026, 2, 3), "12.00", "food")
    tracker.add(date(2026, 2, 17), "61.40", "food")
    for row in monthly_summary(tracker):
        print(f"{row['month']}: {row['n']} expenses, total {money(row['total'])}, "
              f"avg {money(row['average'])}, largest {money(row['largest'])}")
    february = month_by_category(tracker, "2026-02")
    print(f"2026-02 by category: { {k: money(v) for k, v in february.items()} }")
    tracker.close()


CATEGORIES = {  # name -> (typical low, high in whole units, times per month)
    "groceries": (15, 90, 8),
    "transport": (2, 25, 10),
    "eating out": (8, 45, 5),
    "fun": (10, 60, 3),
}


def load_sample(tracker: Tracker, months: list[date], seed: int = 7) -> int:
    rng = random.Random(seed)  # same seed, same "random" spending every run
    count = 0
    for name in CATEGORIES:
        tracker.add_category(name)
    tracker.add_category("rent")
    for first_day in months:
        tracker.add(first_day, "950.00", "rent", "monthly rent")
        count += 1
        for name, (low, high, times) in CATEGORIES.items():
            for _ in range(rng.randint(times - 2, times + 2)):
                day = first_day + timedelta(days=rng.randrange(28))
                amount = f"{rng.uniform(low, high):.2f}"
                tracker.add(day, amount, name)
                count += 1
    return count


def print_report(tracker: Tracker) -> None:
    summary = monthly_summary(tracker)
    months = [row["month"] for row in summary]
    per_month = {m: month_by_category(tracker, m) for m in months}
    names = sorted({name for totals in per_month.values() for name in totals})

    print(f"{'category':<12}" + "".join(f"{m:>11}" for m in months) + f"{'total':>11}")
    print("-" * (12 + 11 * (len(months) + 1)))
    for name in names:
        cells = [per_month[m].get(name, 0) for m in months]
        print(f"{name:<12}" + "".join(f"{money(c):>11}" for c in cells)
              + f"{money(sum(cells)):>11}")
    print("-" * (12 + 11 * (len(months) + 1)))
    totals = [row["total"] for row in summary]
    print(f"{'total':<12}" + "".join(f"{money(t):>11}" for t in totals)
          + f"{money(sum(totals)):>11}")
    print(f"{'# expenses':<12}" + "".join(f"{row['n']:>11}" for row in summary))
    print(f"{'average':<12}"
          + "".join(f"{money(row['average']):>11}" for row in summary))

    # A tiny bar chart: one # per 100 spent outside rent.
    print()
    for m in months:
        spend = sum(v for k, v in per_month[m].items() if k != "rent")
        print(f"{m}  {'#' * round(spend / 10000):<15} {money(spend)} besides rent")


def session_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tracker = Tracker(Path(tmp) / "expenses.db")
        months = [date(2026, 1, 1), date(2026, 2, 1), date(2026, 3, 1)]
        print(f"loaded {load_sample(tracker, months)} sample expenses\n")
        print_report(tracker)
        tracker.close()


def main() -> None:
    storage_demo()
    print()
    category_demo()
    print()
    report_demo()
    print()
    session_demo()


if __name__ == "__main__":
    main()
