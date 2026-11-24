"""Worked solutions for exercises/ch08_iterators.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch08_iterators.py")
)
report = EXERCISES["report"]


def first_or_default(iterable: Iterable[Any], default: Any = None) -> Any:
    # iter() works on any iterable; next() with a default returns it instead
    # of raising StopIteration. Only one item is ever read.
    return next(iter(iterable), default)


def check_first_or_default() -> None:
    report("1. first_or_default", EXERCISES["test_first_or_default"],
           first_or_default)


def countdown(n: int) -> Iterator[int]:
    # Each yield hands out one value and pauses here until the next is
    # asked for. When the loop ends, the generator is exhausted.
    while n > 0:
        yield n
        n -= 1


def check_countdown() -> None:
    report("2. countdown", EXERCISES["test_countdown"], countdown)


def running_total(numbers: Iterable[int]) -> Iterator[int]:
    # Read one number, yield one total: memory stays constant however long
    # the input is. itertools.accumulate(numbers) is the built-in version.
    total = 0
    for n in numbers:
        total += n
        yield total


def check_running_total() -> None:
    report("3. running_total", EXERCISES["test_running_total"], running_total)


def main() -> None:
    check_first_or_default()
    check_countdown()
    check_running_total()


if __name__ == "__main__":
    main()
