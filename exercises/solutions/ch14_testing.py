"""Solutions: testing (chapter 14).

Worked answers for exercises/ch14_testing.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch14_testing.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from collections.abc import Callable
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch14_testing.py")
)
report = EXERCISES["report"]


def check_is_leap(is_leap: Callable[[int], bool]) -> None:
    # One year per branch of the rule, plus a plain non-leap year.
    assert is_leap(2024), "2024 divides by 4: leap"
    assert not is_leap(2023), "2023 does not divide by 4: not leap"
    assert not is_leap(1900), "1900 divides by 100 but not 400: not leap"
    assert is_leap(2000), "2000 divides by 400: leap"
    assert not is_leap(2022), "2022 is even but not divisible by 4: not leap"


def check_check_is_leap() -> None:
    report("1. check_is_leap", EXERCISES["test_check_is_leap"], check_is_leap)


def main() -> None:
    check_check_is_leap()


if __name__ == "__main__":
    main()
