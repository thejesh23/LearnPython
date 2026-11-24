"""A URL shortener: short codes, a database, and a tiny web server.

Services like bit.ly turn a long address into a short one such as
https://sho.rt/q0V. Visiting the short link makes the server answer "go over
there instead" (an HTTP redirect), and the browser follows it. You build the
whole thing with the standard library:

    stage 1  base62 codes: turn a database id into a short string and back
    stage 2  storage: links in an SQLite database file
    stage 3  a web server that creates links and redirects visitors
    stage 4  a client that looks at the redirects without following them

301 or 302? Both mean "go to the Location header". 301 says "moved
permanently": browsers may cache it and never ask again, so later visits are
not counted. 302 says "found, for now": the browser asks every time. That is
why shorteners that count clicks usually answer 302.

The server listens on 127.0.0.1 only, on a port the operating system picks
(port 0), and is shut down at the end of each demo. Nothing leaves your
machine.

Uses:
    02_types               int arithmetic with divmod
    04_strings             string constants, encode/decode to bytes
    05_control_flow        while loops, early returns
    09_classes             subclassing the server and handler classes
    11_errors              a custom exception, catching HTTPError
    12_modules_io          context managers for the database and the server
    13_standard_library    sqlite3, http.server, urllib, threading
"""

import sqlite3
import string
import tempfile
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.request import ProxyHandler
from urllib.request import build_opener


# 10 digits + 26 lower + 26 upper = 62 characters, all safe in a URL.
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(ALPHABET)
INDEX = {char: value for value, char in enumerate(ALPHABET)}


def encode(n: int) -> str:
    """Write a non-negative integer in base 62."""
    if n < 0:
        raise ValueError("only non-negative numbers can be encoded")
    if n == 0:
        return ALPHABET[0]
    digits = []
    # Same idea as writing a number in base 10: the remainder is the last
    # digit, then divide and repeat. Digits come out backwards.
    while n:
        n, remainder = divmod(n, BASE)
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(code: str) -> int:
    n = 0
    for char in code:
        if char not in INDEX:
            raise ValueError(f"not a base62 character: {char!r}")
        n = n * BASE + INDEX[char]
    return n


def base62_demo() -> None:
    print("== stage 1: base62 ==")
    for n in [0, 61, 62, 100_000, 56_800_235_583, 2**63 - 1]:
        print(f"{n:>25,} -> {encode(n)}")
    ok = all(decode(encode(n)) == n for n in range(100_000))
    print(f"round trip for the first 100,000 ids: {ok}")
    print(f"six characters give {BASE**6:,} different codes")
    try:
        decode("ab-c")
    except ValueError as exc:
        print(f"ValueError: {exc}")


# Start counting at 100,000 so even the first link gets a 3-character code
# instead of "1", and codes do not reveal how few links exist.
ID_OFFSET = 100_000


class InvalidURL(ValueError):
    """Raised for anything that is not an absolute http(s) URL."""


@dataclass
class Link:
    code: str
    url: str
    permanent: bool
    hits: int


