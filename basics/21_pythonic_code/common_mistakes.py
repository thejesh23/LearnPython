"""Common Python mistakes — each one shown failing, then fixed.

These are the bugs that bite almost everyone once. None of them raise an
error at the moment you make the mistake; the program just quietly does the
wrong thing, which is what makes them worth learning by sight:

    late-binding closures     lambdas made in a loop all see the LAST value
    editing a list in a loop  items get skipped
    `is` for values           works in tests, fails in production
    shadowing built-ins       `list = ...` breaks list() later
    / versus //               a float where you needed an int, or vice versa
    mutable class attributes  one list shared by every instance

The mutable *default argument* trap (`def f(items=[])`) is the cousin of the
last one; it has its own file, basics/06_functions/default_arguments.py.
"""

from functools import partial


def late_binding_demo() -> None:
    # A closure remembers the VARIABLE, not its value at creation time. By
    # the time the lambdas run, the loop is over and i is 2 for all of them.
    buggy = [lambda: i for i in range(3)]
    print(f"buggy : {[f() for f in buggy]}")

    # Fix 1: a default argument is evaluated when the lambda is created.
    fixed = [lambda i=i: i for i in range(3)]
    print(f"fixed : {[f() for f in fixed]}")

    # Fix 2: partial() binds the current value explicitly.
    def show(n: int) -> int:
        return n

    bound = [partial(show, i) for i in range(3)]
    print(f"partial: {[f() for f in bound]}")


def mutating_while_iterating_demo() -> None:
    numbers = [2, 4, 5, 6, 8]
    for n in numbers:
        if n % 2 == 0:
            numbers.remove(n)  # shifts later items left; the loop skips one
    print(f"remove evens in-loop: {numbers}   <- 4 and 8 survived")

    # Fix: build a new list (or loop over a copy: `for n in numbers[:]`).
    numbers = [2, 4, 5, 6, 8]
    odds = [n for n in numbers if n % 2 != 0]
    print(f"comprehension       : {odds}")

    # Dicts and sets refuse outright, which is kinder.
    ages = {"ana": 30, "ben": 17}
    try:
        for name in ages:
            if ages[name] < 18:
                del ages[name]
    except RuntimeError as exc:
        print(f"dict: RuntimeError: {exc}")
    adults = {name: age for name, age in ages.items() if age >= 18}
    print(f"dict comprehension  : {adults}")


def main() -> None:
    late_binding_demo()
    print()
    mutating_while_iterating_demo()


if __name__ == "__main__":
    main()
