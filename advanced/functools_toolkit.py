"""`functools` — the standard library's function-manipulation kit.

The pieces worth knowing by heart:
    cache / lru_cache      memoisation, one decorator
    partial                freeze arguments, produce a new callable
    reduce                 fold a sequence (usually a loop is clearer)
    wraps                  preserve metadata when writing a decorator
    singledispatch         type-based dispatch without an if-elif chain
    cached_property        compute once per instance, store in __dict__
    total_ordering         all six comparisons from __eq__ and __lt__
"""

import functools
import time
from functools import (
    cache,
    cached_property,
    partial,
    reduce,
    singledispatch,
    total_ordering,
)


@cache  # unbounded lru_cache, 3.9+
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@singledispatch
def describe(value) -> str:
    return f"some {type(value).__name__}"


@describe.register
def _(value: int) -> str:
    return f"the integer {value}"


@describe.register
def _(value: list) -> str:
    return f"a list of {len(value)} items"


@describe.register(str)
def _(value: str) -> str:
    return f"the string {value!r}"


@total_ordering
class Version:
    def __init__(self, major: int, minor: int) -> None:
        self.major, self.minor = major, minor

    def __eq__(self, other: object) -> bool:
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other: "Version") -> bool:
        return (self.major, self.minor) < (other.major, other.minor)

    def __repr__(self) -> str:
        return f"v{self.major}.{self.minor}"


class Dataset:
    def __init__(self, values: list[int]) -> None:
        self.values = values

    @cached_property
    def total(self) -> int:
        print("  (computing total once)")
        return sum(self.values)


def main() -> None:
    start = time.perf_counter()
    print(f"fib(200) = {fib(200)}")
    print(f"in {(time.perf_counter() - start) * 1000:.2f} ms; {fib.cache_info()}")

    # partial freezes arguments.
    to_hex = partial(int, base=16)
    print(f"to_hex('ff') = {to_hex('ff')}")
    add_ten = partial(lambda a, b: a + b, 10)
    print(f"add_ten(5) = {add_ten(5)}")

    print(f"reduce: {reduce(lambda a, b: a * b, range(1, 6))}")

    for value in (42, "hi", [1, 2, 3], 3.14):
        print(f"  describe({value!r}) -> {describe(value)}")

    versions = [Version(1, 2), Version(1, 0), Version(2, 0)]
    print(f"sorted: {sorted(versions)}, max: {max(versions)}, "
          f">= works: {Version(2, 0) >= Version(1, 9)}")

    d = Dataset([1, 2, 3])
    print(f"total {d.total}, again {d.total} (cached: {'total' in d.__dict__})")

    # A decorator without wraps loses the wrapped function's identity.
    def bad(fn):
        def inner(*a, **k):
            return fn(*a, **k)
        return inner

    def good(fn):
        @functools.wraps(fn)
        def inner(*a, **k):
            return fn(*a, **k)
        return inner

    def original() -> None:
        """docs"""

    print(f"without wraps: {bad(original).__name__}, with wraps: {good(original).__name__}")


if __name__ == "__main__":
    main()
