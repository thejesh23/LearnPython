"""Typing callables: `Callable`, `ParamSpec` for decorators, and `@overload`.

How to describe functions that take or return other functions, and functions
whose return type depends on what you pass in.

    Callable[[int, str], bool]   "a function taking (int, str), returning bool"
    Callable[..., bool]          any arguments at all, returning bool
    ParamSpec  (**P)             "the same parameters as some other function",
                                 the key to typing decorators properly
    Concatenate[str, P]          P with an extra first argument in front
    @overload                    list the precise signatures a function has,
                                 when the return type depends on the arguments

Everything here is for the type checker and your editor. The runtime behaviour
is plain Python: the decorators still run, the overloads are never called.
"""

from collections.abc import Callable


BinaryOp = Callable[[float, float], float]  # an alias keeps hints short

OPERATIONS: dict[str, BinaryOp] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "max": max,  # any callable with a matching shape fits, built-ins too
}


def make_multiplier(factor: int) -> Callable[[int], int]:
    # Returning a function: the hint says what the caller gets back can be
    # called with one int and returns an int.
    def multiply(n: int) -> int:
        return n * factor

    return multiply


def run_later(callback: Callable[..., str], *args: object) -> str:
    # Callable[..., str] accepts any parameters. It is the loose option, used
    # when the arguments really do vary. Prefer the precise form when you can.
    return callback(*args)


def callable_demo() -> None:
    for symbol, op in OPERATIONS.items():
        print(f"7 {symbol} 3 = {op(7, 3)}")
    triple = make_multiplier(3)
    print(f"triple(14) = {triple(14)}")
    print(f"run_later(str.upper, 'hi') = {run_later(str.upper, 'hi')!r}")
    print(f"callable(triple) = {callable(triple)}, callable(3) = {callable(3)}")


def main() -> None:
    callable_demo()


if __name__ == "__main__":
    main()
