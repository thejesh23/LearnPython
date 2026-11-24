"""Unicode text and raw bytes: two different types, and how to cross between them.

A `str` is a sequence of *code points*: numbers that Unicode assigns to every
character, from "A" (65) to "€" (8364) to emoji. A `bytes` object is a
sequence of small integers 0-255, which is what files, sockets and disks
actually store.

To go from text to bytes you *encode*, choosing an encoding; to go back you
*decode* with the same encoding. UTF-8 is the usual choice: ASCII characters
take one byte each, and other characters take two, three or four.

Python never mixes the two silently. Adding a str to a bytes is a TypeError,
which forces you to decide the encoding once, at the edge of your program:
decode as data comes in, work with str inside, encode as it goes out.
"""


def code_points_demo() -> None:
    # ord() gives a character's code point; chr() goes the other way.
    for ch in ["A", "a", "é", "€", "π"]:
        print(f"{ch!r}: ord = {ord(ch):>5}   hex = U+{ord(ch):04X}")
    print(f"chr(9731) = {chr(9731)}")

    # \u escapes write a code point by number inside a normal string.
    print(f"'\\u00e9' == 'é' -> {'\u00e9' == 'é'}")

    # Letters are numbers, so you can do arithmetic on them.
    shifted = "".join(chr(ord(c) + 1) for c in "HAL")
    print(f"HAL shifted by one: {shifted}")


def str_vs_bytes_demo() -> None:
    text = "café"
    data = text.encode("utf-8")
    print(f"str   {text!r}: type {type(text).__name__}, len {len(text)}")
    print(f"bytes {data!r}: type {type(data).__name__}, len {len(data)}")

    # Indexing bytes gives an int, not a one-character string.
    print(f"text[0] = {text[0]!r}, data[0] = {data[0]!r}")
    print(f"list(data) = {list(data)}")

    # A b"..." literal may only contain ASCII; anything else needs escapes.
    print(f"b'hi' == 'hi'.encode() -> {b'hi' == 'hi'.encode()}")

    # Decoding with the same encoding round-trips exactly.
    print(f"decoded back: {data.decode('utf-8')!r}")

    # The two types never mix by accident.
    try:
        "price: " + b"10"  # type: ignore[operator]
    except TypeError as exc:
        print(f"TypeError: {exc}")


def utf8_lengths_demo() -> None:
    # UTF-8 is variable width: the higher the code point, the more bytes.
    print(f"{'code point':<11} {'bytes':<6} {'encoded':<12} char")
    for ch in ["A", "é", "€", "\U0001D11E"]:
        encoded = ch.encode("utf-8")
        point = f"U+{ord(ch):04X}"
        print(f"{point:<11} {len(encoded):<6} {encoded.hex(' '):<12} {ch}")

    # So len() of a string and len() of its bytes can differ a lot.
    word = "naïve café"
    print(f"{word!r}: {len(word)} characters, "
          f"{len(word.encode('utf-8'))} UTF-8 bytes, "
          f"{len(word.encode('utf-16-le'))} UTF-16 bytes")

    # Cutting bytes in the middle of a character makes them undecodable.
    cut = "€".encode("utf-8")[:2]
    try:
        cut.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"UnicodeDecodeError: {exc}")


def error_handlers_demo() -> None:
    # ASCII only covers code points 0-127, so "é" cannot be encoded in it.
    text = "café"
    try:
        text.encode("ascii")
    except UnicodeEncodeError as exc:
        print(f"UnicodeEncodeError: {exc}")

    # errors= says what to do instead of raising.
    for handler in ["ignore", "replace", "xmlcharrefreplace", "backslashreplace"]:
        print(f"encode errors={handler!r:<20} -> {text.encode('ascii', handler)!r}")

    # Decoding has the same choices. Latin-1 bytes are not valid UTF-8.
    latin1 = text.encode("latin-1")
    print(f"latin-1 bytes: {latin1!r}")
    for handler in ["replace", "backslashreplace"]:
        print(f"decode errors={handler!r:<18} -> {latin1.decode('utf-8', handler)!r}")
    # "replace" inserts U+FFFD, the official "something was lost here" mark.
    # Prefer fixing the encoding to hiding the problem.


def main() -> None:
    code_points_demo()
    print()
    str_vs_bytes_demo()
    print()
    utf8_lengths_demo()
    print()
    error_handlers_demo()


if __name__ == "__main__":
    main()
