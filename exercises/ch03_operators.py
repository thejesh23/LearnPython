"""Practice exercises for basics/03_operators: arithmetic, comparison, logic.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch03_operators.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

Every answer here is a single expression built from operators, so each
function body can be one `return` line. Nothing needs more than basics/00
to basics/03 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch03_operators.py. Try each exercise yourself first.
"""

from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


def is_even(n: int) -> bool:
    """Return True when n is even, False when it is odd.

    is_even(4)  -> True
    is_even(7)  -> False
    is_even(-3) -> False
    """
    raise NotImplementedError


def test_is_even(fn: Callable[..., Any]) -> None:
    cases = [(4, True), (7, False), (0, True), (-3, False), (-8, True), (10**30, True)]
    for n, want in cases:
        got = fn(n)
        assert got == want, f"is_even({n}) returned {got!r}, expected {want!r}"


def check_is_even() -> None:
    report("1. is_even", test_is_even, is_even)


def main() -> None:
    check_is_even()


if __name__ == "__main__":
    main()
