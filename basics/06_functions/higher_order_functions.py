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


def main() -> None:
    functions_as_values_demo()


if __name__ == "__main__":
    main()
