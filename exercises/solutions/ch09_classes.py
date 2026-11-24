"""Solutions: classes (chapter 09).

Worked answers for exercises/ch09_classes.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch09_classes.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import math
import runpy
from dataclasses import dataclass
from pathlib import Path
from typing import Self


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


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented  # let Python try the other side, then say False
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented  # Python turns this into a TypeError
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, factor: float) -> "Vector":
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Vector(self.x * factor, self.y * factor)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)


def check_vector() -> None:
    report("3. Vector", EXERCISES["test_vector"], Vector)


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    @classmethod
    def from_string(cls, text: str) -> Self:
        parts = text.split(".")
        if len(parts) not in (2, 3):
            raise ValueError(f"expected 'major.minor[.patch]', got {text!r}")
        # int() raises ValueError for non-numbers, which is what we want.
        return cls(*(int(part) for part in parts))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def check_version() -> None:
    report("4. Version.from_string", EXERCISES["test_version"], Version)


# Reuse the given base class from the exercise file, so isinstance checks in
# the test see the same Employee.
Employee = EXERCISES["Employee"]


class Manager(Employee):
    def __init__(self, name: str, salary: float) -> None:
        super().__init__(name, salary)
        self.reports: list[Employee] = []  # per instance, never a class attribute

    def add_report(self, employee: Employee) -> None:
        self.reports.append(employee)

    def describe(self) -> str:
        names = ", ".join(e.name for e in self.reports) or "nobody"
        return f"{super().describe()} and manages {len(self.reports)}: {names}"


def check_manager() -> None:
    report("5. Manager(Employee)", EXERCISES["test_manager"], Manager)


def main() -> None:
    check_rectangle()
    check_bank_account()
    check_vector()
    check_version()
    check_manager()


if __name__ == "__main__":
    main()