def validate(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise InvalidURL(f"not an http(s) URL: {url!r}")


class LinkStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        with self._db() as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS links (
                       id        INTEGER PRIMARY KEY,
                       url       TEXT NOT NULL UNIQUE,
                       permanent INTEGER NOT NULL,
                       hits      INTEGER NOT NULL DEFAULT 0
                   )"""
            )

    @contextmanager
    def _db(self) -> Iterator[sqlite3.Connection]:
        # A fresh connection per operation. That is simple, and it is safe
        # when the web server later calls us from another thread (a single
        # sqlite3 connection may only be used by the thread that made it).
        conn = sqlite3.connect(self.path)
        try:
            with conn:  # commits if the block succeeds, rolls back if not
                yield conn
        finally:
            conn.close()  # `with conn` alone does not close it

    def shorten(self, url: str, *, permanent: bool = False) -> str:
        validate(url)
        with self._db() as db:
            # Always pass values as ? parameters, never with f-strings: the
            # database then treats them as data, so SQL injection is impossible.
            row = db.execute("SELECT id FROM links WHERE url = ?", (url,)).fetchone()
            if row is not None:
                return encode(row[0] + ID_OFFSET)  # same URL, same code
            cursor = db.execute(
                "INSERT INTO links (url, permanent) VALUES (?, ?)", (url, permanent)
            )
            return encode(cursor.lastrowid + ID_OFFSET)

    def lookup(self, code: str) -> Link | None:
        try:
            link_id = decode(code) - ID_OFFSET
        except ValueError:
            return None  # cannot be one of ours
        with self._db() as db:
            row = db.execute(
                "SELECT url, permanent, hits FROM links WHERE id = ?", (link_id,)
            ).fetchone()
        return None if row is None else Link(code, row[0], bool(row[1]), row[2])

    def follow(self, code: str) -> Link | None:
        """Look a code up and count the visit."""
        link = self.lookup(code)
        if link is not None:
            with self._db() as db:
                db.execute(
                    "UPDATE links SET hits = hits + 1 WHERE id = ?",
                    (decode(code) - ID_OFFSET,),
                )
            link.hits += 1
        return link


def storage_demo() -> None:
    print("== stage 2: storage ==")
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "links.db"
        store = LinkStore(db_path)
        for url in [
            "https://docs.python.org/3/library/sqlite3.html",
            "https://www.python.org/downloads/",
            "https://docs.python.org/3/library/sqlite3.html",
        ]:
            code = store.shorten(url)
            print(f"{code} <- {url}")
        print("(the same URL got the same code)")

        try:
            store.shorten("javascript:alert(1)")
        except InvalidURL as exc:
            print(f"InvalidURL: {exc}")

        store.follow(code)
        store.follow(code)
        print(f"after two visits: {store.lookup(code)}")
        print(f"unknown code: {store.lookup('zzz')}, bad code: {store.lookup('?!')}")

        # A new LinkStore on the same file sees the same data: it persisted.
        reopened = LinkStore(db_path)
        print(f"reopened the file: {reopened.lookup(code)}")


class ShortenerHandler(BaseHTTPRequestHandler):
    """Handles one request. The server makes a new handler for each one."""

    server: "ShortenerServer"  # tells type checkers what self.server is

    def do_GET(self) -> None:
        code = self.path.lstrip("/")
        if not code:
            self.send_text(200, "URL shortener. POST url=... to /shorten\n")
            return
        link = self.server.store.follow(code)
        if link is None:
            self.send_text(404, f"no link with code {code!r}\n")
            return
        self.send_response(301 if link.permanent else 302)
        self.send_header("Location", link.url)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self) -> None:
        if self.path != "/shorten":
            self.send_text(404, "POST to /shorten\n")
            return
        # The body is a form: url=...&permanent=1, URL-encoded like a query.
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        url = form.get("url", [""])[0]
        permanent = form.get("permanent") == ["1"]
        try:
            code = self.server.store.shorten(url, permanent=permanent)
        except InvalidURL as exc:
            self.send_text(400, f"{exc}\n")
            return
        self.send_text(201, f"{self.server.base_url}/{code}\n")

    def send_text(self, status: int, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        pass  # the default prints every request to stderr; keep output clean


class ShortenerServer(ThreadingHTTPServer):
    def __init__(self, store: LinkStore) -> None:
        # Port 0 asks the operating system for any free port.
        super().__init__(("127.0.0.1", 0), ShortenerHandler)
        self.store = store

    @property
    def base_url(self) -> str:
        host, port = self.server_address[:2]
        return f"http://{host}:{port}"


@contextmanager
def running_server(store: LinkStore) -> Iterator[ShortenerServer]:
    """Serve in a background thread; always shut down, even after an error."""
    server = ShortenerServer(store)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()  # stops serve_forever()
        server.server_close()  # releases the port
        thread.join()


# An empty ProxyHandler ignores any proxy settings on this machine: we only
# ever talk to our own server on 127.0.0.1.
client = build_opener(ProxyHandler({}))


def post_link(base_url: str, url: str, permanent: bool = False) -> str:
    form = {"url": url, "permanent": "1" if permanent else "0"}
    data = urlencode(form).encode("ascii")  # passing data makes it a POST
    with client.open(f"{base_url}/shorten", data=data, timeout=5) as response:
        return response.read().decode("utf-8").strip()


def server_demo() -> None:
    print("== stage 3: the server ==")
    with tempfile.TemporaryDirectory() as tmp:
        store = LinkStore(Path(tmp) / "links.db")
        with running_server(store) as server:
            port = server.server_address[1]
            print(f"listening on 127.0.0.1, the OS picked a real port: {port > 0}")
            short = post_link(server.base_url, "https://www.python.org/")
            # Print only the path: the port number changes from run to run.
            print(f"POST /shorten -> 201, short link path {urlsplit(short).path}")
            try:
                post_link(server.base_url, "not a url")
            except HTTPError as exc:
                print(f"POST bad url  -> {exc.code}: {exc.read().decode().strip()}")
        print("server shut down")


def main() -> None:
    base62_demo()
    print()
    storage_demo()
    print()
    server_demo()


if __name__ == "__main__":
    main()
