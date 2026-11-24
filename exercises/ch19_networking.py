"""Practice: networking (chapter 19).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch19_networking.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

Nothing here needs the internet: the tests start their own small servers on
127.0.0.1 (this machine only) and stop them again.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch19_networking.py: try first, peek second. The lessons
for this chapter are in basics/19_networking/.
"""

import json
import socket
import threading
import urllib.request
from collections.abc import Callable
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from typing import Any
from urllib.error import HTTPError


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

def get_param(url: str, name: str) -> str | None:
    """Return the value of query parameter `name` in `url`, decoded.

        url = "https://shop.example/search?q=caf%C3%A9+au+lait&page=2#top"
        get_param(url, "q")     ->  "café au lait"
        get_param(url, "page")  ->  "2"
        get_param(url, "top")   ->  None    (the fragment is not the query)

    If the name appears more than once, return the first value. A parameter
    that is present but empty ("?q=&page=1") gives "", not None. Use
    urllib.parse: urlsplit for the query part, then parse_qs (look up its
    keep_blank_values option).
    """
    raise NotImplementedError


def test_get_param(impl: Callable[[str, str], str | None]) -> None:
    url = "https://shop.example/search?q=caf%C3%A9+au+lait&page=2#top"
    cases = [
        (url, "q", "café au lait"),
        (url, "page", "2"),
        (url, "top", None),
        (url, "missing", None),
        ("https://x.example/?tag=red&tag=blue", "tag", "red"),
        ("https://x.example/?q=&page=1", "q", ""),
        ("https://x.example/?sum=1%2B1%3D2", "sum", "1+1=2"),
        ("https://x.example/no/query", "q", None),
    ]
    for address, name, want in cases:
        got = impl(address, name)
        assert got == want, (
            f"get_param({address!r}, {name!r}) gave {got!r}, not {want!r}"
        )


def check_get_param() -> None:
    report("1. get_param", test_get_param, get_param)


# --- Exercise 2 -------------------------------------------------------------

def add_params(url: str, params: dict[str, str | int]) -> str:
    """Return `url` with `params` added to its query string.

    - Parameters already in the URL keep their place; a name given in
      params replaces the old value in that same place.
    - New names go at the end, in the order of params.
    - Values are encoded properly ("fish & chips" -> "fish+%26+chips").
    - The fragment (#...) and everything else stays as it was.

        url = "https://x.example/s?q=old&page=1#top"
        add_params(url, {"page": 3, "lang": "en"})
        ->  "https://x.example/s?q=old&page=3&lang=en#top"

    Split with urlsplit, read the old query with parse_qsl into a dict,
    update it, build the new query with urlencode, put it back with
    ._replace(query=...) and urlunsplit.
    """
    raise NotImplementedError


def test_add_params(impl: Callable[[str, dict[str, str | int]], str]) -> None:
    cases = [
        ("https://x.example/s?q=old&page=1#top", {"page": 3, "lang": "en"},
         "https://x.example/s?q=old&page=3&lang=en#top"),
        ("https://x.example/s", {"q": "fish & chips"},
         "https://x.example/s?q=fish+%26+chips"),
        ("https://x.example/s?a=1", {}, "https://x.example/s?a=1"),
        ("http://127.0.0.1:8000/api?empty=", {"n": 1},
         "http://127.0.0.1:8000/api?empty=&n=1"),
        ("https://x.example/s", {"city": "Zürich"},
         "https://x.example/s?city=Z%C3%BCrich"),
    ]
    for url, params, want in cases:
        got = impl(url, params)
        assert got == want, (
            f"add_params({url!r}, {params}) gave {got!r}, not {want!r}"
        )


def check_add_params() -> None:
    report("2. add_params", test_add_params, add_params)


@contextmanager
def one_client_server(handle: Callable[[socket.socket], None]) -> Iterator[int]:
    """Test helper: serve one client on a free 127.0.0.1 port; yield the port.

    `handle` runs in a background thread with the accepted connection. An
    error raised there is raised again when the with block ends.
    """
    listener = socket.create_server(("127.0.0.1", 0))  # port 0: any free port
    listener.settimeout(0.05)  # wake up often to check whether to stop
    stop = threading.Event()
    errors: list[BaseException] = []

    def run() -> None:
        while not stop.is_set():
            try:
                conn, _address = listener.accept()
            except TimeoutError:
                continue
            with conn:
                conn.settimeout(2)  # a confused client cannot hang the test
                try:
                    handle(conn)
                except BaseException as error:
                    errors.append(error)
            return

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        yield listener.getsockname()[1]
    finally:
        stop.set()
        thread.join(timeout=5)
        listener.close()
        if errors:
            raise errors[0]


# --- Exercise 3 -------------------------------------------------------------

def send_and_receive(port: int, message: str) -> str:
    """Send `message` to a server on 127.0.0.1:port and return its reply.

    The server reads until the client says "no more data", then answers
    and closes the connection. So:
      1. connect with socket.create_connection(("127.0.0.1", port), timeout=5)
      2. send the message encoded as UTF-8 with sendall
      3. call shutdown(socket.SHUT_WR): "I am done sending"
      4. recv in a loop until it returns b"" (the server closed), joining
         the pieces, and decode the whole reply at the end
    Close the socket when done (a with block does it).
    """
    raise NotImplementedError


