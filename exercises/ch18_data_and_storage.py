"""Practice: data and storage (chapter 18).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch18_data_and_storage.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch18_data_and_storage.py: try first, peek second. The
lessons for this chapter are in basics/18_data_and_storage/.
"""

import hashlib
import sqlite3
import struct
import tempfile
from collections.abc import Callable
from contextlib import closing
from pathlib import Path
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Return the SHA-256 fingerprint of a file as 64 hex characters.

    This is how download pages let you check a file arrived intact. Open
    the file in binary mode ("rb") and feed it to hashlib.sha256() in
    chunks of, say, 64 KiB with .update(), so even a huge file never has
    to fit in memory. Finish with .hexdigest().
    """
    raise NotImplementedError


def test_sha256_file(impl: Callable[[Path], str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.bin"
        path.write_bytes(b"")
        empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        got = impl(path)
        assert got == empty, f"an empty file should hash to {empty}, got {got}"
        path.write_bytes(b"abc")
        abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        got = impl(path)
        assert got == abc, f"b'abc' should hash to {abc}, got {got}"
        # Bigger than one chunk, with every byte value, so text mode would break.
        data = bytes(range(256)) * 1500
        path.write_bytes(data)
        want = hashlib.sha256(data).hexdigest()
        got = impl(path)
        assert got == want, f"a 384 KB file: expected {want}, got {got}"


def check_sha256_file() -> None:
    report("1. sha256_file", test_sha256_file, sha256_file)


# --- Exercise 2 -------------------------------------------------------------

def parse_header(data: bytes) -> dict[str, int]:
    """Read the 11-byte header at the start of an imaginary ".lpy" file.

        bytes 0-3    the magic marker b"LPY1"
        bytes 4-5    version, unsigned 16-bit, big-endian
        bytes 6-9    record count, unsigned 32-bit, big-endian
        byte  10     flags, unsigned 8-bit

    Return {"version": ..., "count": ..., "flags": ...}. Bytes after the
    header are the file's contents; ignore them. Raise ValueError if data
    is shorter than 11 bytes or does not start with b"LPY1".

    One struct format describes the whole header: ">4sHIB" (">" means
    big-endian with no padding). struct.unpack_from reads from the start of
    a longer buffer; struct.calcsize(">4sHIB") is 11.
    """
    raise NotImplementedError


def test_parse_header(impl: Callable[[bytes], dict[str, int]]) -> None:
    header = b"LPY1" + bytes([0, 2]) + (70000).to_bytes(4, "big") + bytes([5])
    got = impl(header + b"...the records...")
    want = {"version": 2, "count": 70000, "flags": 5}
    assert got == want, f"expected {want}, got {got} (check the byte order)"
    header = b"LPY1" + bytes([1, 0]) + bytes([0, 0, 0, 1]) + bytes([255])
    got = impl(header)
    want = {"version": 256, "count": 1, "flags": 255}
    assert got == want, f"a header with nothing after it: expected {want}, got {got}"
    for bad in (b"PNG\x89" + header[4:], header[:10], b""):
        try:
            impl(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad!r} should raise ValueError")


def check_parse_header() -> None:
    report("2. parse_header", test_parse_header, parse_header)


# --- Exercise 3 -------------------------------------------------------------

def add_user(conn: sqlite3.Connection, name: str, email: str) -> int:
    """Insert a row into the users table and return its new id.

    The table is: users(id INTEGER PRIMARY KEY, name TEXT, email TEXT).
    Put the values into the SQL with ? placeholders and a tuple, never with
    an f-string: names like "Miles O'Brien" contain quotes. Commit, so other
    connections can see the row, and return cursor.lastrowid.
    """
    raise NotImplementedError


def test_add_user(impl: Callable[[sqlite3.Connection, str, str], int]) -> None:
    people = [
        ("Ada", "ada@example.com"),
        ("Miles O'Brien", "miles@example.com"),
        ("Robert'); DROP TABLE users; --", "bobby@example.com"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "app.db"
        with closing(sqlite3.connect(db)) as conn:
            conn.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
            )
            ids = [impl(conn, name, email) for name, email in people]
            assert ids == [1, 2, 3], f"the new ids should be [1, 2, 3], got {ids}"
        # A second connection sees only committed rows.
        with closing(sqlite3.connect(db)) as other:
            rows = other.execute("SELECT name, email FROM users ORDER BY id").fetchall()
        assert rows == people, f"the table should hold {people}, got {rows}"


def check_add_user() -> None:
    report("3. add_user", test_add_user, add_user)


# --- Exercise 4 -------------------------------------------------------------

def top_customers(conn: sqlite3.Connection, n: int) -> list[tuple[str, float]]:
    """Return the n customers who spent the most, as (name, total) pairs.

    Tables:
        customers(id INTEGER PRIMARY KEY, name TEXT)
        orders(id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)

    Biggest total first; equal totals in alphabetical order of name.
    Customers with no orders are left out. Let the database do the work in
    one query: JOIN the tables, GROUP BY customer, SUM(amount), ORDER BY,
    and LIMIT ? with n as a parameter.
    """
    raise NotImplementedError


def test_top_customers(impl: Callable[[sqlite3.Connection, int], Any]) -> None:
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER,"
            " amount REAL)"
        )
        conn.executemany(
            "INSERT INTO customers (id, name) VALUES (?, ?)",
            [(1, "Cy"), (2, "Ada"), (3, "Bo"), (4, "Dee"), (5, "Eve")],
        )
        conn.executemany(
            "INSERT INTO orders (customer_id, amount) VALUES (?, ?)",
            [(1, 12.5), (2, 30.0), (1, 17.5), (3, 30.0), (5, 2.25), (2, 0.0)],
        )
        got = [tuple(row) for row in impl(conn, 3)]
        want = [("Ada", 30.0), ("Bo", 30.0), ("Cy", 30.0)]
        assert got == want, f"top 3: expected {want}, got {got}"
        got = [tuple(row) for row in impl(conn, 10)]
        want = [("Ada", 30.0), ("Bo", 30.0), ("Cy", 30.0), ("Eve", 2.25)]
        assert got == want, f"top 10 (Dee has no orders): expected {want}, got {got}"
        got = list(impl(conn, 0))
        assert got == [], f"n=0 should give [], got {got}"


def check_top_customers() -> None:
    report("4. top_customers", test_top_customers, top_customers)


def main() -> None:
    check_sha256_file()
    check_parse_header()
    check_add_user()
    check_top_customers()


if __name__ == "__main__":
    main()
