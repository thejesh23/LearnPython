"""Generics — code that works for many types without forgetting which type it got.

Suppose `first(items)` returns the first item of a list. Hinting it as
`list[Any] -> Any` is honest but useless: after `first([1, 2])` the checker no
longer knows the result is an int. A *type parameter* fixes that. Write
`def first[T](items: list[T]) -> T` and the checker reads it as "whatever type
went in, that same type comes out".

Python 3.12 added the square-bracket syntax used here:
    def first[T](...)        a generic function
    class Box[T]: ...        a generic class
    [T: Sized]               a bound: T must be Sized (or a subtype)
    [S: (str, bytes)]        constraints: S is exactly str or exactly bytes

Older code spells the same thing with `T = TypeVar("T")` and `Generic[T]`; you
will see both. Like every hint, type parameters are checked by tools such as
mypy, not by Python when the code runs.
"""

from collections.abc import Callable
from collections.abc import Sequence


def first[T](items: Sequence[T]) -> T:
    # T is a placeholder filled in at each call site. For first([3, 4]) the
    # checker infers T = int, so it knows the result is an int too.
    return items[0]


def pair_up[K, V](keys: Sequence[K], values: Sequence[V]) -> dict[K, V]:
    # Several type parameters can travel together.
    return dict(zip(keys, values))


def function_demo() -> None:
    print(f"first([3, 4]) = {first([3, 4])!r}")
    print(f"first('hey') = {first('hey')!r}")
    print(f"pair_up = {pair_up(['a', 'b'], [1, 2])}")

    # The parameters are real objects you can inspect at runtime.
    print(f"first.__type_params__ = {first.__type_params__}")
    print(f"pair_up.__type_params__ = {pair_up.__type_params__}")
    # At runtime nothing is enforced: T is a promise to the type checker.


class Box[T]:
    """Holds one value of type T. Box[int] holds an int, Box[str] a str."""

    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

    def map[U](self, fn: Callable[[T], U]) -> "Box[U]":
        # A method can add its own parameter: mapping a Box[int] with str()
        # gives a Box[str], and the checker follows the change of type.
        return Box(fn(self.value))

    def __repr__(self) -> str:
        return f"Box({self.value!r})"


class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


def class_demo() -> None:
    number = Box(21)  # the checker infers Box[int]
    text = number.map(lambda n: f"{n * 2} apples")  # Box[str]
    print(f"{number} -> {text}, text.get().upper() = {text.get().upper()!r}")

    # You can also spell the type out. Box[int] is a "generic alias".
    explicit: Box[int] = Box[int](5)
    print(f"Box[int](5) = {explicit}, Box[int] is {Box[int]!r}")

    tasks = Stack[str]()
    tasks.push("write tests")
    tasks.push("fix bug")
    print(f"popped {tasks.pop()!r}, then {tasks.pop()!r}")
    # tasks.push(42) would still run; mypy would report "expected str".


def main() -> None:
    function_demo()
    print()
    class_demo()


if __name__ == "__main__":
    main()