def test_send_and_receive(impl: Callable[[int, str], str]) -> None:
    def shout(conn: socket.socket) -> None:
        received = b""
        try:
            while chunk := conn.recv(7):  # small reads, to test the client loop
                received += chunk
        except TimeoutError:
            raise AssertionError(
                "the server never saw the end of the message: call"
                " shutdown(socket.SHUT_WR) after sending"
            ) from None
        reply = received.decode("utf-8").upper().encode("utf-8")
        for start in range(0, len(reply), 5):
            conn.sendall(reply[start:start + 5])

    for message in ("hello, socket", "grüße aus köln " * 40, ""):
        with one_client_server(shout) as port:
            got = impl(port, message)
        want = message.upper()
        assert got == want, (
            f"sent {message[:20]!r}...: expected {want[:20]!r}..., got {got[:20]!r}..."
        )


def check_send_and_receive() -> None:
    report("3. send_and_receive", test_send_and_receive, send_and_receive)


# --- Exercise 4 -------------------------------------------------------------

def handle_lines(conn: socket.socket) -> None:
    """Server side: answer every line the client sends with the line reversed.

    The client sends UTF-8 text made of lines, each ending in "\n". TCP is
    a stream, so one recv may hold half a line, or several lines, or even
    half of one multi-byte character. For each complete line, send back its
    text reversed plus "\n" ("abc\n" -> "cba\n"). Return when the client
    closes its side (recv returns b"").

    Easiest: conn.makefile("r", encoding="utf-8") gives a file object whose
    readline() and for loop do the buffering for you. Or keep a bytes buffer
    and split it on b"\n" yourself, decoding only complete lines.
    """
    raise NotImplementedError


def test_handle_lines(impl: Callable[[socket.socket], None]) -> None:
    with one_client_server(impl) as port:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as client:
            # The "ï" in "naïve" is two bytes; the first send stops between them.
            client.sendall(b"abc\nna\xc3")
            client.sendall(b"\xafve\nxyz\n\n")
            client.shutdown(socket.SHUT_WR)
            reply = b""
            while chunk := client.recv(1024):
                reply += chunk
    want = "cba\nevïan\nzyx\n\n"
    got = reply.decode("utf-8", errors="replace")
    assert got == want, f"the client should receive {want!r}, got {got!r}"


def check_handle_lines() -> None:
    report("4. handle_lines", test_handle_lines, handle_lines)


# --- Exercise 5 -------------------------------------------------------------

# Like urllib.request.urlopen, but ignores any proxy settings, so requests
# to 127.0.0.1 always go straight to the test server. Use OPENER.open(...).
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def fetch_json(url: str, attempts: int = 3) -> Any:
    """GET `url` and return its JSON body, retrying when the server fails.

    - Open the URL with OPENER.open(url, timeout=5) and json.loads the body.
    - On an error status, urllib raises urllib.error.HTTPError; its .code
      is the status number.
    - 5xx means the server failed and might recover: try again, up to
      `attempts` tries in total, then re-raise the last HTTPError.
    - 4xx means the request itself is wrong: re-raise at once, no retry.
    (A real client would also wait a little longer before each retry.)
    """
    raise NotImplementedError


def test_fetch_json(impl: Callable[..., Any]) -> None:
    hits: dict[str, int] = {}

    class Api(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            hits[self.path] = hits.get(self.path, 0) + 1
            status, body = {
                "/books/1": (200, {"title": "Dune"}),
                "/flaky": (503, {"error": "busy"}) if hits[self.path] < 3
                else (200, {"ok": True}),
                "/down": (500, {"error": "broken"}),
            }.get(self.path, (404, {"error": "not found"}))
            data = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: object) -> None:
            pass  # keep the report free of request logs

    server = ThreadingHTTPServer(("127.0.0.1", 0), Api)
    # A short poll_interval lets shutdown() return quickly at the end.
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True
    )
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        got = impl(f"{base}/books/1")
        assert got == {"title": "Dune"}, f"/books/1 gave {got!r}"
        got = impl(f"{base}/flaky", attempts=3)
        assert got == {"ok": True}, f"/flaky works on the third try, got {got!r}"
        assert hits["/flaky"] == 3, f"/flaky was tried {hits['/flaky']} times, not 3"
        for path, tries, status in (("/missing", 3, 404), ("/down", 2, 500)):
            try:
                impl(base + path, attempts=tries)
            except HTTPError as error:
                error.close()
                assert error.code == status, (
                    f"{path}: expected status {status}, got {error.code}"
                )
            else:
                raise AssertionError(f"{path} should raise HTTPError {status}")
        tries = hits["/missing"]
        assert tries == 1, f"a 404 must not be retried, but it was tried {tries} times"
        tries = hits["/down"]
        assert tries == 2, f"/down with attempts=2 was tried {tries} times"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def check_fetch_json() -> None:
    report("5. fetch_json", test_fetch_json, fetch_json)


def main() -> None:
    check_get_param()
    check_add_params()
    check_send_and_receive()
    check_handle_lines()
    check_fetch_json()


if __name__ == "__main__":
    main()
