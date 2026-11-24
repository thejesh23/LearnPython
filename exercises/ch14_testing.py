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


def main() -> None:
    check_check_is_leap()


if __name__ == "__main__":
    main()
