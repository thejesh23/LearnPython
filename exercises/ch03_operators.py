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


def in_range(x: float, low: float, high: float) -> bool:
    """Return True when low <= x <= high (both ends included).

    in_range(5, 1, 10)  -> True
    in_range(10, 1, 10) -> True
    in_range(11, 1, 10) -> False

    Hint: Python lets you write this the way you would in maths.
    """
    raise NotImplementedError


def test_in_range(fn: Callable[..., Any]) -> None:
    cases = [
        ((5, 1, 10), True),
        ((1, 1, 10), True),
        ((10, 1, 10), True),
        ((0, 1, 10), False),
        ((11, 1, 10), False),
        ((2.5, 2, 3), True),
        ((-3, -5, -2), True),
        ((-1, -5, -2), False),
    ]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"in_range{args} returned {got!r}, expected {want!r}"


def check_in_range() -> None:
    report("2. in_range", test_in_range, in_range)


def display_name(name: str, nickname: str) -> str:
    """Return the nickname, or the full name when the nickname is empty.

    display_name("Robert", "Bob") -> "Bob"
    display_name("Robert", "")    -> "Robert"

    Hint: `or` returns one of its operands, not just True or False.
    """
    raise NotImplementedError


def test_display_name(fn: Callable[..., Any]) -> None:
    cases = [
        (("Robert", "Bob"), "Bob"),
        (("Robert", ""), "Robert"),
        (("Ada", "Ada"), "Ada"),
        (("Margaret", "Peggy"), "Peggy"),
    ]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"display_name{args} returned {got!r}, expected {want!r}"


def check_display_name() -> None:
    report("3. display_name", test_display_name, display_name)


def is_vowel(ch: str) -> bool:
    """Return True when the single character ch is a vowel, in either case.

    The vowels are a, e, i, o and u.

    is_vowel("a") -> True
    is_vowel("E") -> True
    is_vowel("y") -> False
    """
    raise NotImplementedError


def test_is_vowel(fn: Callable[..., Any]) -> None:
    cases = [
        ("a", True),
        ("E", True),
        ("u", True),
        ("O", True),
        ("b", False),
        ("y", False),
        ("Z", False),
        ("!", False),
    ]
    for ch, want in cases:
        got = fn(ch)
        assert got == want, f"is_vowel({ch!r}) returned {got!r}, expected {want!r}"


def check_is_vowel() -> None:
    report("4. is_vowel", test_is_vowel, is_vowel)


def is_leap_year(year: int) -> bool:
    """Return True for a leap year in the Gregorian calendar.

    A year is a leap year when it divides by 4, except that years dividing
    by 100 are not, except that years dividing by 400 are after all.

    is_leap_year(2024) -> True
    is_leap_year(1900) -> False    divides by 100
    is_leap_year(2000) -> True     divides by 400
    """
    raise NotImplementedError


def test_is_leap_year(fn: Callable[..., Any]) -> None:
    cases = [
        (2024, True),
        (2023, False),
        (1900, False),
        (2000, True),
        (2100, False),
        (2400, True),
        (1996, True),
    ]
    for year, want in cases:
        got = fn(year)
        assert got == want, f"is_leap_year({year}) returned {got!r}, expected {want!r}"


def check_is_leap_year() -> None:
    report("5. is_leap_year", test_is_leap_year, is_leap_year)


def ceil_div(a: int, b: int) -> int:
    """Divide a by b (b > 0) and round the answer up to a whole number.

    Handy for "how many boxes of 6 do I need for 14 eggs?" (3 boxes).

    ceil_div(14, 6) -> 3
    ceil_div(12, 6) -> 2
    ceil_div(-7, 2) -> -3    up means towards positive infinity

    It must be exact even for huge numbers, so avoid `/`, which makes a
    float. Hint: // rounds down. What does it do to a negated number?
    """
    raise NotImplementedError


def test_ceil_div(fn: Callable[..., Any]) -> None:
    cases = [
        ((14, 6), 3),
        ((12, 6), 2),
        ((0, 5), 0),
        ((1, 5), 1),
        ((-7, 2), -3),
        ((10**20 + 1, 10**20), 2),
    ]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"ceil_div{args} returned {got!r}, expected {want!r}"


def check_ceil_div() -> None:
    report("6. ceil_div", test_ceil_div, ceil_div)


def main() -> None:
    check_is_even()
    check_in_range()
    check_display_name()
    check_is_vowel()
    check_is_leap_year()
    check_ceil_div()


if __name__ == "__main__":
    main()
