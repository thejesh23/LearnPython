"""Practice exercises for basics/04_strings: methods, f-strings and slicing.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch04_strings.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

None of these needs a loop: string methods, format specs and slices do the
work. Nothing needs more than basics/00 to basics/04 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch04_strings.py. Try each exercise yourself first.
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


def format_price(amount: float) -> str:
    """Format an amount as dollars: a $ sign, comma separators, two decimals.

    format_price(3.5)     -> "$3.50"
    format_price(1234.5)  -> "$1,234.50"
    format_price(1000000) -> "$1,000,000.00"

    Hint: the format specs `,` and `.2f` can be combined in one f-string.
    """
    raise NotImplementedError


def test_format_price(fn: Callable[..., Any]) -> None:
    cases = [
        (3.5, "$3.50"),
        (0, "$0.00"),
        (1234.5, "$1,234.50"),
        (1000000, "$1,000,000.00"),
        (19.999, "$20.00"),
        (999.99, "$999.99"),
    ]
    for amount, want in cases:
        got = fn(amount)
        assert got == want, (
            f"format_price({amount!r}) returned {got!r}, expected {want!r}"
        )


def check_format_price() -> None:
    report("1. format_price", test_format_price, format_price)


def initials(full_name: str) -> str:
    """Return the initials of a two-word name, upper case, each with a dot.

    The name may have stray spaces and any capitalisation.

    initials("Ada Lovelace")      -> "A.L."
    initials("  grace   hopper ") -> "G.H."
    """
    raise NotImplementedError


def test_initials(fn: Callable[..., Any]) -> None:
    cases = [
        ("Ada Lovelace", "A.L."),
        ("  grace   hopper ", "G.H."),
        ("alan Turing", "A.T."),
        ("Q X", "Q.X."),
    ]
    for name, want in cases:
        got = fn(name)
        assert got == want, f"initials({name!r}) returned {got!r}, expected {want!r}"


def check_initials() -> None:
    report("2. initials", test_initials, initials)


def main() -> None:
    check_format_price()
    check_initials()


if __name__ == "__main__":
    main()
