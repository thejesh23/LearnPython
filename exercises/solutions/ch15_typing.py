"""Solutions: type hints (chapter 15).

Worked answers for exercises/ch15_typing.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch15_typing.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from collections.abc import Callable
from pathlib import Path
from typing import Literal, cast, get_args
from typing import overload


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch15_typing.py")
)
report = EXERCISES["report"]


# [T] declares a type parameter scoped to this one function: whatever type
# the items have, the default and the result have the same type.
def first[T](items: list[T], default: T) -> T:
    return items[0] if items else default


def check_first() -> None:
    report("1. first[T]", EXERCISES["test_first"], first)


type Mode = Literal["r", "w", "a"]


def parse_mode(text: str) -> Mode:
    allowed = get_args(Mode.__value__)  # ('r', 'w', 'a'), kept in one place
    if text not in allowed:
        raise ValueError(f"mode must be one of {allowed}, got {text!r}")
    # A type checker cannot see that the `in` test narrowed str to Mode, so
    # tell it with cast(); cast does nothing at runtime.
    return cast(Mode, text)


def check_parse_mode() -> None:
    report("2. parse_mode", EXERCISES["test_parse_mode"], parse_mode)


# The overloads are for the type checker only; at runtime the last,
# undecorated definition is the function that actually runs.
@overload
def double(value: int) -> int: ...
@overload
def double(value: str) -> str: ...
def double(value: int | str) -> int | str:
    return value * 2


def check_double() -> None:
    report("3. double with @overload", EXERCISES["test_double"], double)


def compose[A, B, C](f: Callable[[A], B], g: Callable[[B], C]) -> Callable[[A], C]:
    def composed(x: A) -> C:
        return g(f(x))  # f runs only when composed is called

    return composed


def check_compose() -> None:
    report("4. compose[A, B, C]", EXERCISES["test_compose"], compose)


class Registry[T]:
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def register(self, name: str, item: T) -> None:
        if name in self._items:
            raise ValueError(f"{name!r} is already registered")
        self._items[name] = item

    def get(self, name: str) -> T:
        return self._items[name]  # a missing name raises KeyError(name)

    def names(self) -> list[str]:
        return sorted(self._items)


def check_registry() -> None:
    report("5. Registry[T]", EXERCISES["test_registry"], Registry)


def main() -> None:
    check_first()
    check_parse_mode()
    check_double()
    check_compose()
    check_registry()


if __name__ == "__main__":
    main()
