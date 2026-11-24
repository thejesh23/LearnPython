"""`sqlite3` — a real SQL database that ships with Python.

SQLite keeps a whole database in one file (or in memory) and needs no server,
no install and no password. It is a good home for data that has outgrown a
JSON or CSV file: you can search, sort and update it without loading
everything into memory.

    sqlite3.connect(path)       open or create a database; ":memory:" for RAM
    conn.execute(sql, params)   run one SQL statement
    cursor.fetchone/fetchall    read the result rows
    conn.commit()               make changes permanent

The one rule to remember: put values into SQL with `?` placeholders and a
tuple of parameters, never with f-strings or `+`. Building SQL from text is
how SQL injection happens, and the last part of this file shows it.

Everything here uses an in-memory database, so nothing is written to disk.
"""

import sqlite3


def make_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")  # a fresh, empty database in memory
    conn.execute("""
        CREATE TABLE pets (
            id      INTEGER PRIMARY KEY,   -- filled in automatically
            name    TEXT NOT NULL,
            species TEXT NOT NULL,
            age     INTEGER
        )
    """)
    return conn


def create_and_insert_demo() -> None:
    conn = make_db()
    # Each ? is filled from the tuple, in order. The driver handles quoting.
    conn.execute("INSERT INTO pets (name, species, age) VALUES (?, ?, ?)",
                 ("Rex", "dog", 4))
    conn.execute("INSERT INTO pets (name, species, age) VALUES (?, ?, ?)",
                 ("Tom", "cat", 7))
    # None becomes SQL NULL: "unknown".
    cursor = conn.execute("INSERT INTO pets (name, species, age) VALUES (?, ?, ?)",
                          ("Nemo", "fish", None))
    print(f"the last insert got id {cursor.lastrowid}")
    conn.commit()  # without commit, a file database would lose these rows

    # A SELECT returns a cursor; each row is a tuple.
    rows = conn.execute("SELECT id, name, species, age FROM pets").fetchall()
    for row in rows:
        print(f"  {row}")

    # A one-item parameter tuple needs the trailing comma: ("cat",).
    one = conn.execute("SELECT name FROM pets WHERE species = ?", ("cat",)).fetchone()
    print(f"fetchone: {one}")
    none = conn.execute("SELECT name FROM pets WHERE species = ?", ("owl",)).fetchone()
    print(f"no match: {none}")
    conn.close()


def main() -> None:
    create_and_insert_demo()


if __name__ == "__main__":
    main()
