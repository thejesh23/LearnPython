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


def is_palindrome(text: str) -> bool:
    """Return True when text reads the same backwards, ignoring case and spaces.

    is_palindrome("racecar")           -> True
    is_palindrome("Never odd or even") -> True
    is_palindrome("Python")            -> False
    is_palindrome("")                  -> True
    """
    raise NotImplementedError


def test_is_palindrome(fn: Callable[..., Any]) -> None:
    cases = [
        ("racecar", True),
        ("Never odd or even", True),
        ("Was it a car or a cat I saw", True),
        ("Python", False),
        ("ab", False),
        ("A", True),
        ("", True),
    ]
    for text, want in cases:
        got = fn(text)
        assert got == want, (
            f"is_palindrome({text!r}) returned {got!r}, expected {want!r}"
        )


def check_is_palindrome() -> None:
    report("3. is_palindrome", test_is_palindrome, is_palindrome)


def mask_card(number: str) -> str:
    """Hide a card number except its last four digits.

    Remove the spaces first, then replace every digit but the last four
    with "*". Numbers of four digits or fewer come back unchanged.

    mask_card("4111 1111 1111 1234") -> "************1234"
    mask_card("1234567890")          -> "******7890"
    mask_card("12")                  -> "12"

    Hint: "*" * n repeats a string, and a slice never raises IndexError.
    """
    raise NotImplementedError


def test_mask_card(fn: Callable[..., Any]) -> None:
    cases = [
        ("4111 1111 1111 1234", "************1234"),
        ("1234567890", "******7890"),
        ("12345", "*2345"),
        ("1234", "1234"),
        ("12", "12"),
        ("", ""),
    ]
    for number, want in cases:
        got = fn(number)
        assert got == want, f"mask_card({number!r}) returned {got!r}, expected {want!r}"


def check_mask_card() -> None:
    report("4. mask_card", test_mask_card, mask_card)


def parse_setting(line: str) -> tuple[str, str]:
    """Split a "key = value" line into a (key, value) pair.

    Split at the first "=" only, so the value may contain "=" itself.
    Strip spaces from both parts. With no "=", the value is "".

    parse_setting("name = Ada")         -> ("name", "Ada")
    parse_setting("  debug=true ")      -> ("debug", "true")
    parse_setting("query = a=1")        -> ("query", "a=1")
    parse_setting("verbose")            -> ("verbose", "")
    """
    raise NotImplementedError


def test_parse_setting(fn: Callable[..., Any]) -> None:
    cases = [
        ("name = Ada", ("name", "Ada")),
        ("  debug=true ", ("debug", "true")),
        ("query = a=1", ("query", "a=1")),
        ("verbose", ("verbose", "")),
        ("empty =", ("empty", "")),
        ("greeting = hello world", ("greeting", "hello world")),
    ]
    for line, want in cases:
        got = fn(line)
        assert got == want, (
            f"parse_setting({line!r}) returned {got!r}, expected {want!r}"
        )


def check_parse_setting() -> None:
    report("5. parse_setting", test_parse_setting, parse_setting)


def main() -> None:
    check_format_price()
    check_initials()
    check_is_palindrome()
    check_mask_card()
    check_parse_setting()


if __name__ == "__main__":
    main()
