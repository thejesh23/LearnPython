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


def main() -> None:
    code_points_demo()


if __name__ == "__main__":
    main()
