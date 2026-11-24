"""Solutions: classes (chapter 09).

Worked answers for exercises/ch09_classes.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch09_classes.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch09_classes.py")
)
report = EXERCISES["report"]


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        return self.width == self.height


def check_rectangle() -> None:
    report("1. Rectangle", EXERCISES["test_rectangle"], Rectangle)


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = balance  # leading underscore: internal by convention

    @property
    def balance(self) -> float:
        # No @balance.setter, so assigning to .balance raises AttributeError.
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"deposit must be positive, got {amount}")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"withdrawal must be positive, got {amount}")
        if amount > self._balance:
            raise ValueError(f"cannot withdraw {amount}: balance is {self._balance}")
        self._balance -= amount
        return self._balance


def check_bank_account() -> None:
    report("2. BankAccount", EXERCISES["test_bank_account"], BankAccount)


def main() -> None:
    check_rectangle()
    check_bank_account()


if __name__ == "__main__":
    main()
