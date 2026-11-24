"""Recursion: a function that solves a problem by calling itself on a smaller piece.

Every recursive function needs two parts:

    base case       a version of the problem small enough to answer directly
    recursive step  shrink the problem, call yourself, build on the answer

Forget the base case, or fail to shrink, and the calls never stop.

Each call gets its own frame on the *call stack*, holding its own local
variables. Python caps how deep that stack may grow (about 1000 frames by
default) and raises RecursionError beyond it. So in Python a plain loop is
usually the better choice for long, straight-line work, and recursion shines
on tree-shaped data: folders inside folders, nested lists, menus, expressions.

When a recursive function recomputes the same inputs again and again, a cache
fixes it; see functools.cache in basics/13_standard_library/functools_tools.py.
recursion/recursion_limits_and_tail_calls.py goes deeper into the limit.
"""


def factorial(n: int) -> int:
    """n! = n * (n-1) * ... * 1."""
    if n <= 1:  # base case: answer directly, no further calls
        return 1
    return n * factorial(n - 1)  # recursive step: a smaller problem


def sum_digits(n: int) -> int:
    """Add up the digits of a non-negative integer."""
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


def base_case_demo() -> None:
    print(f"factorial(5) = {factorial(5)}")
    print(f"factorial(0) = {factorial(0)}")
    print(f"sum_digits(2024) = {sum_digits(2024)}")


def main() -> None:
    base_case_demo()


if __name__ == "__main__":
    main()
