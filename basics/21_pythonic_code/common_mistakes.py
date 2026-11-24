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


def main() -> None:
    late_binding_demo()


if __name__ == "__main__":
    main()
