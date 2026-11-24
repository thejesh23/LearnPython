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

import linecache
import warnings


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


def main() -> None:
    warn_demo()


if __name__ == "__main__":
    main()
