"""Practice: errors and exceptions (chapter 11).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch11_errors.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch11_errors.py: try first, peek second. The lessons
for this chapter are in basics/11_errors/.
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


# --- Exercise 1 -------------------------------------------------------------

def safe_int(text: str, default: int = 0) -> int:
    """Convert text to an int, or return `default` if it is not a number.

    Use try/except and catch only ValueError. A wrong *type*, such as None,
    is a bug in the caller and should still raise TypeError.

    >>> safe_int("42"), safe_int(" 7 "), safe_int("abc"), safe_int("x", -1)
    (42, 7, 0, -1)
    """
    raise NotImplementedError


def test_safe_int(impl: Callable[..., int]) -> None:
    cases = [("42", 42), (" 7 ", 7), ("-3", -3), ("abc", 0), ("", 0), ("4.5", 0)]
    for text, expected in cases:
        got = impl(text)
        assert got == expected, f"safe_int({text!r}) should be {expected}, got {got}"
    assert impl("x", -1) == -1, "safe_int('x', -1) should return the default -1"
    assert impl("12", -1) == 12, "the default is only for bad input"
    try:
        impl(None)
    except TypeError:
        pass
    else:
        raise AssertionError("safe_int(None) should raise TypeError: catch only "
                             "ValueError")


def check_safe_int() -> None:
    report("1. safe_int", test_safe_int, safe_int)


# --- Exercise 2 -------------------------------------------------------------

def parse_age(text: str) -> int:
    """Parse an age between 0 and 150, raising ValueError with a clear message.

    - Not a whole number: raise ValueError("age must be a whole number, got
      'abc'") *from* the original error, so the traceback keeps the cause.
    - Outside 0..150: raise ValueError("age out of range: 200").

    >>> parse_age("30")
    30
    """
    raise NotImplementedError


def test_parse_age(impl: Callable[[str], int]) -> None:
    for text, expected in [("30", 30), ("0", 0), ("150", 150)]:
        got = impl(text)
        assert got == expected, f"parse_age({text!r}) should be {expected}, got {got}"
    try:
        impl("abc")
    except ValueError as exc:
        expected = "age must be a whole number, got 'abc'"
        assert str(exc) == expected, f"message was {str(exc)!r}, not {expected!r}"
        assert isinstance(exc.__cause__, ValueError), (
            "use 'raise ... from exc' so the original error is kept as the cause"
        )
    else:
        raise AssertionError("parse_age('abc') should raise ValueError")
    for text in ("-1", "151"):
        try:
            impl(text)
        except ValueError as exc:
            expected = f"age out of range: {text}"
            assert str(exc) == expected, f"message was {str(exc)!r}, not {expected!r}"
        else:
            raise AssertionError(f"parse_age({text!r}) should raise ValueError")


def check_parse_age() -> None:
    report("2. parse_age", test_parse_age, parse_age)


# --- Exercise 3 -------------------------------------------------------------

class InsufficientFunds(Exception):
    """Raised when a withdrawal is bigger than the balance.

    InsufficientFunds(balance, amount) should store `balance` and `amount`
    as attributes, plus `shortfall` (amount - balance), and pass a readable
    message to super().__init__ so that:

    >>> str(InsufficientFunds(10, 60))
    'cannot withdraw 60.00 from a balance of 10.00'
    """

    def __init__(self, balance: float, amount: float) -> None:
        raise NotImplementedError


def test_insufficient_funds(impl: type) -> None:
    err = impl(10, 60)
    assert isinstance(err, Exception), "inherit from Exception"
    assert (err.balance, err.amount) == (10, 60), "store balance and amount"
    assert err.shortfall == 50, f"shortfall should be 50, got {err.shortfall}"
    expected = "cannot withdraw 60.00 from a balance of 10.00"
    assert str(err) == expected, f"str() was {str(err)!r}, expected {expected!r}"
    try:
        raise impl(5, 7.5)
    except impl as caught:  # callers can catch exactly this error
        assert caught.shortfall == 2.5, "shortfall should be 2.5 for (5, 7.5)"


def check_insufficient_funds() -> None:
    report("3. InsufficientFunds", test_insufficient_funds, InsufficientFunds)


# --- Exercise 4 -------------------------------------------------------------

def retry(func: Callable[[], str], attempts: int) -> str:
    """Call func() and return its result, retrying on ConnectionError.

    - Try at most `attempts` times in total (attempts is at least 1).
    - If every try raises ConnectionError, re-raise the last one (a bare
      `raise` inside the except block does that).
    - Any other exception is not worth retrying: let it through at once.
    """
    raise NotImplementedError


def test_retry(impl: Callable[[Callable[[], str], int], str]) -> None:
    calls = 0

    def flaky(failures: int, error: type[Exception]) -> Callable[[], str]:
        """Make a func that raises `error` for its first `failures` calls."""
        def func() -> str:
            nonlocal calls
            calls += 1
            if calls <= failures:
                raise error(f"failure {calls}")
            return "ok"
        return func

    calls = 0
    result = impl(flaky(0, ConnectionError), 1)
    assert result == "ok", f"a first-try success should return 'ok', got {result!r}"
    calls = 0
    result = impl(flaky(2, ConnectionError), 3)
    assert result == "ok", f"2 failures then success should give 'ok', got {result!r}"
    assert calls == 3, f"func should be called 3 times, was called {calls}"
    calls = 0
    try:
        impl(flaky(10, ConnectionError), 3)
    except ConnectionError as exc:
        assert calls == 3, f"stop after 3 attempts, but func ran {calls} times"
        assert str(exc) == "failure 3", f"re-raise the last error, got {exc!r}"
    else:
        raise AssertionError("after 3 failed attempts the error should be raised")
    calls = 0
    try:
        impl(flaky(10, ValueError), 3)
    except ValueError:
        assert calls == 1, f"do not retry a ValueError; func ran {calls} times"
    else:
        raise AssertionError("a ValueError should pass straight through")


def check_retry() -> None:
    report("4. retry", test_retry, retry)


# --- Exercise 5 -------------------------------------------------------------

def validate_order(order: dict[str, object]) -> None:
    """Check an order and report *every* problem at once.

    Collect an exception for each problem below, in this order:
        "item" missing or ""          ValueError("item is required")
        "quantity" is not an int      TypeError("quantity must be an int")
        "quantity" is an int below 1  ValueError("quantity must be at least 1")
        "email" has no "@"            ValueError("email needs an @")
    If the list is not empty, raise ExceptionGroup("invalid order", errors).
    A valid order returns None.
    """
    raise NotImplementedError


def test_validate_order(impl: Callable[[dict[str, object]], None]) -> None:
    good = {"item": "lamp", "quantity": 2, "email": "ana@example.com"}
    assert impl(good) is None, "a valid order should return None"

    def problems(order: dict[str, object]) -> list[str]:
        try:
            impl(order)
        except ExceptionGroup as group:
            assert group.message == "invalid order", "name the group 'invalid order'"
            return [f"{type(e).__name__}: {e}" for e in group.exceptions]
        return []

    found = problems({**good, "quantity": 0})
    expected = ["ValueError: quantity must be at least 1"]
    assert found == expected, f"quantity 0 gave {found}"
    found = problems({"quantity": "two", "email": "nope"})
    expected = ["ValueError: item is required",
                "TypeError: quantity must be an int",
                "ValueError: email needs an @"]
    assert found == expected, f"a bad order gave {found}, expected {expected}"


def check_validate_order() -> None:
    report("5. validate_order", test_validate_order, validate_order)


# --- Exercise 6 -------------------------------------------------------------

def split_errors(group: ExceptionGroup) -> tuple[list[str], list[str]]:
    """Return (ValueError messages, TypeError messages) from an exception group.

    Raise the group inside try and handle it with `except* ValueError` and
    `except* TypeError`. Groups can be nested, so walk into any group you
    find and keep the messages in left-to-right order. Any other exception
    type is not yours to handle: except* re-raises it for you.

    >>> group = ExceptionGroup("bad", [ValueError("a"), TypeError("b")])
    >>> split_errors(group)
    (['a'], ['b'])
    """
    raise NotImplementedError


def test_split_errors(impl: Callable[[ExceptionGroup], Any]) -> None:
    flat = ExceptionGroup("x", [ValueError("a"), TypeError("b"), ValueError("c")])
    result = impl(flat)
    assert result == (["a", "c"], ["b"]), f"flat group gave {result}"
    nested = ExceptionGroup("outer", [
        ValueError("a"),
        ExceptionGroup("inner", [TypeError("b"), ValueError("c")]),
        TypeError("d"),
    ])
    result = impl(nested)
    assert result == (["a", "c"], ["b", "d"]), f"nested group gave {result}"
    only_types = ExceptionGroup("x", [TypeError("t")])
    result = impl(only_types)
    assert result == ([], ["t"]), f"a group of one TypeError gave {result}"
    mixed = ExceptionGroup("x", [ValueError("a"), KeyError("k")])
    try:
        impl(mixed)
    except ExceptionGroup as leftover:
        assert leftover.subgroup(KeyError), "the KeyError should be re-raised"
        assert not leftover.subgroup(ValueError), "ValueErrors are handled"
    else:
        raise AssertionError("an unhandled KeyError should be re-raised")


def check_split_errors() -> None:
    report("6. split_errors", test_split_errors, split_errors)


def main() -> None:
    check_safe_int()
    check_parse_age()
    check_insufficient_funds()
    check_retry()
    check_validate_order()
    check_split_errors()


if __name__ == "__main__":
    main()
