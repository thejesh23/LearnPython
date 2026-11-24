"""TCP sockets — a tiny echo server and client talking over 127.0.0.1.

A socket is one end of a network connection. With TCP, one side *listens* on
a port and *accepts* connections; the other side *connects*. After that both
ends simply send and receive bytes.

Three things trip up everyone the first time:

1. Sockets carry **bytes**, not text. Encode before sending, decode after.
2. TCP is a **stream**, not a sequence of messages. Two `sendall` calls may
   arrive as one `recv`, and one `sendall` may arrive in pieces. If you need
   messages you must mark where each one ends: this is called *framing*.
3. Both ends must agree when the conversation is over, or one waits forever.
   Closing (or `shutdown(SHUT_WR)`) is how a side says "no more data".

Every server here binds to 127.0.0.1 (this machine only) on port 0, which
asks the operating system for any free port, and runs in a background thread
so the client can run in the main thread of the same script.
"""

import socket
import threading
from collections.abc import Callable


def serve_one_client(
    handle: Callable[[socket.socket], None],
) -> tuple[int, threading.Thread]:
    """Listen on a free local port and hand the first client to `handle`."""
    # create_server = socket() + bind() + listen(). Port 0 means "any free".
    listener = socket.create_server(("127.0.0.1", 0))
    listener.settimeout(5)  # never hang forever if no client shows up
    port = listener.getsockname()[1]

    def run() -> None:
        with listener:
            conn, _address = listener.accept()
            with conn:
                handle(conn)

    # Listening already started above, so the client cannot connect too early.
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return port, thread


def echo(conn: socket.socket) -> None:
    # recv returns up to 1024 bytes, or b"" once the client has finished.
    while chunk := conn.recv(1024):
        conn.sendall(chunk)


def echo_demo() -> None:
    port, thread = serve_one_client(echo)
    # The port number changes every run, so print a fact about it instead.
    print(f"server listening on 127.0.0.1, OS-assigned port: {port > 0}")

    with socket.create_connection(("127.0.0.1", port), timeout=5) as client:
        client.sendall("hello, socket".encode("utf-8"))  # str -> bytes
        # Tell the server we are done sending, so its recv loop ends.
        client.shutdown(socket.SHUT_WR)
        received = b""
        while chunk := client.recv(1024):
            received += chunk
    print(f"raw reply: {received!r}")
    print(f"decoded  : {received.decode('utf-8')}")

    thread.join(timeout=5)
    print(f"server thread finished: {not thread.is_alive()}")


def main() -> None:
    echo_demo()


if __name__ == "__main__":
    main()
