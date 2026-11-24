"""Practice exercises for basics/01_variables: assignment and unpacking.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch01_variables.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

Each exercise is a function. The values arrive as its parameters, and
`return` hands your answer back; that is all you need to know about
functions until basics/06. Nothing here needs more than basics/00 and
basics/01 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch01_variables.py. Try each exercise yourself first.
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


def swap(a: Any, b: Any) -> tuple[Any, Any]:
    """Return the two values in the opposite order, as a tuple.

    swap(1, 2)      -> (2, 1)
    swap("x", "y")  -> ("y", "x")

    Hint: Python can swap two names in one line, with no temporary variable.
    """
    raise NotImplementedError


def test_swap(fn: Callable[..., Any]) -> None:
    cases = [((1, 2), (2, 1)), (("x", "y"), ("y", "x")), ((7, 7), (7, 7))]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"swap{args} returned {got!r}, expected {want!r}"


def check_swap() -> None:
    report("1. swap", test_swap, swap)


def rotate_left(a: Any, b: Any, c: Any) -> tuple[Any, Any, Any]:
    """Move every value one place to the left; the first wraps to the end.

    rotate_left(1, 2, 3)       -> (2, 3, 1)
    rotate_left("a", "b", "c") -> ("b", "c", "a")
    """
    raise NotImplementedError


def test_rotate_left(fn: Callable[..., Any]) -> None:
    cases = [
        ((1, 2, 3), (2, 3, 1)),
        (("a", "b", "c"), ("b", "c", "a")),
        ((0, 0, 1), (0, 1, 0)),
    ]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"rotate_left{args} returned {got!r}, expected {want!r}"


def check_rotate_left() -> None:
    report("2. rotate_left", test_rotate_left, rotate_left)


def main() -> None:
    check_swap()
    check_rotate_left()


if __name__ == "__main__":
    main()
