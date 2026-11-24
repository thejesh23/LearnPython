"""Practice exercises for basics/05_control_flow: branches and loops.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch05_control_flow.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

If a run seems to hang, a while loop is probably never reaching its exit
condition: press Ctrl+C and check that the loop changes what it tests.
Nothing here needs more than basics/00 to basics/05 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch05_control_flow.py. Try each exercise yourself first.
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


def fizzbuzz(n: int) -> str:
    """Return "Fizz" for multiples of 3, "Buzz" for multiples of 5,
    "FizzBuzz" for multiples of both, and otherwise the number as text.

    fizzbuzz(9)  -> "Fizz"
    fizzbuzz(10) -> "Buzz"
    fizzbuzz(15) -> "FizzBuzz"
    fizzbuzz(7)  -> "7"

    Hint: the order of the branches matters.
    """
    raise NotImplementedError


def test_fizzbuzz(fn: Callable[..., Any]) -> None:
    cases = [
        (1, "1"),
        (3, "Fizz"),
        (5, "Buzz"),
        (7, "7"),
        (9, "Fizz"),
        (10, "Buzz"),
        (15, "FizzBuzz"),
        (30, "FizzBuzz"),
    ]
    for n, want in cases:
        got = fn(n)
        assert got == want, f"fizzbuzz({n}) returned {got!r}, expected {want!r}"


def check_fizzbuzz() -> None:
    report("1. fizzbuzz", test_fizzbuzz, fizzbuzz)


def main() -> None:
    check_fizzbuzz()


if __name__ == "__main__":
    main()
