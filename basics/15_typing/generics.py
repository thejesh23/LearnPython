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


def main() -> None:
    function_demo()


if __name__ == "__main__":
    main()
