"""`sqlite3` — a real SQL database in the standard library, no server.

Two habits that matter more than anything else here:

  1. **Always use parameters** (`?` placeholders). String-formatting values into
     SQL is how SQL injection happens, and the driver's escaping is correct in
     cases yours will not be.
  2. **Use the connection as a context manager** for transactions: the block
     commits on success and rolls back on an exception.

`executemany` batches inserts into one statement. `row_factory` turns tuples
into something addressable by column name.

This sample uses an in-memory database, so it writes nothing to disk.
"""

import sqlite3


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row  # rows addressable by column name
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript(
        """
        CREATE TABLE author (
            id      INTEGER PRIMARY KEY,
            name    TEXT NOT NULL UNIQUE
        );
        CREATE TABLE book (
            id        INTEGER PRIMARY KEY,
            title     TEXT NOT NULL,
            year      INTEGER,
            author_id INTEGER REFERENCES author(id)
        );
        """
    )

    with conn:  # transaction: commits at the end of the block
        conn.execute("INSERT INTO author (name) VALUES (?)", ("Ada",))
        conn.executemany(
            "INSERT INTO book (title, year, author_id) VALUES (?, ?, ?)",
            [("Notes", 1843, 1), ("Sketches", 1842, 1), ("Letters", 1845, 1)],
        )

    print("parameterised query:")
    for row in conn.execute(
        "SELECT title, year FROM book WHERE year > ? ORDER BY year", (1842,)
    ):
        print(f"  {row['title']} ({row['year']})")

    print("join and aggregate:")
    row = conn.execute(
        """
        SELECT a.name, COUNT(*) AS books, MIN(b.year) AS earliest
        FROM author a JOIN book b ON b.author_id = a.id
        GROUP BY a.id
        """
    ).fetchone()
    print(f"  {row['name']}: {row['books']} books, earliest {row['earliest']}")

    print("rollback on error:")
    try:
        with conn:
            conn.execute("INSERT INTO book (title, author_id) VALUES (?, ?)", ("Ok", 1))
            conn.execute("INSERT INTO author (name) VALUES (?)", ("Ada",))  # UNIQUE fails
    except sqlite3.IntegrityError as exc:
        print(f"  IntegrityError: {exc}")
    count = conn.execute("SELECT COUNT(*) FROM book").fetchone()[0]
    print(f"  book count still {count} — the whole block rolled back")

    print("foreign key enforcement:")
    try:
        conn.execute("INSERT INTO book (title, author_id) VALUES ('Orphan', 99)")
    except sqlite3.IntegrityError as exc:
        print(f"  IntegrityError: {exc}")

    print("never do this:  \"... WHERE name = '\" + user_input + \"'\"")
    unsafe_input = "x'; DROP TABLE book; --"
    safe = conn.execute("SELECT COUNT(*) FROM author WHERE name = ?", (unsafe_input,))
    print(f"  parameterised lookup of a hostile string is just a miss: {safe.fetchone()[0]}")

    print(f"tables still present: "
          f"{[r[0] for r in conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')]}")
    conn.close()


if __name__ == "__main__":
    main()
