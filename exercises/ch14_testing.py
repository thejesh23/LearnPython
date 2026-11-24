"""Practice: testing (chapter 14).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch14_testing.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch14_testing.py: try first, peek second. The lessons
for this chapter are in basics/14_testing/.
"""

import time
import unittest
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


# In this chapter you write the checks. Each exercise's test runs your code
# against a correct implementation (it must pass) and against buggy ones
# (each bug must be caught).

# --- Exercise 1 -------------------------------------------------------------

def check_is_leap(is_leap: Callable[[int], bool]) -> None:
    """Write asserts that pass for a correct is_leap and fail for buggy ones.

    The rule: a year is a leap year if it divides by 4, except that years
    dividing by 100 are leap years only when they also divide by 400.
    Pick years that cover every branch of that rule, for example:
        assert is_leap(2024), "2024 is a leap year"
        assert not is_leap(2023), "2023 is not a leap year"
    """
    raise NotImplementedError


def test_check_is_leap(impl: Callable[[Callable[[int], bool]], None]) -> None:
    def correct(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def no_century_rule(year: int) -> bool:
        return year % 4 == 0

    def no_400_rule(year: int) -> bool:
        return year % 4 == 0 and year % 100 != 0

    def every_even_year(year: int) -> bool:
        return year % 2 == 0

    def always(year: int) -> bool:
        return True

    try:
        impl(correct)
    except AssertionError as exc:
        raise AssertionError(f"a correct is_leap failed your check: {exc}") from None
    bugs = {
        "treats 1900 like a leap year": no_century_rule,
        "forgets that 2000 is a leap year": no_400_rule,
        "says every even year is a leap year": every_even_year,
        "says every year is a leap year": always,
    }
    for description, buggy in bugs.items():
        try:
            impl(buggy)
        except AssertionError:
            continue  # good: the bug was caught
        raise AssertionError(f"your checks missed an is_leap that {description}")


def check_check_is_leap() -> None:
    report("1. check_is_leap", test_check_is_leap, check_is_leap)


# --- Exercise 2 -------------------------------------------------------------

def assert_raises(
    exc_type: type[BaseException], func: Callable[..., Any], *args: Any
) -> BaseException:
    """A small version of unittest's assertRaises.

    Call func(*args).
      - If it raises exc_type (or a subclass), return the exception object,
        so the caller can look at its message.
      - If it raises nothing, raise AssertionError with the message
        "<function name> did not raise <exception name>", for example
        "int did not raise ValueError" (use func.__name__ and
        exc_type.__name__).
      - Any other exception is a real bug: let it pass through unchanged.

    >>> assert_raises(ValueError, int, "abc")
    ValueError("invalid literal for int() with base 10: 'abc'")
    """
    raise NotImplementedError


def test_assert_raises(impl: Callable[..., BaseException]) -> None:
    caught = impl(ValueError, int, "abc")
    assert isinstance(caught, ValueError), f"return the exception, got {caught!r}"
    assert "abc" in str(caught), "the returned exception should keep its message"
    caught = impl(LookupError, {}.__getitem__, "key")
    assert isinstance(caught, KeyError), "a subclass (KeyError) should count too"
    try:
        impl(ValueError, int, "5")
    except AssertionError as exc:
        expected = "int did not raise ValueError"
        assert str(exc) == expected, f"message was {str(exc)!r}, not {expected!r}"
    else:
        raise AssertionError("when nothing is raised, raise AssertionError")
    try:
        impl(KeyError, int, "abc")
    except ValueError:
        pass  # good: an unexpected error went straight through
    else:
        raise AssertionError("an exception of another type should pass through")


def check_assert_raises() -> None:
    report("2. assert_raises", test_assert_raises, assert_raises)


# --- Exercise 3 -------------------------------------------------------------

def check_send_welcome(send_welcome: Callable[[str, Any], None]) -> None:
    """Check a send_welcome(email, mailer) function using a Mock mailer.

    A correct send_welcome calls exactly once:
        mailer.send(to=email, subject="Welcome!")
    Create a unittest.mock.Mock() to stand in for the mailer, call
    send_welcome("ana@example.com", mock), then check what the mock
    recorded. mock.send.assert_called_once_with(...) raises AssertionError
    for a wrong count or wrong arguments, which is exactly what you want.
    """
    raise NotImplementedError


def test_check_send_welcome(impl: Callable[[Callable[..., None]], None]) -> None:
    def correct(email: str, mailer: Any) -> None:
        mailer.send(to=email, subject="Welcome!")

    def wrong_subject(email: str, mailer: Any) -> None:
        mailer.send(to=email, subject="Hello")

    def sends_twice(email: str, mailer: Any) -> None:
        mailer.send(to=email, subject="Welcome!")
        mailer.send(to=email, subject="Welcome!")

    def never_sends(email: str, mailer: Any) -> None:
        pass

    def wrong_address(email: str, mailer: Any) -> None:
        mailer.send(to="admin@example.com", subject="Welcome!")

    try:
        impl(correct)
    except AssertionError as exc:
        raise AssertionError(f"a correct send_welcome failed: {exc}") from None
    bugs = {
        "uses the wrong subject": wrong_subject,
        "sends the email twice": sends_twice,
        "never sends anything": never_sends,
        "sends to the wrong address": wrong_address,
    }
    for description, buggy in bugs.items():
        try:
            impl(buggy)
        except AssertionError:
            continue
        raise AssertionError(f"your check missed a send_welcome that {description}")


def check_check_send_welcome() -> None:
    report("3. check_send_welcome", test_check_send_welcome, check_send_welcome)


# --- Exercise 4 -------------------------------------------------------------

def greeting() -> str:
    """Given, complete: a function that depends on the real clock."""
    hour = time.localtime().tm_hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def greeting_at(hour: int) -> str:
    """Return what greeting() says when the clock shows `hour` o'clock.

    Do not change greeting(). Instead, use unittest.mock.patch as a with
    block to replace time.localtime while you call it:
        with patch("time.localtime") as fake:
            fake.return_value.tm_hour = hour
            ...
    The patch is undone when the block ends, even if something raises.

    >>> greeting_at(9)
    'Good morning'
    """
    raise NotImplementedError


def test_greeting_at(impl: Callable[[int], str]) -> None:
    real_localtime = time.localtime
    cases = [(9, "Good morning"), (0, "Good morning"), (12, "Good afternoon"),
             (17, "Good afternoon"), (18, "Good evening"), (23, "Good evening")]
    for hour, expected in cases:
        got = impl(hour)
        assert got == expected, (
            f"greeting_at({hour}) should be {expected!r}, got {got!r}"
        )
    assert time.localtime is real_localtime, "undo the patch when you are done"


def check_greeting_at() -> None:
    report("4. greeting_at", test_greeting_at, greeting_at)


# --- Exercise 5 -------------------------------------------------------------

class Stack:
    """Given, complete: the stack that StackTests below should test."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)


class StackTests(unittest.TestCase):
    """Write test_... methods for Stack until every bug below is caught.

    Get a fresh stack with self.make_stack(), never Stack() directly: the
    checker runs your tests against the real Stack and against buggy
    copies, and make_stack is how it swaps them in. The bugs to catch:
      - pop returns the oldest item instead of the newest
      - peek removes the item it shows
      - len() does not go down after a pop
      - pop on an empty stack returns None instead of raising IndexError
    Useful: self.assertEqual(a, b), and `with self.assertRaises(IndexError):`.
    Replace the stub method below with as many tests as you need.
    """

    def make_stack(self) -> Stack:
        return Stack()

    def test_push_then_pop(self) -> None:
        raise NotImplementedError


def test_stack_tests(impl: type) -> None:
    class OldestFirst(Stack):
        def pop(self) -> Any:
            if not self._items:
                raise IndexError("pop from an empty stack")
            return self._items.pop(0)

    class PeekRemoves(Stack):
        def peek(self) -> Any:
            return self.pop()

    class LenCountsPushes(Stack):
        def __init__(self) -> None:
            super().__init__()
            self.pushes = 0

        def push(self, item: Any) -> None:
            super().push(item)
            self.pushes += 1

        def __len__(self) -> int:
            return self.pushes

    class SilentEmptyPop(Stack):
        def pop(self) -> Any:
            return self._items.pop() if self._items else None

    def run_with(stack_class: type) -> unittest.TestResult:
        # Subclass the learner's TestCase so make_stack builds `stack_class`.
        case = type("Checked", (impl,), {"make_stack": lambda self: stack_class()})
        result = unittest.TestResult()
        unittest.defaultTestLoader.loadTestsFromTestCase(case).run(result)
        return result

    result = run_with(Stack)
    problems = result.errors + result.failures
    if any("NotImplementedError" in trace for _, trace in problems):
        raise NotImplementedError
    assert result.testsRun > 0, "write at least one test_... method"
    if problems:
        last_line = problems[0][1].strip().splitlines()[-1]
        raise AssertionError(f"a test fails on the correct Stack: {last_line}")
    bugs = {
        "pop returns the oldest item": OldestFirst,
        "peek removes the item": PeekRemoves,
        "len() ignores pops": LenCountsPushes,
        "pop on empty returns None": SilentEmptyPop,
    }
    for description, buggy in bugs.items():
        assert not run_with(buggy).wasSuccessful(), (
            f"no test caught the bug: {description}"
        )


def check_stack_tests() -> None:
    report("5. StackTests", test_stack_tests, StackTests)


def main() -> None:
    check_check_is_leap()
    check_assert_raises()
    check_check_send_welcome()
    check_greeting_at()
    check_stack_tests()


if __name__ == "__main__":
    main()
