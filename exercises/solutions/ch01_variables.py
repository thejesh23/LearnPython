"""Worked solutions for exercises/ch01_variables.py.

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
from typing import Any


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch01_variables.py")
)
report = EXERCISES["report"]


def swap(a: Any, b: Any) -> tuple[Any, Any]:
    # The right side builds the tuple (b, a) before anything is assigned,
    # so no temporary variable is needed. Here we return it directly.
    return b, a


def check_swap() -> None:
    report("1. swap", EXERCISES["test_swap"], swap)


def rotate_left(a: Any, b: Any, c: Any) -> tuple[Any, Any, Any]:
    # Same idea as swap, with three names: the commas make the tuple.
    return b, c, a


def check_rotate_left() -> None:
    report("2. rotate_left", EXERCISES["test_rotate_left"], rotate_left)


def main() -> None:
    check_swap()
    check_rotate_left()


if __name__ == "__main__":
    main()
