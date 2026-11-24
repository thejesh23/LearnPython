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
from dataclasses import dataclass
from operator import attrgetter


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


def compose(f: Callable[[int], int], g: Callable[[int], int]) -> Callable[[int], int]:
    """Return a new function that runs g, then f on the result."""

    def composed(value: int) -> int:
        return f(g(value))

    composed.__name__ = f"{f.__name__}_after_{g.__name__}"
    return composed


def make_validator(minimum: int, maximum: int) -> Callable[[int], bool]:
    """Build a checker function from settings, instead of passing them every call."""

    def is_valid(value: int) -> bool:
        return minimum <= value <= maximum

    return is_valid


def returning_functions_demo() -> None:
    square_then_double = compose(double, square)
    print(f"{square_then_double.__name__}(3) = {square_then_double(3)}")
    double_then_square = compose(square, double)
    print(f"{double_then_square.__name__}(3) = {double_then_square(3)}")

    is_percent = make_validator(0, 100)
    is_dice_roll = make_validator(1, 6)
    print(f"is_percent(42) = {is_percent(42)}, is_percent(140) = {is_percent(140)}")
    print(f"rolls valid: {[is_dice_roll(r) for r in (0, 3, 6, 7)]}")


def is_even(n: int) -> bool:
    return n % 2 == 0


def map_filter_demo() -> None:
    nums = [1, 2, 3, 4, 5, 6]

    # map and filter are higher-order built-ins. They return lazy iterators.
    doubled = map(double, nums)
    print(f"map returns {type(doubled).__name__}; list(...) -> {list(doubled)}")
    print(f"filter(is_even) -> {list(filter(is_even, nums))}")

    # The same results as comprehensions, which most Python code prefers
    # because the expression and the condition sit in one readable line.
    print(f"comprehension    -> {[double(n) for n in nums if is_even(n)]}")

    # map still reads well when the function already exists by name...
    print(f"map(int, ...)    -> {list(map(int, ['7', '8', '9']))}")
    # ...and it can walk several sequences in step.
    print(f"map(add, a, b)   -> {list(map(add, [1, 2, 3], [10, 20, 30]))}")

    # filter(None, ...) keeps only the truthy items.
    print(f"filter(None)     -> {list(filter(None, ['a', '', 'b', None, 'c']))}")


@dataclass
class Book:
    title: str
    year: int
    pages: int


BOOKS = [
    Book("Dune", 1965, 412),
    Book("Neuromancer", 1984, 271),
    Book("Hyperion", 1989, 482),
    Book("Foundation", 1951, 255),
]


def reading_hours(book: Book) -> float:
    """A named key function: easier to test and reuse than an inline lambda."""
    return book.pages / 40


def key_functions_demo() -> None:
    # sorted, min and max call the key once per item and compare the results.
    print(f"oldest:   {min(BOOKS, key=attrgetter('year')).title}")
    print(f"longest:  {max(BOOKS, key=attrgetter('pages')).title}")
    by_time = sorted(BOOKS, key=reading_hours)
    print(f"quickest reads: {[b.title for b in by_time]}")

    # Any one-argument function works as a key, including built-ins.
    titles = ["dune", "Neuromancer", "hyperion", "Foundation"]
    print(f"plain sort:       {sorted(titles)}")
    print(f"key=str.lower:    {sorted(titles, key=str.lower)}")
    print(f"key=len:          {sorted(titles, key=len)}")


def main() -> None:
    functions_as_values_demo()
    print()
    passing_functions_demo()
    print()
    returning_functions_demo()
    print()
    map_filter_demo()
    print()
    key_functions_demo()


if __name__ == "__main__":
    main()
