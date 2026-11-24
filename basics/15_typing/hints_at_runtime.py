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

from dataclasses import dataclass
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


def main() -> None:
    not_enforced_demo()
    print()
    get_type_hints_demo()
    print()
    type_checking_demo()


if __name__ == "__main__":
    main()
