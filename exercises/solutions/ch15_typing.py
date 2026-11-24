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
from pathlib import Path
from typing import Literal, cast, get_args


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


def main() -> None:
    check_first()
    check_parse_mode()


if __name__ == "__main__":
    main()
