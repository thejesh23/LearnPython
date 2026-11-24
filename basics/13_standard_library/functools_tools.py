"""`functools` — tools that take functions and give back better functions.

    cache / lru_cache   remember results so repeated calls are instant
    partial             pre-fill some arguments of an existing function
    reduce              fold a sequence down to one value
    singledispatch      choose an implementation by the type of the argument
    cached_property     compute an attribute once, on first access

The common thread: functions are ordinary objects in Python, so you can pass
them around, wrap them, and build new ones from old ones.
"""

import operator
import time
from functools import cache
from functools import cached_property
from functools import partial
from functools import reduce
from functools import singledispatch


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


def power(base: float, exponent: float) -> float:
    return base**exponent


def partial_demo() -> None:
    # partial(f, ...) returns a new callable with some arguments already set.
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    print(f"square(7) = {square(7)}, cube(2) = {cube(2)}")

    # Handy wherever an API wants a one-argument function.
    parse_binary = partial(int, base=2)
    print(f"binary strings: {list(map(parse_binary, ['101', '1111', '10000']))}")


def reduce_demo() -> None:
    # reduce(f, items) computes f(f(f(a, b), c), d): it folds left to right.
    numbers = [1, 2, 3, 4, 5]
    product = reduce(operator.mul, numbers)
    print(f"product of {numbers} = {product}")

    # A starting value handles the empty case, which otherwise raises.
    print(f"product of [] with start 1 = {reduce(operator.mul, [], 1)}")

    # Prefer a built-in when one exists: sum(), max(), any(), "".join(),
    # and math.prod() say what they do. reduce is for the folds left over.
    nested = [[1, 2], [3], [4, 5]]
    print(f"flattened with reduce: {reduce(operator.add, nested, [])}")


@singledispatch
def describe(value: object) -> str:
    return f"something else: {value!r}"


@describe.register
def _(value: int) -> str:
    return f"an int; doubled it is {value * 2}"


@describe.register
def _(value: list) -> str:
    return f"a list of {len(value)} items"


def singledispatch_demo() -> None:
    # Instead of a chain of isinstance() checks inside one function, each
    # type gets its own small function, and new types can be added later.
    for value in [12345, [1, 2, 3], "hi", True]:
        print(f"{value!r:>12} -> {describe(value)}")
    # True counts as an int, because bool is a subclass of int.


class Document:
    def __init__(self, text: str) -> None:
        self.text = text

    @cached_property
    def word_count(self) -> int:
        # Runs on the first access only; the result is then stored on the
        # instance like a normal attribute.
        print("  (counting words...)")
        return len(self.text.split())


def cached_property_demo() -> None:
    doc = Document("the quick brown fox jumps over the lazy dog")
    print(f"first access: {doc.word_count}")
    print(f"second access: {doc.word_count}")
    # Unlike @property, the value does not follow later changes to self.text.
    # Delete the attribute to force a recount.
    doc.text += " again"
    del doc.word_count
    print(f"after del: {doc.word_count}")


def main() -> None:
    cache_demo()
    print()
    partial_demo()
    print()
    reduce_demo()
    print()
    singledispatch_demo()
    print()
    cached_property_demo()


if __name__ == "__main__":
    main()
