"""Generator pipelines: chaining lazy steps so data flows one item at a time.

A *generator expression* looks like a list comprehension with round brackets:
`(n * n for n in numbers)`. Instead of building the whole list, it produces
each value only when asked for it.

Chain several of them, each reading from the one before, and you get a
*pipeline*. Nothing runs until the last step asks for a value; then a single
item travels through every step before the next item is read. So memory use
stays small and flat, however much data passes through, and a pipeline can
even read from an endless source as long as something stops it.

basics/08_iterators/generators.py introduces `yield`. This file is about
connecting generators together. advanced/lazy_evaluation_pipelines.py goes
further.
"""

import sys
from collections.abc import Iterable
from collections.abc import Iterator


def genexp_demo() -> None:
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]

    squares_list = [n * n for n in numbers]  # built now, all at once
    squares_gen = (n * n for n in numbers)  # built later, one at a time
    print(f"list comprehension: {squares_list}")
    print(f"generator expression: {type(squares_gen).__name__} object")
    print(f"next() -> {next(squares_gen)}, next() -> {next(squares_gen)}")

    # As the only argument to a function, the extra brackets can be dropped.
    print(f"sum of squares = {sum(n * n for n in numbers)}")
    print(f"any above 8?   = {any(n > 8 for n in numbers)}")
    print(f"longest word   = {max(len(w) for w in ['fig', 'banana', 'kiwi'])}")

    # A generator is used up after one pass; it does not restart.
    evens = (n for n in numbers if n % 2 == 0)
    print(f"first pass:  {list(evens)}")
    print(f"second pass: {list(evens)}   <- already exhausted")


LOG = [
    "2026-01-05 INFO  started",
    "2026-01-05 ERROR disk full",
    "",
    "2026-01-06 WARN  slow response",
    "2026-01-06 ERROR timeout",
    "2026-01-07 INFO  stopped",
]


def read_lines(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        print(f"    read   {line!r}")
        yield line


def parse(lines: Iterable[str]) -> Iterator[tuple[str, str, str]]:
    for line in lines:
        if line:  # skip blank lines
            date, level, message = line.split(maxsplit=2)
            yield date, level, message


def errors_only(records: Iterable[tuple[str, str, str]]) -> Iterator[str]:
    for date, level, message in records:
        if level == "ERROR":
            yield f"{date}: {message}"


def pipeline_demo() -> None:
    # Building the pipeline runs nothing: each step just wraps the one before.
    pipeline = errors_only(parse(read_lines(LOG)))
    print(f"pipeline built: {type(pipeline).__name__}, no lines read yet")

    # Pulling values drives it. Watch each line go all the way through
    # before the next line is read.
    for report in pipeline:
        print(f"  ERROR -> {report}")

    # The same pipeline written with generator expressions.
    parsed = (line.split(maxsplit=2) for line in LOG if line)
    errors = (f"{d}: {m}" for d, level, m in parsed if level == "ERROR")
    print(f"genexp version: {list(errors)}")


def memory_demo() -> None:
    # A list stores every element, so its size grows with the data.
    # A generator stores only its current position, so its size does not.
    for n in [10, 1_000, 1_000_000]:
        as_list = [x * 2 for x in range(n)]
        as_gen = (x * 2 for x in range(n))
        print(f"n = {n:>9,}: list {sys.getsizeof(as_list):>9,} bytes, "
              f"generator {sys.getsizeof(as_gen):>4} bytes")

    # Summing through a pipeline never holds more than one number at a time.
    total = sum(x * 2 for x in range(1_000_000) if x % 3 == 0)
    print(f"sum via pipeline = {total:,}")
    # (getsizeof counts the container itself, not the objects it refers to,
    # so the true cost of the list is even larger.)


def main() -> None:
    genexp_demo()
    print()
    pipeline_demo()
    print()
    memory_demo()


if __name__ == "__main__":
    main()
