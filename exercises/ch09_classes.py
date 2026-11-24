"""Practice: classes (chapter 09).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch09_classes.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch09_classes.py: try first, peek second. The lessons
for this chapter are in basics/09_classes/.
"""

from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

class Rectangle:
    """A rectangle that knows its own area and perimeter.

    Store width and height as attributes and add three methods:
        area()        width * height
        perimeter()   2 * (width + height)
        is_square()   True when width equals height

    >>> r = Rectangle(3, 4)
    >>> r.width, r.height, r.area(), r.perimeter(), r.is_square()
    (3, 4, 12, 14, False)
    """

    def __init__(self, width: float, height: float) -> None:
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

    def is_square(self) -> bool:
        raise NotImplementedError


def test_rectangle(impl: type) -> None:
    r = impl(3, 4)
    assert (r.width, r.height) == (3, 4), "store width and height as attributes"
    assert r.area() == 12, f"Rectangle(3, 4).area() should be 12, got {r.area()}"
    assert r.perimeter() == 14, f"perimeter should be 14, got {r.perimeter()}"
    assert r.is_square() is False, "Rectangle(3, 4) is not a square"
    assert impl(5, 5).is_square() is True, "Rectangle(5, 5) is a square"
    assert impl(0, 7).area() == 0, "a zero-width rectangle has area 0"
    small, big = impl(1, 2), impl(10, 20)
    assert (small.area(), big.area()) == (2, 200), "each object keeps its own sizes"


def check_rectangle() -> None:
    report("1. Rectangle", test_rectangle, Rectangle)


def main() -> None:
    check_rectangle()


if __name__ == "__main__":
    main()
