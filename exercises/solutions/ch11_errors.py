"""Solutions: errors and exceptions (chapter 11).

Worked answers for exercises/ch11_errors.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch11_errors.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch11_errors.py")
)
report = EXERCISES["report"]


def safe_int(text: str, default: int = 0) -> int:
    try:
        return int(text)
    except ValueError:  # only "not a number"; a TypeError is a real bug
        return default


def check_safe_int() -> None:
    report("1. safe_int", EXERCISES["test_safe_int"], safe_int)


def main() -> None:
    check_safe_int()


if __name__ == "__main__":
    main()
