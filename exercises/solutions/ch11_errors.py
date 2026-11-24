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
from collections.abc import Callable
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


def retry(func: Callable[[], str], attempts: int) -> str:
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except ConnectionError:
            if attempt == attempts:
                raise  # out of attempts: re-raise the error we just caught
    raise AssertionError("unreachable: the loop returns or raises")


def check_retry() -> None:
    report("4. retry", EXERCISES["test_retry"], retry)


def validate_order(order: dict[str, object]) -> None:
    errors: list[Exception] = []
    if not order.get("item"):
        errors.append(ValueError("item is required"))
    quantity = order.get("quantity")
    if not isinstance(quantity, int):
        errors.append(TypeError("quantity must be an int"))
    elif quantity < 1:
        errors.append(ValueError("quantity must be at least 1"))
    if "@" not in str(order.get("email", "")):
        errors.append(ValueError("email needs an @"))
    if errors:
        raise ExceptionGroup("invalid order", errors)


def check_validate_order() -> None:
    report("5. validate_order", EXERCISES["test_validate_order"], validate_order)


def main() -> None:
    check_safe_int()
    check_parse_age()
    check_insufficient_funds()
    check_retry()
    check_validate_order()


if __name__ == "__main__":
    main()
