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


def main() -> None:
    no_dict_demo()


if __name__ == "__main__":
    main()
