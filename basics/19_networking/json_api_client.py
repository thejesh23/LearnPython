"""A small JSON API client: timeouts, error handling and retries with backoff.

Most real programs talk to some web API that speaks JSON. The happy path is
three lines; the rest of a good client is about what happens when things go
wrong:

    timeouts   never wait forever; a hung server should not hang you
    errors     turn "HTTP 404 with a JSON body" into one clear exception
    retries    try again, but only for failures that might go away
               (5xx, timeouts), and wait longer after each failure

To stay offline, the file starts its own tiny API on 127.0.0.1 in a
background thread. The routes live in a dict, so each stage adds an endpoint
by registering a function.
"""

import json
import threading
import time
import urllib.request
from collections.abc import Callable
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from typing import Any
from urllib.error import HTTPError
from urllib.error import URLError


# --- the server side: a route is a function from path parts to (status, data)
Route = Callable[[list[str]], tuple[int, Any]]
ROUTES: dict[str, Route] = {}
BOOKS = {1: "Dune", 2: "Emma", 3: "Ulysses"}


def route(name: str) -> Callable[[Route], Route]:
    def register(func: Route) -> Route:
        ROUTES[name] = func
        return func

    return register


@route("books")
def books(parts: list[str]) -> tuple[int, Any]:
    if not parts:
        return 200, [{"id": k, "title": v} for k, v in BOOKS.items()]
    if parts[0].isdigit() and int(parts[0]) in BOOKS:
        book_id = int(parts[0])
        return 200, {"id": book_id, "title": BOOKS[book_id]}
    return 404, {"error": f"no book {parts[0]!r}"}


class ApiHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        name, *rest = self.path.strip("/").split("/")
        handler = ROUTES.get(name)
        status, data = handler(rest) if handler else (404, {"error": "no route"})
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass  # keep the demo output clean


@contextmanager
def local_api() -> Iterator[str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
    # poll_interval: how often serve_forever checks for shutdown (default 0.5s).
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True
    )
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


# --- the client side
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


class ApiError(Exception):
    """One exception type for every way a call can fail."""

    def __init__(self, status: int | None, message: str) -> None:
        super().__init__(f"[{status or 'no response'}] {message}")
        self.status = status  # None means we never got an HTTP answer


def get_json(url: str, *, timeout: float = 2.0) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with OPENER.open(request, timeout=timeout) as response:
            return json.load(response)
    # HTTPError is a subclass of URLError, so it must be caught first.
    except HTTPError as exc:
        detail = json.loads(exc.read() or b"{}").get("error", exc.reason)
        raise ApiError(exc.code, detail) from exc
    except URLError as exc:
        # Refused, unknown host, or a timeout while connecting.
        if isinstance(exc.reason, TimeoutError):
            raise ApiError(None, "timed out") from exc
        raise ApiError(None, f"network error: {exc.reason}") from exc
    except TimeoutError as exc:
        # A timeout after connecting, while waiting for or reading the reply.
        raise ApiError(None, "timed out") from exc


def client_demo() -> None:
    with local_api() as base:
        titles = [book["title"] for book in get_json(f"{base}/books")]
        print(f"all titles: {titles}")
        print(f"book 2: {get_json(f'{base}/books/2')}")
        for path in ("/books/99", "/authors"):
            try:
                get_json(base + path)
            except ApiError as exc:
                print(f"{path}: ApiError {exc}")


@route("slow")
def slow(parts: list[str]) -> tuple[int, Any]:
    time.sleep(0.3)  # pretend to be an overloaded server
    return 200, {"finally": "done"}


def timeout_demo() -> None:
    with local_api() as base:
        # The timeout applies to each blocking step (connect, each read), not
        # to the whole request, but it is still the line between "slow" and
        # "stuck forever".
        try:
            get_json(f"{base}/slow", timeout=0.1)
        except ApiError as exc:
            print(f"timeout=0.1: {exc}")
        print(f"timeout=2.0: {get_json(f'{base}/slow', timeout=2.0)}")


def main() -> None:
    client_demo()
    print()
    timeout_demo()


if __name__ == "__main__":
    main()
