"""`__eq__` and `__hash__` — the contract behind dict keys and set members.

A set or dict finds an item in two steps: `hash(item)` picks a bucket, then
`==` checks the candidates in that bucket. That only works if one rule holds:

    if a == b, then hash(a) == hash(b)

(The reverse need not hold: unequal objects may share a hash.) Break the rule
and sets keep duplicates and dicts cannot find keys you just stored.

A second rule follows from the first: an object's hash must not change while
it sits in a set or dict. So anything hashed by value should be immutable,
which is why lists are unhashable and tuples are. For your own classes the
easy, safe choice is `@dataclass(frozen=True)`.

dunder_methods.py shows how to write the two methods; this file is about why
the contract matters and what breaks when it is ignored.
"""


class BrokenPoint:
    """Value equality, but the default identity-based hash: breaks the rule."""

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BrokenPoint):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    __hash__ = object.__hash__  # hash by identity: different for each object


class Point(BrokenPoint):
    def __hash__(self) -> int:
        # Hash exactly the fields that __eq__ compares.
        return hash((self.x, self.y))


def contract_demo() -> None:
    a, b = BrokenPoint(1, 2), BrokenPoint(1, 2)
    print(f"a == b: {a == b}, same hash: {hash(a) == hash(b)}")
    print(f"set of two equal BrokenPoints has {len({a, b})} items")
    print(f"BrokenPoint(1, 2) in {{a}}: {BrokenPoint(1, 2) in {a}}")

    p, q = Point(1, 2), Point(1, 2)
    print(f"set of two equal Points has {len({p, q})} item")
    print(f"Point(1, 2) in {{p}}: {Point(1, 2) in {p}}")


def mutable_key_demo() -> None:
    p = Point(1, 2)
    seen = {p}
    print(f"before: p in seen -> {p in seen}")

    # Changing a field changes the hash, but the set filed p under the old
    # one. The object is still inside, yet the set can no longer find it.
    p.x = 100
    print(f"after p.x = 100: p in seen -> {p in seen}")
    print(f"but iterating finds it: {any(item is p for item in seen)}")

    # This is why Python's own mutable containers refuse to be hashed.
    try:
        hash([1, 2])
    except TypeError as exc:
        print(f"TypeError: {exc}")


def main() -> None:
    contract_demo()
    print()
    mutable_key_demo()


if __name__ == "__main__":
    main()
