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

import string


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


def main() -> None:
    base62_demo()


if __name__ == "__main__":
    main()
