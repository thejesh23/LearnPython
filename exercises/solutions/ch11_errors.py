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


def parse_age(text: str) -> int:
    try:
        age = int(text)
    except ValueError as exc:
        # "from exc" records the original error as __cause__.
        raise ValueError(f"age must be a whole number, got {text!r}") from exc
    if not 0 <= age <= 150:
        raise ValueError(f"age out of range: {age}")
    return age


def check_parse_age() -> None:
    report("2. parse_age", EXERCISES["test_parse_age"], parse_age)


class InsufficientFunds(Exception):
    def __init__(self, balance: float, amount: float) -> None:
        # The message goes to Exception.__init__, which is what str() shows.
        super().__init__(
            f"cannot withdraw {amount:.2f} from a balance of {balance:.2f}"
        )
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance


def check_insufficient_funds() -> None:
    report("3. InsufficientFunds", EXERCISES["test_insufficient_funds"],
           InsufficientFunds)


def main() -> None:
    check_safe_int()
    check_parse_age()
    check_insufficient_funds()


if __name__ == "__main__":
    main()
