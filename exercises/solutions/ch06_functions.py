"""Worked solutions for exercises/ch06_functions.py.

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
    str(Path(__file__).resolve().parent.parent / "ch06_functions.py")
)
report = EXERCISES["report"]


def average(*numbers: float) -> float:
    # *numbers arrives as a tuple. An empty tuple is falsy, which guards
    # the division by zero.
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def check_average() -> None:
    report("1. average", EXERCISES["test_average"], average)


def main() -> None:
    check_average()


if __name__ == "__main__":
    main()
