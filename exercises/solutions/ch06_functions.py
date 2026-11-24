"""Worked solutions for exercises/ch06_functions.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import functools
import runpy
from collections.abc import Callable
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


def make_greeting(name: str, greeting: str = "Hello", *, punctuation: str = "!") -> str:
    # Everything after the bare * must be passed by name, so a call can
    # never set punctuation by accident through a third positional value.
    return f"{greeting}, {name}{punctuation}"


def check_make_greeting() -> None:
    report("2. make_greeting", EXERCISES["test_make_greeting"], make_greeting)


def append_to(item: int, items: list[int] | None = None) -> list[int]:
    # A default is built once, when def runs, so [] there would be one list
    # shared by every call. None as the default and a fresh list inside
    # gives each call its own.
    if items is None:
        items = []
    items.append(item)
    return items


def check_append_to() -> None:
    report("3. append_to", EXERCISES["test_append_to"], append_to)


def by_last_name(names: list[str]) -> list[str]:
    # sorted() returns a new list and leaves the input alone, and it is
    # stable, so equal last names stay in their original order.
    return sorted(names, key=lambda name: name.split()[-1])


def check_by_last_name() -> None:
    report("4. by_last_name", EXERCISES["test_by_last_name"], by_last_name)


def make_accumulator(start: float = 0) -> Callable[[float], float]:
    # Each call of make_accumulator creates a new `total`, and the inner
    # function closes over that one. nonlocal lets it assign to it.
    total = start

    def add(amount: float) -> float:
        nonlocal total
        total += amount
        return total

    return add


def check_make_accumulator() -> None:
    report("5. make_accumulator", EXERCISES["test_make_accumulator"],
           make_accumulator)


def uppercase_result(fn: Callable[..., str]) -> Callable[..., str]:
    # *args and **kwargs forward any call unchanged; functools.wraps copies
    # the name and docstring onto the wrapper.
    @functools.wraps(fn)
    def wrapper(*args: object, **kwargs: object) -> str:
        return fn(*args, **kwargs).upper()

    return wrapper


def check_uppercase_result() -> None:
    report("6. uppercase_result", EXERCISES["test_uppercase_result"],
           uppercase_result)


def main() -> None:
    check_average()
    check_make_greeting()
    check_append_to()
    check_by_last_name()
    check_make_accumulator()
    check_uppercase_result()


if __name__ == "__main__":
    main()
