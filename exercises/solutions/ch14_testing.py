"""Solutions: testing (chapter 14).

Worked answers for exercises/ch14_testing.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch14_testing.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import Mock
from unittest.mock import patch


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch14_testing.py")
)
report = EXERCISES["report"]


def check_is_leap(is_leap: Callable[[int], bool]) -> None:
    # One year per branch of the rule, plus a plain non-leap year.
    assert is_leap(2024), "2024 divides by 4: leap"
    assert not is_leap(2023), "2023 does not divide by 4: not leap"
    assert not is_leap(1900), "1900 divides by 100 but not 400: not leap"
    assert is_leap(2000), "2000 divides by 400: leap"
    assert not is_leap(2022), "2022 is even but not divisible by 4: not leap"


def check_check_is_leap() -> None:
    report("1. check_is_leap", EXERCISES["test_check_is_leap"], check_is_leap)


def assert_raises(
    exc_type: type[BaseException], func: Callable[..., Any], *args: Any
) -> BaseException:
    try:
        func(*args)
    except exc_type as exc:  # other exception types are not caught here
        return exc
    # Only reached when func returned normally.
    raise AssertionError(f"{func.__name__} did not raise {exc_type.__name__}")


def check_assert_raises() -> None:
    report("2. assert_raises", EXERCISES["test_assert_raises"], assert_raises)


def check_send_welcome(send_welcome: Callable[[str, Any], None]) -> None:
    mailer = Mock()  # accepts any call and records it
    send_welcome("ana@example.com", mailer)
    # Checks the call count (exactly one) and the exact arguments together.
    mailer.send.assert_called_once_with(to="ana@example.com", subject="Welcome!")


def check_check_send_welcome() -> None:
    report("3. check_send_welcome", EXERCISES["test_check_send_welcome"],
           check_send_welcome)


# The function under test is the one given in the exercise file.
greeting = EXERCISES["greeting"]


def greeting_at(hour: int) -> str:
    # Patch the name where it is looked up: greeting() calls time.localtime.
    with patch("time.localtime") as fake:
        fake.return_value.tm_hour = hour
        return greeting()


def check_greeting_at() -> None:
    report("4. greeting_at", EXERCISES["test_greeting_at"], greeting_at)


Stack = EXERCISES["Stack"]


class StackTests(unittest.TestCase):
    def make_stack(self) -> Stack:
        return Stack()

    # One small test per behaviour, so a failure names the broken behaviour.
    def test_pop_returns_newest(self) -> None:
        stack = self.make_stack()
        stack.push(1)
        stack.push(2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)

    def test_peek_does_not_remove(self) -> None:
        stack = self.make_stack()
        stack.push("a")
        self.assertEqual(stack.peek(), "a")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack.pop(), "a")

    def test_len_follows_push_and_pop(self) -> None:
        stack = self.make_stack()
        self.assertEqual(len(stack), 0)
        stack.push(1)
        stack.push(2)
        stack.pop()
        self.assertEqual(len(stack), 1)

    def test_pop_empty_raises(self) -> None:
        stack = self.make_stack()
        with self.assertRaises(IndexError):
            stack.pop()


def check_stack_tests() -> None:
    report("5. StackTests", EXERCISES["test_stack_tests"], StackTests)


def main() -> None:
    check_check_is_leap()
    check_assert_raises()
    check_check_send_welcome()
    check_greeting_at()
    check_stack_tests()


if __name__ == "__main__":
    main()
