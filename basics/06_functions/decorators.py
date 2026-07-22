"""Decorators — a function that wraps another function.

`@decorator` above a `def` is pure syntax sugar for:

    fn = decorator(fn)

That is the whole idea. A decorator takes a function, returns a replacement,
and the name now points at the replacement. Because the replacement is usually
a closure, it can run code before and after the original call.

Always apply `functools.wraps` to the inner function: without it the wrapper
replaces the original's name, docstring, and signature metadata.
"""

import functools
import time


def logged(fn):
    """Print each call and its result."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"  -> {fn.__name__}{args}")
        result = fn(*args, **kwargs)
        print(f"  <- {result}")
        return result

    return wrapper


def repeat(times: int):
    """A decorator *factory*: takes an argument, returns a decorator."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result

        return wrapper

    return decorator


@logged
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@repeat(3)
def ping() -> str:
    print("  ping")
    return "pong"


@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    """Naive recursion, made fast by the standard library's memo decorator."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def main() -> None:
    print("logged:")
    add(2, 3)

    print("repeat(3):")
    print(f"  result = {ping()}")

    # wraps preserved the identity of the original function.
    print(f"add.__name__ = {add.__name__}, doc = {add.__doc__!r}")

    start = time.perf_counter()
    print(f"fib(90) = {fib(90)}")
    print(f"took {(time.perf_counter() - start) * 1000:.3f} ms thanks to lru_cache")
    print(f"cache: {fib.cache_info()}")

    # Stacked decorators apply bottom-up: @a @b def f -> a(b(f)).


if __name__ == "__main__":
    main()
