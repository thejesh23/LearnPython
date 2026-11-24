"""Solutions: networking (chapter 19).

Worked answers for exercises/ch19_networking.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch19_networking.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
import socket
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch19_networking.py")
)
report = EXERCISES["report"]


def get_param(url: str, name: str) -> str | None:
    # parse_qs decodes %XX and "+" and maps each name to a LIST of values.
    # Without keep_blank_values=True, "q=" would vanish instead of giving "".
    values = parse_qs(urlsplit(url).query, keep_blank_values=True).get(name)
    return values[0] if values else None


def check_get_param() -> None:
    report("1. get_param", EXERCISES["test_get_param"], get_param)


def add_params(url: str, params: dict[str, str | int]) -> str:
    parts = urlsplit(url)
    # A dict keeps insertion order, and updating an existing key keeps its
    # place, which is exactly the ordering the task asks for.
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({name: str(value) for name, value in params.items()})
    return urlunsplit(parts._replace(query=urlencode(query)))


def check_add_params() -> None:
    report("2. add_params", EXERCISES["test_add_params"], add_params)


def send_and_receive(port: int, message: str) -> str:
    with socket.create_connection(("127.0.0.1", port), timeout=5) as conn:
        conn.sendall(message.encode("utf-8"))
        # Without this the server keeps waiting for more, and so do we.
        conn.shutdown(socket.SHUT_WR)
        chunks = []
        while chunk := conn.recv(4096):
            chunks.append(chunk)
    # Decode once at the end: a character may be split across two chunks.
    return b"".join(chunks).decode("utf-8")


def check_send_and_receive() -> None:
    report("3. send_and_receive", EXERCISES["test_send_and_receive"],
           send_and_receive)


def main() -> None:
    check_get_param()
    check_add_params()
    check_send_and_receive()


if __name__ == "__main__":
    main()
