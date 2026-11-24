"""Practice exercises for basics/02_types: numbers, text, truth and None.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch02_types.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

Nothing here needs more than basics/00 to basics/02 cover. Two exercises
use Decimal and Fraction from the standard library; their hints show the
import line to add at the top of this file.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch02_types.py. Try each exercise yourself first.
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


def utf8_length(text: str) -> tuple[int, int]:
    """Return (characters, bytes): the length of text, and of its UTF-8 form.

    utf8_length("hello") -> (5, 5)
    utf8_length("héllo") -> (5, 6)    the é takes two bytes
    utf8_length("☃")     -> (1, 3)
    """
    raise NotImplementedError


def test_utf8_length(fn: Callable[..., Any]) -> None:
    cases = [("hello", (5, 5)), ("héllo", (5, 6)), ("☃", (1, 3)), ("", (0, 0))]
    for text, want in cases:
        got = fn(text)
        assert got == want, f"utf8_length({text!r}) returned {got!r}, expected {want!r}"


def check_utf8_length() -> None:
    report("1. utf8_length", test_utf8_length, utf8_length)


def split_seconds(total: int) -> tuple[int, int, int]:
    """Split a number of seconds into (hours, minutes, seconds).

    Hours are not wrapped at 24: a long duration simply has many hours.

    split_seconds(3725)  -> (1, 2, 5)
    split_seconds(59)    -> (0, 0, 59)
    split_seconds(90061) -> (25, 1, 1)

    Hint: divmod(a, b) gives the quotient and the remainder at once.
    """
    raise NotImplementedError


def test_split_seconds(fn: Callable[..., Any]) -> None:
    cases = [
        (3725, (1, 2, 5)),
        (59, (0, 0, 59)),
        (0, (0, 0, 0)),
        (3600, (1, 0, 0)),
        (90061, (25, 1, 1)),
    ]
    for total, want in cases:
        got = fn(total)
        assert got == want, (
            f"split_seconds({total}) returned {got!r}, expected {want!r}"
        )


def check_split_seconds() -> None:
    report("2. split_seconds", test_split_seconds, split_seconds)


def main() -> None:
    check_utf8_length()
    check_split_seconds()


if __name__ == "__main__":
    main()
