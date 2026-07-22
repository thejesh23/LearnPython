"""`match` (3.10+) — structural pattern matching, not a C-style switch.

A `case` does not just compare equality: it matches the *shape* of a value and
binds names out of it in one step. That makes it a good fit for tagged tuples,
dicts parsed from JSON, and class instances.

Two rules catch newcomers:
  - A bare name in a pattern is a *capture*, matching anything. `case x:` does
    not compare against a variable x — it binds x. To compare against a
    constant, use a dotted name (`case Color.RED:`) or a guard.
  - Cases are tried in order; `case _:` is the catch-all default.
"""

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def describe(value: object) -> str:
    match value:
        case 0:
            return "the number zero"
        case 1 | 2 | 3:
            return "a small number"
        case int(n) if n < 0:  # class pattern plus a guard
            return f"a negative number ({n})"
        case str() as s if not s:
            return "an empty string"
        case str(s):
            return f"a string of length {len(s)}"
        case [x]:  # a one-element sequence
            return f"a one-item sequence holding {x!r}"
        case [first, *rest]:
            return f"a sequence starting {first!r} with {len(rest)} more"
        case {"type": kind, **extra}:  # dict pattern, capturing the remainder
            return f"a mapping of type {kind!r} with {len(extra)} other keys"
        case Point(x=0, y=0):
            return "the origin"
        case Point(x=px, y=py):
            return f"a point at ({px}, {py})"
        case _:
            return "something else"


def main() -> None:
    samples: list[object] = [
        0,
        2,
        -5,
        "",
        "hello",
        [42],
        [1, 2, 3],
        {"type": "circle", "r": 3},
        Point(0, 0),
        Point(3, 4),
        3.14,
    ]
    for sample in samples:
        print(f"{sample!r:>26} -> {describe(sample)}")


if __name__ == "__main__":
    main()
