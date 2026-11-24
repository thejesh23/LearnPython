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
import struct
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


def shout_lines(conn: socket.socket) -> None:
    # makefile() wraps the socket in a buffered file, so readline() keeps
    # reading until it sees b"\n", however the bytes were split in transit.
    with conn.makefile("rb") as reader:
        for line in reader:
            reply = line.decode("utf-8").strip().upper() + "\n"
            conn.sendall(reply.encode("utf-8"))


def newline_framing_demo() -> None:
    port, thread = serve_one_client(shout_lines)
    messages = ["first message", "second", "third and last"]

    with socket.create_connection(("127.0.0.1", port), timeout=5) as client:
        # All three messages in ONE send. Without a delimiter the server could
        # not tell where one ends and the next begins.
        payload = "".join(m + "\n" for m in messages).encode("utf-8")
        client.sendall(payload)
        client.shutdown(socket.SHUT_WR)
        with client.makefile("rb") as reader:
            replies = [line.decode("utf-8").rstrip("\n") for line in reader]

    print(f"sent {len(payload)} bytes in one sendall")
    for sent, got in zip(messages, replies, strict=True):
        print(f"  {sent!r:>18} -> {got!r}")
    thread.join(timeout=5)
    # Limitation: a message can never contain "\n" itself.


HEADER = struct.Struct("!I")  # 4-byte unsigned int, network (big-endian) order


def recv_exactly(conn: socket.socket, size: int) -> bytes | None:
    """Read exactly `size` bytes, or return None if the peer closed first."""
    buffer = b""
    while len(buffer) < size:
        chunk = conn.recv(size - len(buffer))  # may return fewer bytes
        if not chunk:
            if buffer:
                raise ConnectionError("connection closed mid-message")
            return None
        buffer += chunk
    return buffer


def send_message(conn: socket.socket, body: bytes) -> None:
    conn.sendall(HEADER.pack(len(body)) + body)


def recv_message(conn: socket.socket) -> bytes | None:
    header = recv_exactly(conn, HEADER.size)
    if header is None:
        return None
    (length,) = HEADER.unpack(header)
    return recv_exactly(conn, length)


def describe(conn: socket.socket) -> None:
    while (body := recv_message(conn)) is not None:
        send_message(conn, f"got {len(body)} bytes".encode("utf-8"))


def length_prefix_demo() -> None:
    port, thread = serve_one_client(describe)
    # Newlines, zero bytes, anything: the length says where the message ends.
    bodies = [b"plain", b"two\nlines", bytes(range(5)), b"x" * 10_000]

    with socket.create_connection(("127.0.0.1", port), timeout=5) as client:
        for body in bodies:
            send_message(client, body)
            reply = recv_message(client)
            assert reply is not None
            print(f"  sent {body[:12]!r:<24} reply: {reply.decode('utf-8')}")
    # Leaving the with-block closes the client; the server sees EOF and stops.
    thread.join(timeout=5)
    print(f"header for 10000: {HEADER.pack(10_000).hex(' ')}")


def main() -> None:
    echo_demo()
    print()
    newline_framing_demo()
    print()
    length_prefix_demo()


if __name__ == "__main__":
    main()
