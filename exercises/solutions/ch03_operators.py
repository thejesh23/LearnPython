"""Worked solutions for exercises/ch03_operators.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from pathlib import Path


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch03_operators.py")
)
report = EXERCISES["report"]


def is_even(n: int) -> bool:
    # In Python n % 2 is always 0 or 1 for a positive divisor, even when n
    # is negative, so this one test covers every int.
    return n % 2 == 0


def check_is_even() -> None:
    report("1. is_even", EXERCISES["test_is_even"], is_even)


def in_range(x: float, low: float, high: float) -> bool:
    # A chained comparison means (low <= x) and (x <= high).
    return low <= x <= high


def check_in_range() -> None:
    report("2. in_range", EXERCISES["test_in_range"], in_range)


def display_name(name: str, nickname: str) -> str:
    # `a or b` is a when a is truthy, else b; an empty string is falsy.
    return nickname or name


def check_display_name() -> None:
    report("3. display_name", EXERCISES["test_display_name"], display_name)


def main() -> None:
    check_is_even()
    check_in_range()
    check_display_name()


if __name__ == "__main__":
    main()
