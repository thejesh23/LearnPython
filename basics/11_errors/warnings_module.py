"""`warnings` — telling the caller "this works, but you should change it".

An exception stops the program. A warning is a message that lets the program
carry on: "this function is deprecated", "this setting will change in the
next release". Library authors use warnings so users can upgrade at their own
pace; the user decides whether to see them, ignore them, or turn them into
errors.

Common categories (all subclasses of Warning):

    UserWarning          the default when you do not pick one
    DeprecationWarning   for developers: an API is going away. Hidden by
                         default unless triggered by code in __main__
    FutureWarning        for end users: behaviour is going to change
    RuntimeWarning       something dubious happened at runtime
    ResourceWarning      e.g. a file was never closed; hidden by default

Warnings go to stderr. This file wraps every one in
`warnings.catch_warnings(record=True)` so it can print them neatly instead.
The same switches exist outside Python code: `python -W error script.py`, or
the PYTHONWARNINGS environment variable.
"""

import functools
import linecache
import warnings
from collections.abc import Callable
from typing import Any


def old_total(prices: list[float]) -> float:
    # stacklevel=2 makes the warning point at the *caller's* line, which is
    # the line the user has to change, not this one.
    warnings.warn(
        "old_total() is deprecated; use sum() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return sum(prices)


def show(caught: list[warnings.WarningMessage]) -> None:
    for w in caught:
        source = linecache.getline(w.filename, w.lineno).strip()
        print(f"  {w.category.__name__}: {w.message}")
        print(f"    reported at: {source}")


def warn_demo() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")  # record every warning, no filtering
        total = old_total([1.5, 2.5])
        warnings.warn("cache size is very large")  # UserWarning by default
        warnings.warn("rounding will change in 2.0", FutureWarning)
    print(f"the code still ran: total = {total}")
    show(caught)


def filters_demo() -> None:
    with warnings.catch_warnings(record=True) as caught:
        # Filters are checked newest first; the first match decides.
        warnings.simplefilter("always")
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", message="noisy")  # regex on the text
        warnings.warn("rounding will change", FutureWarning)
        warnings.warn("noisy message from a library")
        warnings.warn("this one gets through")
    print(f"after ignore filters, {len(caught)} warning(s) recorded:")
    show(caught)

    with warnings.catch_warnings(record=True) as caught:
        # "once" shows a given message only the first time.
        warnings.simplefilter("once")
        for _ in range(3):
            warnings.warn("disk almost full", RuntimeWarning)
    print(f"'once' turned 3 identical warnings into {len(caught)}")


def as_errors_demo() -> None:
    # "error" raises the warning as an exception. Test suites often run with
    # -W error so deprecated calls fail loudly before the API is removed.
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        try:
            old_total([1.0])
        except DeprecationWarning as exc:
            print(f"raised as an exception: DeprecationWarning: {exc}")

    # catch_warnings restored the old filters on exit, so the "error" rule
    # is gone and the same call only warns again.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old_total([1.0])
    print(f"once the block ends it is just a warning: {len(caught)} recorded")


def deprecated(advice: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Mark a function as deprecated. (Python 3.13 adds warnings.deprecated.)"""

    def decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__}() is deprecated; {advice}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorate


@deprecated("use greet(name, polite=True)")
def say_hello(name: str) -> str:
    return f"Hello, {name}"


def deprecated_decorator_demo() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        print(f"result: {say_hello('Ada')}")
    show(caught)


def main() -> None:
    warn_demo()
    print()
    filters_demo()
    print()
    as_errors_demo()
    print()
    deprecated_decorator_demo()


if __name__ == "__main__":
    main()
