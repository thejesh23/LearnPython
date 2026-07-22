"""`@dataclass` — the boilerplate remover for classes that mostly hold data.

The decorator reads the annotated class attributes and generates `__init__`,
`__repr__`, and `__eq__` for you. Options add more:

    frozen=True   immutable instances, and a generated __hash__
    order=True    comparison operators from the field order
    slots=True    no per-instance __dict__: less memory, no new attributes
    kw_only=True  every field must be passed by keyword

The mutable-default rule from functions applies here too, and the dataclass
machinery enforces it: use `field(default_factory=list)`, never `= []`.
"""

from dataclasses import asdict, dataclass, field, replace


@dataclass
class Point:
    x: float
    y: float = 0.0

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int = 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class Basket:
    owner: str
    items: list[str] = field(default_factory=list)  # a fresh list per instance
    tag: str = field(default="", repr=False)  # hidden from __repr__


def main() -> None:
    p = Point(3, 4)
    print(f"repr for free: {p!r}")
    print(f"eq for free:   {p == Point(3, 4)}")
    print(f"distance: {p.distance_to(Point(0, 0))}")

    versions = [Version(1, 2), Version(1, 0, 5), Version(2, 0)]
    print(f"sorted: {[str(v) for v in sorted(versions)]}")
    print(f"hashable because frozen: {len(set(versions))} unique")

    try:
        versions[0].minor = 9  # type: ignore[misc]
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}")

    # replace() builds a modified copy of a frozen instance.
    print(f"replace: {replace(versions[0], patch=1)}")

    b1, b2 = Basket("Ada"), Basket("Alan")
    b1.items.append("apple")
    print(f"{b1}  |  {b2}   (default_factory gave each its own list)")

    print(f"asdict: {asdict(p)}")


if __name__ == "__main__":
    main()
