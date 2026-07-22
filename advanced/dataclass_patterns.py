"""Dataclasses beyond the basics: post-init, inheritance, and immutability.

`__post_init__` runs after the generated `__init__` — the place for derived
fields and validation. `field(init=False)` keeps a computed attribute out of the
constructor signature; `InitVar` does the reverse, accepting a value that is
used during construction but never stored.

Inheritance has one rule that surprises everyone: fields are ordered
base-first, so a base class with a default forces every subclass field to have
one too. `kw_only=True` sidesteps it entirely.

A frozen dataclass blocks attribute assignment, which makes instances hashable
and safe to share — but `object.__setattr__` is still the escape hatch that
`__post_init__` must use to set anything.
"""

from dataclasses import InitVar, asdict, dataclass, field, fields, replace


@dataclass
class Order:
    item: str
    quantity: int
    unit_price: float
    discount: InitVar[float] = 0.0  # consumed by __post_init__, never stored
    total: float = field(init=False)  # computed, not a constructor argument
    tags: list[str] = field(default_factory=list, compare=False)
    internal_id: str = field(default="", repr=False)

    def __post_init__(self, discount: float) -> None:
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        self.total = round(self.quantity * self.unit_price * (1 - discount), 2)


@dataclass(frozen=True, order=True, slots=True)
class Version:
    major: int
    minor: int
    label: str = field(default="", compare=False)  # ignored by ordering

    def __post_init__(self) -> None:
        # Frozen blocks normal assignment, so normalise through object.
        object.__setattr__(self, "label", self.label.lower())


@dataclass(kw_only=True)
class Base:
    created: str = "today"


@dataclass(kw_only=True)
class Event(Base):
    name: str  # no default needed, because kw_only lifts the ordering rule


def main() -> None:
    order = Order("widget", 3, 9.99, discount=0.1)
    print(f"{order}")
    print(f"  total computed in __post_init__: {order.total}")
    print(f"  'discount' is not a field: {[f.name for f in fields(order)]}")

    try:
        Order("bad", 0, 1.0)
    except ValueError as exc:
        print(f"  validation: {exc}")

    # compare=False excludes a field from equality.
    a, b = Order("x", 1, 1.0), Order("x", 1, 1.0)
    a.tags.append("urgent")
    print(f"  equal despite different tags: {a == b}")

    print("frozen + order + slots:")
    versions = [Version(1, 2, "BETA"), Version(1, 0), Version(2, 0, "GA")]
    print(f"  sorted: {sorted(versions)}")
    print(f"  label normalised: {versions[0].label!r}")
    print(f"  hashable: {len(set(versions))}, no __dict__: {not hasattr(versions[0], '__dict__')}")
    try:
        versions[0].minor = 9
    except Exception as exc:
        print(f"  {type(exc).__name__}: {exc}")
    print(f"  replace() makes a modified copy: {replace(versions[0], minor=5)}")

    print("kw_only lifts the default-ordering restriction:")
    print(f"  {Event(name='deploy')}")

    print(f"asdict: {asdict(Version(3, 1))}")
    print(f"field metadata: {[(f.name, f.type) for f in fields(Version)]}")


if __name__ == "__main__":
    main()
