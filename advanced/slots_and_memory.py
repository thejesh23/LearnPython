"""`__slots__` — trading flexibility for memory and attribute speed.

By default every instance carries a `__dict__`, which is why you can attach new
attributes at runtime. That dict costs real memory, and it dominates when you
have millions of small objects.

Declaring `__slots__` replaces it with a fixed array of descriptors: less
memory, faster attribute access, and no ability to add unlisted attributes.

Caveats: a subclass without its own `__slots__` reintroduces `__dict__`;
multiple inheritance from two slotted classes with different layouts is an
error; and `weakref` support disappears unless you list `__weakref__`.
"""

import sys
from dataclasses import dataclass


class Regular:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y


class Slotted:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y


@dataclass(slots=True)
class SlottedPoint:
    x: int
    y: int


class SlottedChild(Slotted):
    """No __slots__ here, so instances get a __dict__ back."""


def deep_size(obj: object) -> int:
    size = sys.getsizeof(obj)
    if hasattr(obj, "__dict__"):
        size += sys.getsizeof(obj.__dict__)
    return size


def main() -> None:
    r, s = Regular(1, 2), Slotted(1, 2)
    print(f"Regular instance: {deep_size(r)} bytes (incl. __dict__)")
    print(f"Slotted instance: {deep_size(s)} bytes")
    print(f"dataclass(slots=True): {deep_size(SlottedPoint(1, 2))} bytes")

    r.extra = "fine"
    print(f"regular accepts new attributes: {r.extra}")
    try:
        s.extra = "nope"
    except AttributeError as exc:
        print(f"AttributeError: {exc}")

    print(f"Slotted has __dict__: {hasattr(s, '__dict__')}")
    print(f"SlottedChild has __dict__ again: {hasattr(SlottedChild(1, 2), '__dict__')}")

    print(f"slot descriptors: {[n for n in Slotted.__slots__]}")
    print(f"the slots are descriptors: {type(Slotted.x).__name__}")

    # Scale is where it matters.
    many_regular = sum(deep_size(Regular(i, i)) for i in range(1000))
    many_slotted = sum(deep_size(Slotted(i, i)) for i in range(1000))
    print(f"1000 objects: regular {many_regular}B vs slotted {many_slotted}B "
          f"({100 - many_slotted * 100 // many_regular}% saved)")


if __name__ == "__main__":
    main()
