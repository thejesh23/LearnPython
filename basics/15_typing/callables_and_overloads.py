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

import functools
import inspect
from collections.abc import Callable
from typing import Concatenate
from typing import get_overloads
from typing import overload


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


def logged[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    # **P captures fn's whole parameter list; R captures its return type.
    # The result has exactly the same signature, so the checker still knows
    # area(width=2, height=3) is valid and returns a float. Typing this as
    # Callable[..., Any] would compile too, but every check would be lost.
    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"  calling {fn.__name__} with {args} {kwargs}")
        return fn(*args, **kwargs)

    return wrapper


@logged
def area(width: float, height: float) -> float:
    return width * height


def with_request_id[**P, R](fn: Callable[Concatenate[str, P], R]) -> Callable[P, R]:
    # Concatenate[str, P] is "a str first, then P". The decorator supplies the
    # str itself, so callers of the result pass only the P part.
    counter = 0

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        nonlocal counter
        counter += 1
        return fn(f"req-{counter}", *args, **kwargs)

    return wrapper


@with_request_id
def handle(request_id: str, path: str) -> str:
    return f"[{request_id}] GET {path}"


def paramspec_demo() -> None:
    print(f"area(width=2, height=3) = {area(width=2, height=3)}")
    # functools.wraps copies the name and lets inspect see the real signature.
    print(f"area.__name__ = {area.__name__!r}, signature {inspect.signature(area)}")
    print(handle("/home"))
    print(handle("/about"))


@overload
def parse_number(text: str) -> int: ...
@overload
def parse_number(text: list[str]) -> list[int]: ...
def parse_number(text: str | list[str]) -> int | list[int]:
    # The @overload stubs above are for the checker: they say a str gives an
    # int and a list gives a list. Without them the only hint would be
    # "int | list[int]", and every caller would have to check which it got.
    # Only this last, undecorated definition actually runs.
    if isinstance(text, str):
        return int(text)
    return [int(item) for item in text]


def overload_demo() -> None:
    single = parse_number("42")  # checker: int
    many = parse_number(["1", "2", "3"])  # checker: list[int]
    print(f"parse_number('42') = {single!r}, so single + 1 = {single + 1}")
    print(f"parse_number(['1', '2', '3']) = {many!r}, sum = {sum(many)}")

    # Since Python 3.11 the registered overloads can be listed at runtime.
    for stub in get_overloads(parse_number):
        print(f"  overload: {inspect.signature(stub)}")


def main() -> None:
    callable_demo()
    print()
    paramspec_demo()
    print()
    overload_demo()


if __name__ == "__main__":
    main()
