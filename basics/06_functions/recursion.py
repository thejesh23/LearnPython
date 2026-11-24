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

import sys


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


def countdown_sum(n: int, depth: int = 0) -> int:
    """Sum 1..n, printing each call on the way down and each return on the way up."""
    pad = "  " * depth
    print(f"{pad}call countdown_sum({n})")
    if n == 0:
        print(f"{pad}base case -> 0")
        return 0
    result = n + countdown_sum(n - 1, depth + 1)
    print(f"{pad}return {result}")
    return result


def call_stack_demo() -> None:
    # Every call waits, paused, until the call it made returns. The paused
    # calls stack up, then finish in reverse order.
    countdown_sum(3)


def count_down(n: int) -> int:
    """Recursive: one stack frame per step."""
    return 0 if n == 0 else 1 + count_down(n - 1)


def count_down_loop(n: int) -> int:
    """The same work as a loop: one frame, any size."""
    steps = 0
    while n > 0:
        n -= 1
        steps += 1
    return steps


def limit_demo() -> None:
    print(f"recursion limit = {sys.getrecursionlimit()}")
    print(f"count_down(500) = {count_down(500)}")
    try:
        count_down(100_000)
    except RecursionError as exc:
        print(f"count_down(100_000) -> RecursionError: {exc}")
    print(f"count_down_loop(100_000) = {count_down_loop(100_000)}")
    # sys.setrecursionlimit() can raise the cap, but each frame costs real
    # memory; for long linear work, a loop is the honest fix.


# A folder tree as nested dicts: a dict is a folder, an int is a file size.
FILES = {
    "notes.txt": 12,
    "photos": {"cat.jpg": 300, "dog.jpg": 250, "old": {"1999.jpg": 80}},
    "code": {"main.py": 4, "lib": {"util.py": 2, "math.py": 3}},
}


def total_size(folder: dict) -> int:
    """Each folder's size is its files plus the size of its sub-folders."""
    total = 0
    for item in folder.values():
        if isinstance(item, dict):
            total += total_size(item)  # same question, smaller tree
        else:
            total += item
    return total


def show_tree(folder: dict, indent: int = 0) -> None:
    for name, item in folder.items():
        if isinstance(item, dict):
            print(f"{'  ' * indent}{name}/  ({total_size(item)} KB)")
            show_tree(item, indent + 1)
        else:
            print(f"{'  ' * indent}{name}  ({item} KB)")


def tree_demo() -> None:
    # A loop would need to know how deep the nesting goes. Recursion does not:
    # each level handles itself and hands sub-folders to another call.
    show_tree(FILES)
    print(f"total = {total_size(FILES)} KB")


def main() -> None:
    base_case_demo()
    print()
    call_stack_demo()
    print()
    limit_demo()
    print()
    tree_demo()


if __name__ == "__main__":
    main()
