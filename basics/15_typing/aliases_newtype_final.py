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


def main() -> None:
    type_statement_demo()


if __name__ == "__main__":
    main()
