"""Lazy pipelines: composing generators so data flows one item at a time.

A chain of list comprehensions materialises every intermediate stage. The same
chain written with generator expressions materialises nothing — each item is
pulled through the whole pipeline before the next one is read, so memory stays
flat whether the source has a thousand rows or a billion.

The consumer decides how much work happens. `next()` on a pipeline over an
infinite source does exactly one item's worth. `sum()` walks the whole thing.
That inversion — the end of the chain driving the start — is the point.

The cost: a generator is single-use, and debugging a lazy chain shows you
generator objects rather than values until you consume it.
"""

import itertools
import sys
from collections.abc import Iterable, Iterator


def read_lines() -> Iterator[str]:
    """Stands in for a file or socket: yields, never returns a list."""
    for i in range(1, 1_000_001):
        yield f"{i},user{i % 100},{i * 3 % 997}"


def parse(lines: Iterable[str]) -> Iterator[tuple[int, str, int]]:
    for line in lines:
        row_id, user, score = line.split(",")
        yield int(row_id), user, int(score)


def filter_high(rows: Iterable[tuple[int, str, int]], threshold: int):
    return (row for row in rows if row[2] >= threshold)


def take(rows: Iterable[tuple[int, str, int]], n: int) -> list:
    return list(itertools.islice(rows, n))


def main() -> None:
    print("a pipeline over a million rows, without holding any of them:")
    pipeline = filter_high(parse(read_lines()), threshold=990)
    print(f"  first 3 matches: {take(pipeline, 3)}")
    print("  the source generator is still paused mid-stream")

    print("memory: list stage vs generator stage")
    listed = [n * n for n in range(200_000)]
    lazy = (n * n for n in range(200_000))
    print(f"  list comprehension: {sys.getsizeof(listed):>9} bytes")
    print(f"  generator expression:{sys.getsizeof(lazy):>9} bytes")

    print("the consumer decides how much work happens:")
    counted = itertools.count(1)
    squares = (n * n for n in counted)
    evens = (s for s in squares if s % 2 == 0)
    print(f"  first 5 even squares from an infinite source: "
          f"{list(itertools.islice(evens, 5))}")

    print("aggregation without materialising:")
    total = sum(score for _, _, score in parse(read_lines()))
    print(f"  sum of a million scores: {total}")

    print("single-use is the trade:")
    once = (n for n in range(3))
    print(f"  first pass {list(once)}, second pass {list(once)}")
    print("  tee() duplicates it, at the cost of buffering the difference:")
    a, b = itertools.tee(n for n in range(3))
    print(f"  {list(a)} and {list(b)}")

    print("chaining stays flat, not nested:")
    stages = [
        lambda rows: ((i, u, s * 2) for i, u, s in rows),
        lambda rows: (r for r in rows if r[0] % 2 == 0),
    ]
    data = parse(itertools.islice(read_lines(), 10))
    for stage in stages:
        data = stage(data)
    print(f"  {list(data)[:3]}")


if __name__ == "__main__":
    main()
