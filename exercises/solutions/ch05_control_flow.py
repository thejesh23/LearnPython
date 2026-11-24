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


def sum_of_multiples(limit: int) -> int:
    # range(limit) stops just below limit; `continue` skips the rest.
    total = 0
    for n in range(limit):
        if n % 3 != 0 and n % 5 != 0:
            continue
        total += n
    return total


def check_sum_of_multiples() -> None:
    report("2. sum_of_multiples", EXERCISES["test_sum_of_multiples"],
           sum_of_multiples)


def first_index(items: list[Any] | str, target: Any) -> int:
    # Return from inside the loop at the first match; reaching the end of
    # the loop means there was none.
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def check_first_index() -> None:
    report("3. first_index", EXERCISES["test_first_index"], first_index)


def collatz_steps(n: int) -> int:
    # The number of steps is not known up front, so this is a while loop.
    # Every pass changes n, which is what eventually ends the loop.
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def check_collatz_steps() -> None:
    report("4. collatz_steps", EXERCISES["test_collatz_steps"], collatz_steps)


def main() -> None:
    check_fizzbuzz()
    check_sum_of_multiples()
    check_first_index()
    check_collatz_steps()


if __name__ == "__main__":
    main()
