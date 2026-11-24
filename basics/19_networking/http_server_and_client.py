"""HTTP with only the standard library: `http.server` and `urllib.request`.

HTTP is text-framed requests and responses on top of a TCP socket:

    request:   GET /hello?name=Ada HTTP/1.1      response:  HTTP/1.0 200 OK
               Host: 127.0.0.1:54321                        Content-Type: text/plain
               User-Agent: ...                              Content-Length: 12
                                                            (blank line)
                                                            Hello, Ada!

The server side here is `ThreadingHTTPServer` plus a handler class: one
`do_GET` / `do_POST` method per HTTP method, and helpers to send a status
code, headers and a body. The client side is `urllib.request.urlopen`.

Status codes are grouped by their first digit: 2xx success, 3xx redirect,
4xx "you asked for something wrong", 5xx "the server failed". `urlopen`
raises `HTTPError` for 4xx and 5xx, and `URLError` when it could not talk to
a server at all.

`http.server` is fine for demos, tests and local tools. It is not meant for
production traffic; use a real web framework and server for that.
"""

import json
import threading
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import parse_qs
from urllib.parse import urlsplit


class GreetingHandler(BaseHTTPRequestHandler):
    """Answers GET /hello?name=... and a couple of other paths."""

    def do_GET(self) -> None:
        url = urlsplit(self.path)  # self.path is the path plus query string
        if url.path == "/hello":
            name = parse_qs(url.query).get("name", ["world"])[0]
            self.send_text(200, f"Hello, {name}!")
        elif url.path == "/teapot":
            self.send_text(418, "I'm a teapot")
        else:
            self.send_text(404, f"nothing at {url.path}")

    def send_text(self, status: int, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(status)  # status line plus Server and Date headers
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Agent-Seen", self.headers.get("User-Agent", "?"))
        self.end_headers()  # the blank line between headers and body
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass  # silence the default one-line-per-request log on stderr


@contextmanager
def running_server(
    handler: type[BaseHTTPRequestHandler],
) -> Iterator[str]:
    """Run a server on a free local port; yield its base URL; stop it."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    # poll_interval: how often serve_forever checks for shutdown (default 0.5s).
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True
    )
    thread.start()
    try:
        host, port = server.server_address[:2]
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()  # ask serve_forever to return...
        server.server_close()  # ...then release the listening socket
        thread.join(timeout=5)


# An opener with an empty ProxyHandler ignores any http_proxy environment
# variable, so requests to 127.0.0.1 always go straight to our server.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def get_demo() -> None:
    with running_server(GreetingHandler) as base:
        request = urllib.request.Request(
            f"{base}/hello?name=Ada", headers={"User-Agent": "learnpython/1.0"}
        )
        # Always pass a timeout: the default is to wait forever.
        with OPENER.open(request, timeout=5) as response:
            print(f"status : {response.status} {response.reason}")
            print(f"type   : {response.headers['Content-Type']}")
            print(f"agent  : {response.headers['X-Agent-Seen']}")
            print(f"body   : {response.read().decode('utf-8')}")


class NotesHandler(GreetingHandler):
    """Adds POST /notes, which stores a JSON note and returns it with an id."""

    # Class attributes on purpose: the server builds a NEW handler object for
    # every request, so anything stored on self would be gone next time. The
    # lock matters because ThreadingHTTPServer runs requests in parallel.
    notes: list[dict[str, object]] = []
    lock = threading.Lock()

    def do_POST(self) -> None:
        if self.path != "/notes":
            self.send_text(404, f"cannot POST to {self.path}")
            return
        # The body is only as long as Content-Length says; never read "all".
        length = int(self.headers.get("Content-Length", "0"))
        try:
            note = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self.send_text(400, "body must be JSON")
            return
        with self.lock:
            note["id"] = len(self.notes) + 1
            self.notes.append(note)
        body = json.dumps(note).encode("utf-8")
        self.send_response(201)  # 201 Created
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Location", f"/notes/{note['id']}")
        self.end_headers()
        self.wfile.write(body)


def post_demo() -> None:
    with running_server(NotesHandler) as base:
        for text in ("buy milk", "call mum"):
            # Passing data= makes urllib send a POST instead of a GET.
            request = urllib.request.Request(
                f"{base}/notes",
                data=json.dumps({"text": text}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with OPENER.open(request, timeout=5) as response:
                created = json.loads(response.read())
                where = response.headers["Location"]
                print(f"{response.status} created {created} at {where}")


def fetch(url: str, method: str = "GET") -> str:
    """Return a one-line summary of what happened, never raise."""
    request = urllib.request.Request(url, method=method)
    try:
        with OPENER.open(request, timeout=5) as response:
            return f"{response.status} {response.read().decode('utf-8')!r}"
    except HTTPError as exc:
        # The server answered, just not with success. An HTTPError is also a
        # response: it has a status code, headers and a body you can read.
        return f"HTTPError {exc.code} {exc.reason}: {exc.read()[:30]!r}"
    except URLError as exc:
        # No HTTP answer at all: refused, DNS failure, timeout and so on.
        return f"URLError: {type(exc.reason).__name__}"


def errors_demo() -> None:
    with running_server(GreetingHandler) as base:
        print(fetch(f"{base}/hello"))
        print(fetch(f"{base}/missing"))
        print(fetch(f"{base}/teapot"))
        # The handler has no do_DELETE, so the base class answers 501.
        print(fetch(f"{base}/hello", method="DELETE"))
    # The server is stopped now: nothing listens on that port any more.
    print(fetch(f"{base}/hello"))


def main() -> None:
    get_demo()
    print()
    post_demo()
    print()
    errors_demo()


if __name__ == "__main__":
    main()
