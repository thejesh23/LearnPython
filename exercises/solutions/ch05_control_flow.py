"""Worked solutions for exercises/ch05_control_flow.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from pathlib import Path
from typing import Any


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch05_control_flow.py")
)
report = EXERCISES["report"]


def fizzbuzz(n: int) -> str:
    # The most specific case goes first: a multiple of 15 is also a
    # multiple of 3, so testing 3 first would never reach "FizzBuzz".
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def check_fizzbuzz() -> None:
    report("1. fizzbuzz", EXERCISES["test_fizzbuzz"], fizzbuzz)


def main() -> None:
    check_fizzbuzz()


if __name__ == "__main__":
    main()
