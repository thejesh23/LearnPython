"""Naming and pinning down types: `type`, `NewType`, `Final`, `ClassVar`, `Self`.

    type Point = ...     a named alias for a longer type (Python 3.12+)
    NewType              a *distinct* type built on an existing one, so a UserId
                         cannot be passed where an OrderId is expected
    Final / @final       "never reassign this" / "never override or subclass this"
    ClassVar             an attribute that belongs to the class, not each instance
    Self                 "an instance of whatever class this method was called on"

These change nothing about how the program runs. They let a type checker catch
mix-ups that would otherwise only show up as wrong answers.
"""

from dataclasses import dataclass
from dataclasses import fields
from typing import ClassVar
from typing import Final
from typing import NewType
from typing import Self
from typing import final


type Point = tuple[float, float]
type Pair[T] = tuple[T, T]  # aliases can be generic too

# The value is evaluated lazily, so an alias may refer to itself. This one
# describes any JSON value, however deeply nested.
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None


def midpoint(a: Point, b: Point) -> Point:
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def swap[T](pair: Pair[T]) -> Pair[T]:
    return (pair[1], pair[0])


def depth(value: JSON) -> int:
    if isinstance(value, dict):
        return 1 + max((depth(v) for v in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((depth(v) for v in value), default=0)
    return 0


def type_statement_demo() -> None:
    print(f"midpoint((0, 0), (4, 2)) = {midpoint((0, 0), (4, 2))}")
    print(f"swap(('a', 'b')) = {swap(('a', 'b'))}")
    print(f"depth of nested JSON = {depth({'a': [1, {'b': [2]}]})}")

    # Unlike a plain `Point = tuple[...]` assignment, the alias is its own
    # object, with a name and the aliased type available as __value__.
    print(f"type(Point) is {type(Point).__name__}, Point.__value__ = {Point.__value__}")


UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)


def cancel_order(order_id: OrderId) -> str:
    return f"cancelled order {order_id}"


def newtype_demo() -> None:
    user = UserId(7)
    order = OrderId(1042)
    print(cancel_order(order))

    # Both are ints underneath, so this runs and does the wrong thing.
    # mypy reports it: 'Argument 1 has incompatible type "UserId"'.
    print(f"{cancel_order(user)}   <- a bug a type checker would catch")

    # NewType costs nothing at runtime: UserId(7) simply returns the int 7.
    print(f"type(user) is int: {type(user) is int}, user + 1 = {user + 1}")


MAX_RETRIES: Final = 3  # a constant; reassigning it is a checker error


@dataclass
class Download:
    url: str
    retries: int = MAX_RETRIES
    # ClassVar marks a class-level attribute. The dataclass leaves it out of
    # __init__ and repr, because it is shared by every Download.
    started: ClassVar[int] = 0

    def __post_init__(self) -> None:
        Download.started += 1


@final
class Settings:
    """@final: the checker reports any attempt to subclass this."""

    TIMEOUT: Final[float] = 2.5


def final_and_classvar_demo() -> None:
    a = Download("https://example.com/a")
    b = Download("https://example.com/b", retries=1)
    print(a)
    print(b)
    print(f"Download.started = {Download.started}")
    print(f"dataclass fields: {[f.name for f in fields(Download)]}")

    # Final is a promise, not a lock: Python itself still allows this.
    Settings.TIMEOUT = 10.0  # type: ignore[misc]
    print(f"Settings.TIMEOUT after reassigning = {Settings.TIMEOUT}")
    print(f"@final sets a marker: Settings.__final__ = {Settings.__final__}")


class QueryBuilder:
    def __init__(self) -> None:
        self.parts: list[str] = []

    def where(self, condition: str) -> Self:
        # Returning Self (not "QueryBuilder") means a subclass calling this
        # gets its own type back, so chained calls keep the subclass methods.
        self.parts.append(f"WHERE {condition}")
        return self

    @classmethod
    def from_table(cls, table: str) -> Self:
        query = cls()
        query.parts.append(f"FROM {table}")
        return query


class PagedQuery(QueryBuilder):
    def page(self, number: int, size: int = 20) -> Self:
        self.parts.append(f"LIMIT {size} OFFSET {(number - 1) * size}")
        return self


def self_demo() -> None:
    # from_table and where are inherited, yet the checker knows the result is
    # a PagedQuery, so .page() is allowed at the end of the chain.
    query = PagedQuery.from_table("users").where("active").page(3)
    print(f"{type(query).__name__}: {' '.join(query.parts)}")


def main() -> None:
    type_statement_demo()
    print()
    newtype_demo()
    print()
    final_and_classvar_demo()
    print()
    self_demo()


if __name__ == "__main__":
    main()
