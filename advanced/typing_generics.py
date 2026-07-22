"""Generics and the modern typing syntax (3.12 `type` parameters).

Python 3.12 lets you write type parameters inline — `def first[T](...)` and
`class Stack[T]` — with no TypeVar import and no `Generic[T]` base.

Concepts that pay off in review:
    TypeVar bound     restrict what T can be
    Protocol          structural typing, checked statically
    overload          different signatures for the same function
    TypedDict         a dict with a known key/value shape
    Self              a method returning "the same class as self"
    NewType           a distinct type at check time, an alias at runtime
"""

from typing import NewType, Protocol, Self, TypedDict, overload


class Comparable(Protocol):
    def __lt__(self, other, /) -> bool: ...


def largest[T: Comparable](items: list[T]) -> T:
    """A bounded type parameter: T must support <."""
    best = items[0]
    for item in items[1:]:
        if best < item:
            best = item
    return best


class Stack[T]:
    """A generic container — no Generic[T] base needed in 3.12."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> Self:  # Self keeps chaining type-correct
        self._items.append(item)
        return self

    def pop(self) -> T:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


type Pair[T] = tuple[T, T]  # a generic type alias (3.12)


class UserRecord(TypedDict):
    name: str
    age: int
    email: str


UserId = NewType("UserId", int)  # distinct to a checker, a plain int at runtime


@overload
def double(value: int) -> int: ...
@overload
def double(value: str) -> str: ...
def double(value: int | str) -> int | str:
    return value * 2


def send_invite(user_id: UserId) -> str:
    return f"invited #{user_id}"


def main() -> None:
    print(f"largest ints    = {largest([3, 9, 2])}")
    print(f"largest strings = {largest(['pear', 'apple', 'fig'])}")

    stack: Stack[int] = Stack()
    stack.push(1).push(2).push(3)
    print(f"stack len = {len(stack)}, pop = {stack.pop()}")

    coords: Pair[float] = (1.5, 2.5)
    print(f"pair alias = {coords}")

    user: UserRecord = {"name": "Ada", "age": 36, "email": "ada@example.com"}
    print(f"typed dict is a plain dict at runtime: {type(user).__name__}, {user['name']}")

    print(f"double(21) = {double(21)}, double('ab') = {double('ab')}")
    print(f"NewType: {send_invite(UserId(7))}, runtime type is {type(UserId(7)).__name__}")

    print(f"generic parameters of Stack: {Stack.__type_params__}")


if __name__ == "__main__":
    main()
