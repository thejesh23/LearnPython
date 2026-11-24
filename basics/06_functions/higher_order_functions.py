"""Higher-order functions: functions that take or return other functions.

In Python a function is a value like any other. `len` without parentheses is
the function object itself; `len(x)` is a call. That means you can store a
function in a variable, list or dict, hand it to another function as an
argument, and build new functions inside a function and return them.

A function that accepts or returns a function is called *higher-order*. You
already use some: `sorted(words, key=len)` hands `len` to `sorted`, which calls
it once per item.

Related files: lambdas.py (one-line anonymous functions), closures_and_scope.py
(how returned functions remember variables) and decorators.py (the @ syntax
for wrapping a function).
"""

from collections.abc import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


# A dispatch table: look the operation up by name instead of a long if/elif.
OPERATIONS = {"+": add, "-": subtract, "*": multiply}


def calculate(a: float, symbol: str, b: float) -> float:
    return OPERATIONS[symbol](a, b)


def functions_as_values_demo() -> None:
    # Without parentheses, `add` is the function object; nothing is called.
    print(f"callable(add) = {callable(add)}")
    print(f"callable(add(1, 2)) = {callable(add(1, 2))}   (that is the int 3)")
    print(f"type(add) = {type(add).__name__}, name = {add.__name__}")

    plus = add  # a second name for the same function object, not a call
    print(f"plus(2, 3) = {plus(2, 3)}, plus is add -> {plus is add}")

    for expression in [(6, "+", 2), (6, "-", 2), (6, "*", 2)]:
        print(f"{expression} -> {calculate(*expression)}")


def apply_to_all(func: Callable[[int], int], values: list[int]) -> list[int]:
    """Call func on every value. The caller decides *what* happens to each."""
    return [func(v) for v in values]


def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


def double(n: int) -> int:
    return n * 2


def square(n: int) -> int:
    return n * n


def passing_functions_demo() -> None:
    nums = [1, 2, 3, 4]
    # Pass the function itself: `double`, not `double()`.
    print(f"apply_to_all(double) -> {apply_to_all(double, nums)}")
    print(f"apply_to_all(square) -> {apply_to_all(square, nums)}")
    print(f"apply_twice(double, 5) = {apply_twice(double, 5)}")
    print(f"apply_twice(square, 3) = {apply_twice(square, 3)}")

    # A common slip: calling the function while passing it.
    try:
        apply_twice(double(5), 1)  # type: ignore[arg-type]
    except TypeError as exc:
        print(f"passed double(5) by mistake -> TypeError: {exc}")


def main() -> None:
    functions_as_values_demo()
    print()
    passing_functions_demo()


if __name__ == "__main__":
    main()
