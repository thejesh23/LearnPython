"""More SQL with `sqlite3`: executemany, joins, GROUP BY and transactions.

sqlite3_basics.py covers connecting, inserting and fetching. This file is
about the things that make a database worth using over a list of dicts:

    executemany        insert many rows with one call
    JOIN               combine rows from two tables that refer to each other
    GROUP BY           count, sum or average per group, inside the database
    transactions       several changes that succeed or fail together

A transaction is what keeps a bank transfer from taking money out of one
account without putting it into the other. Using the connection in a `with`
block commits when the block ends normally and rolls everything back if an
exception escapes. Note that `with conn:` does *not* close the connection;
`contextlib.closing` does that.
"""

import sqlite3


AUTHORS = [(1, "Ursula K. Le Guin"), (2, "Terry Pratchett"), (3, "Ada Newcomer")]
BOOKS = [
    ("A Wizard of Earthsea", 1, 1968, 4.5),
    ("The Left Hand of Darkness", 1, 1969, 4.3),
    ("Guards! Guards!", 2, 1989, 4.6),
    ("Mort", 2, 1987, 4.4),
    ("Small Gods", 2, 1992, 4.7),
]


def make_library() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    # executescript runs several statements; only for fixed SQL you wrote.
    conn.executescript("""
        CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE books (
            id        INTEGER PRIMARY KEY,
            title     TEXT NOT NULL,
            author_id INTEGER NOT NULL REFERENCES authors(id),
            year      INTEGER,
            rating    REAL
        );
    """)
    # executemany runs one statement once per tuple: one call, many rows.
    conn.executemany("INSERT INTO authors (id, name) VALUES (?, ?)", AUTHORS)
    conn.executemany(
        "INSERT INTO books (title, author_id, year, rating) VALUES (?, ?, ?, ?)",
        BOOKS,
    )
    conn.commit()
    return conn


def executemany_demo() -> None:
    conn = make_library()
    for table in ("authors", "books"):
        (count,) = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        print(f"{table}: {count} rows")
    # The table name above is our own constant, not user input, so an
    # f-string is acceptable there. Placeholders only work for values.
    print("books store an author_id, not the author's name:")
    print(f"  {conn.execute('SELECT title, author_id FROM books').fetchone()}")
    conn.close()


def join_demo() -> None:
    conn = make_library()
    # JOIN matches each book to its author through author_id = authors.id.
    rows = conn.execute("""
        SELECT books.title, authors.name
        FROM books
        JOIN authors ON authors.id = books.author_id
        WHERE books.year < ?
        ORDER BY books.year
    """, (1990,)).fetchall()
    print("books before 1990, with author names:")
    for title, author in rows:
        print(f"  {title:<26} {author}")

    # A plain JOIN drops authors with no books. LEFT JOIN keeps them, with
    # NULL (None in Python) where the book columns would be.
    rows = conn.execute("""
        SELECT authors.name, books.title
        FROM authors
        LEFT JOIN books ON books.author_id = authors.id
        WHERE books.id IS NULL
    """).fetchall()
    print(f"authors with no books yet (LEFT JOIN): {rows}")
    conn.close()


def main() -> None:
    executemany_demo()
    print()
    join_demo()


if __name__ == "__main__":
    main()
