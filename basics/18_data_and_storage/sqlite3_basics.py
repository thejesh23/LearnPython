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


PETS = [
    {"name": "Rex", "species": "dog", "age": 4},
    {"name": "Tom", "species": "cat", "age": 7},
    {"name": "Bella", "species": "dog", "age": 2},
    {"name": "Nemo", "species": "fish", "age": None},
]


def rows_demo() -> None:
    conn = make_db()
    # :name placeholders are filled from a dict, handy when you have one.
    for pet in PETS:
        conn.execute("INSERT INTO pets (name, species, age) "
                     "VALUES (:name, :species, :age)", pet)
    conn.commit()

    # row_factory = sqlite3.Row gives rows you can index by column name.
    conn.row_factory = sqlite3.Row
    query = "SELECT name, age FROM pets WHERE species = ? ORDER BY age"
    # A cursor can be looped over directly, one row at a time.
    for row in conn.execute(query, ("dog",)):
        print(f"  {row['name']} is {row['age']}  (keys: {row.keys()})")

    row = conn.execute("SELECT * FROM pets WHERE name = ?", ("Nemo",)).fetchone()
    print(f"as a dict: {dict(row)}")
    conn.close()


def update_delete_demo() -> None:
    conn = make_db()
    for pet in PETS:
        conn.execute("INSERT INTO pets (name, species, age) "
                     "VALUES (:name, :species, :age)", pet)

    # rowcount says how many rows a change touched.
    cur = conn.execute("UPDATE pets SET age = age + 1 WHERE species = ?", ("dog",))
    print(f"birthday for {cur.rowcount} dogs")
    cur = conn.execute("DELETE FROM pets WHERE age IS NULL")  # IS NULL, not = NULL
    print(f"deleted {cur.rowcount} pet(s) with an unknown age")
    cur = conn.execute("DELETE FROM pets WHERE name = ?", ("Nobody",))
    print(f"deleting a missing name touches {cur.rowcount} rows, no error")
    conn.commit()

    left = conn.execute("SELECT name, age FROM pets ORDER BY name").fetchall()
    print(f"left: {left}")
    conn.close()


def find_unsafe(conn: sqlite3.Connection, name: str) -> list[tuple]:
    # WRONG: the user's text becomes part of the SQL itself.
    sql = f"SELECT name, species FROM pets WHERE name = '{name}'"
    return conn.execute(sql).fetchall()


def find_safe(conn: sqlite3.Connection, name: str) -> list[tuple]:
    # RIGHT: the SQL is fixed; the name travels separately as plain data.
    return conn.execute("SELECT name, species FROM pets WHERE name = ?",
                        (name,)).fetchall()


def injection_demo() -> None:
    conn = make_db()
    for pet in PETS:
        conn.execute("INSERT INTO pets (name, species, age) "
                     "VALUES (:name, :species, :age)", pet)

    print(f"normal search, unsafe: {find_unsafe(conn, 'Tom')}")
    print(f"normal search, safe:   {find_safe(conn, 'Tom')}")

    # A user types this into the search box instead of a name.
    attack = "x' OR '1'='1"
    print("the query the unsafe version builds:")
    print(f"  SELECT name, species FROM pets WHERE name = '{attack}'")
    print(f"unsafe with the attack: {find_unsafe(conn, attack)}")
    print(f"safe with the attack:   {find_safe(conn, attack)}  (no pet has that name)")

    # Names with apostrophes are not attacks, yet they break the unsafe version.
    irish = "O'Malley"
    try:
        find_unsafe(conn, irish)
    except sqlite3.OperationalError as exc:
        print(f"unsafe with {irish}: OperationalError: {exc}")
    print(f"safe with {irish}: {find_safe(conn, irish)}")
    conn.close()


def main() -> None:
    create_and_insert_demo()
    print()
    rows_demo()
    print()
    update_delete_demo()
    print()
    injection_demo()


if __name__ == "__main__":
    main()
