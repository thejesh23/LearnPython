"""`__slots__` — fixed attributes, smaller objects.

A normal instance keeps its attributes in a per-object dictionary,
`obj.__dict__`. That is what lets you add any attribute at any time, and it
costs memory for every single object.

Declaring `__slots__ = ("x", "y")` tells Python the exact attribute names up
front. Instances then store those values in fixed places, with no `__dict__`:

    + less memory per object (it adds up with millions of small objects)
    + a typo such as `p.xx = 1` raises AttributeError instead of silently
      creating a new attribute
    - you cannot add attributes that are not listed
    - every class in the hierarchy must declare slots, or the dict comes back

Most classes do not need slots. Reach for them when you create very many
instances of a small class, or with `@dataclass(slots=True)`.
"""

import sys
import tracemalloc
from dataclasses import dataclass


class PointDict:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class PointSlots:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def no_dict_demo() -> None:
    d = PointDict(1, 2)
    s = PointSlots(1, 2)
    print(f"PointDict  __dict__: {d.__dict__}")
    print(f"PointSlots has __dict__? {hasattr(s, '__dict__')}")

    # A plain object accepts any new attribute, typos included.
    d.xx = 99
    print(f"typo silently added to PointDict: {d.__dict__}")
    try:
        s.xx = 99  # type: ignore[attr-defined]
    except AttributeError as exc:
        print(f"PointSlots refuses it: AttributeError: {exc}")


def memory_for(cls: type, count: int = 10_000) -> int:
    """Bytes allocated while creating `count` instances of cls."""
    tracemalloc.start()
    objects = [cls(1.5, 2.5) for _ in range(count)]
    used, _peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objects
    return used


def memory_demo() -> None:
    # sys.getsizeof counts only the object itself, not its __dict__, so on
    # its own it hides most of the difference.
    d, s = PointDict(1, 2), PointSlots(1, 2)
    print(f"getsizeof alone: dict object {sys.getsizeof(d)} bytes, "
          f"slotted object {sys.getsizeof(s)} bytes")
    with_dict = sys.getsizeof(d) + sys.getsizeof(d.__dict__)
    print(f"adding the __dict__ ({with_dict} bytes), slots are smaller: "
          f"{sys.getsizeof(s) < with_dict}")

    # tracemalloc counts every allocation, which is the honest measurement.
    # The exact numbers differ between Python versions; the direction does not.
    plain = memory_for(PointDict)
    slotted = memory_for(PointSlots)
    print(f"10,000 slotted points used less memory: {slotted < plain}")


class Point3D(PointSlots):
    __slots__ = ("z",)  # list only the *new* names; x and y are inherited

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y)
        self.z = z


class Labelled(PointSlots):
    """Forgot __slots__: this subclass quietly gets a __dict__ again."""


def slots_gotchas_demo() -> None:
    p = Point3D(1, 2, 3)
    print(f"Point3D ({p.x}, {p.y}, {p.z}) has __dict__? {hasattr(p, '__dict__')}")

    lab = Labelled(1, 2)
    lab.name = "origin-ish"
    print(f"Labelled has __dict__? {hasattr(lab, '__dict__')}: {lab.__dict__}")

    # A slot name cannot also have a class-level default value.
    try:
        class Bad:
            __slots__ = ("x",)
            x = 0
    except ValueError as exc:
        print(f"ValueError: {exc}")


@dataclass(slots=True)
class Pixel:
    x: int
    y: int
    colour: str = "black"  # defaults work: the dataclass handles them


def dataclass_slots_demo() -> None:
    px = Pixel(3, 4)
    print(f"{px}, __slots__ = {Pixel.__slots__}")
    print(f"has __dict__? {hasattr(px, '__dict__')}")
    try:
        px.alpha = 0.5  # type: ignore[attr-defined]
    except AttributeError as exc:
        print(f"AttributeError: {exc}")


def main() -> None:
    no_dict_demo()
    print()
    memory_demo()
    print()
    slots_gotchas_demo()
    print()
    dataclass_slots_demo()


if __name__ == "__main__":
    main()
