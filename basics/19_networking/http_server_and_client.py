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

import threading
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
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


def main() -> None:
    get_demo()


if __name__ == "__main__":
    main()
