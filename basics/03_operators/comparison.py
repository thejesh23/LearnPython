"""Comparison operators — and Python's chaining, which most languages lack.

`1 < x < 10` is one expression, not `(1 < x) < 10`. Python evaluates the
middle operand once and combines the comparisons with `and`. That makes range
checks read exactly like the maths.

Comparisons also work on sequences, where they run element by element
(lexicographic order), so `[1, 2] < [1, 3]` is True.
"""


def main() -> None:
    x = 7
    print(f"x == 7 -> {x == 7}")
    print(f"x != 7 -> {x != 7}")
    print(f"x <  10 -> {x < 10}")
    print(f"x >= 7 -> {x >= 7}")

    # Chained comparison: reads like maths, evaluates x only once.
    print(f"1 < x < 10 -> {1 < x < 10}")
    print(f"10 < x < 20 -> {10 < x < 20}")

    # Sequences compare lexicographically, element by element.
    print(f"[1, 2] < [1, 3] -> {[1, 2] < [1, 3]}")
    print(f"'apple' < 'banana' -> {'apple' < 'banana'}")
    print(f"(1, 2, 3) > (1, 2) -> {(1, 2, 3) > (1, 2)}")

    # Equality across numeric types compares value, not representation.
    print(f"1 == 1.0 -> {1 == 1.0}")

    # Ordering between unrelated types is an error, not a silent False.
    try:
        print(1 < "2")  # type: ignore[operator]
    except TypeError as exc:
        print(f"no cross-type ordering: {exc}")

    # sorted() and max()/min() build on the same comparison protocol.
    people = [("Ada", 36), ("Alan", 41), ("Grace", 45)]
    print(f"oldest = {max(people, key=lambda p: p[1])}")


if __name__ == "__main__":
    main()
