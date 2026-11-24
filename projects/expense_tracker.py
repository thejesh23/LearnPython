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

import sqlite3
import tempfile
from datetime import date
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


def main() -> None:
    storage_demo()


if __name__ == "__main__":
    main()
