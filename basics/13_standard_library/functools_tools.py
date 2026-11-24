"""`functools` — tools that take functions and give back better functions.

    cache / lru_cache   remember results so repeated calls are instant
    partial             pre-fill some arguments of an existing function
    reduce              fold a sequence down to one value
    singledispatch      choose an implementation by the type of the argument
    cached_property     compute an attribute once, on first access

The common thread: functions are ordinary objects in Python, so you can pass
them around, wrap them, and build new ones from old ones.
"""

import time
from functools import cache


@cache
def fib(n: int) -> int:
    # Without @cache this recursion recomputes the same values over and over
    # and fib(35) takes seconds. With it, each n is computed exactly once.
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def cache_demo() -> None:
    start = time.perf_counter()
    print(f"fib(90) = {fib(90)}")
    print(f"took {time.perf_counter() - start:.4f}s thanks to the cache")
    print(f"cache info: {fib.cache_info()}")
    # @cache only works when arguments are hashable and the function is
    # "pure": same inputs, same output, no side effects worth repeating.


def main() -> None:
    cache_demo()


if __name__ == "__main__":
    main()
