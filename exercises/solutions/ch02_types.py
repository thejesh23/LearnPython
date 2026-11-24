"""Worked solutions for exercises/ch02_types.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from fractions import Fraction
from pathlib import Path


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch02_types.py")
)
report = EXERCISES["report"]


def utf8_length(text: str) -> tuple[int, int]:
    # len() of a str counts code points; encoding gives bytes, and len()
    # of those counts bytes. Characters outside ASCII take 2 to 4 bytes.
    return len(text), len(text.encode("utf-8"))


def check_utf8_length() -> None:
    report("1. utf8_length", EXERCISES["test_utf8_length"], utf8_length)


def split_seconds(total: int) -> tuple[int, int, int]:
    # Peel off the smallest unit first: divmod by 60 leaves the seconds as
    # the remainder, then the same step on the minutes leaves the minutes.
    minutes, seconds = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds


def check_split_seconds() -> None:
    report("2. split_seconds", EXERCISES["test_split_seconds"], split_seconds)


def simplify(numerator: int, denominator: int) -> str:
    # Fraction reduces to lowest terms and normalises the sign as soon as it
    # is built; str() prints "3/4", or just "2" for a whole number.
    return str(Fraction(numerator, denominator))


def check_simplify() -> None:
    report("3. simplify", EXERCISES["test_simplify"], simplify)


def main() -> None:
    check_utf8_length()
    check_split_seconds()
    check_simplify()


if __name__ == "__main__":
    main()
