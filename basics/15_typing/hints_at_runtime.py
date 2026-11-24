"""What happens to type hints when the program actually runs.

Short answer: almost nothing. Python stores the hints on the function or class
and then ignores them. A function hinted `(n: int) -> int` will accept a string
without complaint. The checking is done *before* running, by a separate tool:

    mypy file.py        (pip install mypy)
    pyright file.py     (pip install pyright, also built into VS Code's Pylance)

This file looks at the runtime side:
    __annotations__     the raw hints, possibly still strings
    get_type_hints()    the hints resolved into real objects
    TYPE_CHECKING       a flag that is False at runtime and True for checkers,
                        for imports only the checker needs
    a small decorator   that uses the hints to check arguments at runtime
"""

import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING
from typing import get_type_hints


def double(n: int) -> int:
    return n * 2


def not_enforced_demo() -> None:
    print(f"double(4) = {double(4)}")
    # Wrong type, no error: "ab" * 2 is valid Python, so it just runs.
    print(f"double('ab') = {double('ab')!r}   (a checker would flag this call)")
    print(f"double.__annotations__ = {double.__annotations__}")


@dataclass
class Node:
    value: int
    # Node is not defined yet while its own body runs, so the hint has to be
    # written as a string: a "forward reference".
    next: "Node | None" = None


# Node exists by now; the quotes here are only to show what happens to them.
def last(node: "Node") -> "Node":
    while node.next is not None:
        node = node.next
    return node


def get_type_hints_demo() -> None:
    chain = Node(1, Node(2, Node(3)))
    print(f"last(chain).value = {last(chain).value}")

    # __annotations__ keeps the strings exactly as written...
    print(f"last.__annotations__ = {last.__annotations__}")
    # ...get_type_hints evaluates them into the real classes.
    print(f"get_type_hints(last) = {get_type_hints(last)}")
    print(f"get_type_hints(Node) = {get_type_hints(Node)}")


if TYPE_CHECKING:
    # This block never runs, so the import costs nothing at runtime. Use it
    # for imports needed only in hints: heavy modules, or ones that would
    # cause a circular import. Hints that use them must then be strings.
    from decimal import Decimal


def format_price(amount: "Decimal") -> str:
    return f"${amount:.2f}"


def type_checking_demo() -> None:
    print(f"TYPE_CHECKING at runtime = {TYPE_CHECKING}")
    print(f"format_price(3.5) = {format_price(3.5)}  (a float works at runtime)")

    # The trade-off: the name really is missing at runtime, so anything that
    # resolves the hints, like get_type_hints, fails.
    try:
        get_type_hints(format_price)
    except NameError as exc:
        print(f"get_type_hints(format_price) -> NameError: {exc}")


def checked[R](fn: Callable[..., R]) -> Callable[..., R]:
    """Raise TypeError when an argument does not match a plain-class hint."""
    hints = get_type_hints(fn)
    signature = inspect.signature(fn)

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        # bind() matches the call's arguments to parameter names, exactly as
        # Python would, so positional and keyword calls are handled alike.
        bound = signature.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            expected = hints.get(name)
            # Only check simple classes. Hints like list[int] or int | None
            # need much more work, which is what real libraries do.
            if isinstance(expected, type) and not isinstance(value, expected):
                raise TypeError(f"{name}={value!r} is not {expected.__name__}")
        return fn(*args, **kwargs)

    return wrapper


@checked
def repeat(word: str, times: int) -> str:
    return " ".join([word] * times)


def validator_demo() -> None:
    print(f"repeat('hey', 3) = {repeat('hey', 3)!r}")
    print(f"repeat(word='ok', times=2) = {repeat(word='ok', times=2)!r}")
    for args in [("hey", "3"), (3, 3)]:
        try:
            repeat(*args)
        except TypeError as exc:
            print(f"repeat{args} -> TypeError: {exc}")
    # Checking every call like this costs time. Most projects rely on mypy or
    # pyright before running instead, and check only data from outside (user
    # input, JSON, files) at runtime.


def main() -> None:
    not_enforced_demo()
    print()
    get_type_hints_demo()
    print()
    type_checking_demo()
    print()
    validator_demo()


if __name__ == "__main__":
    main()
