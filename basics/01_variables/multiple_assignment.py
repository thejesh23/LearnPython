"""Assigning several names at once — and taking values back apart.

Python lets the left-hand side of `=` be a *pattern* of names. The right-hand
side is evaluated fully first, then matched against that pattern. That single
rule gives you tuple unpacking, the one-line swap, and starred capture.
"""


def main() -> None:
    # Chained assignment: all three names point at the same value.
    a = b = c = 0
    print(f"a={a} b={b} c={c}")

    # Tuple unpacking: shapes on both sides must match.
    x, y = 3, 4
    print(f"x={x} y={y}")

    # The classic swap. No temporary variable: the right side (y, x) is
    # built as a tuple first, then unpacked back into x and y.
    x, y = y, x
    print(f"after swap: x={x} y={y}")

    # Starred assignment captures "everything else" into a list.
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"first={first} middle={middle} last={last}")

    # A lone underscore is the conventional name for "I must bind this,
    # but I do not care about it".
    _, minutes, _ = ("09", "30", "00")
    print(f"minutes={minutes}")

    # Unpacking mismatches fail loudly rather than silently dropping values.
    try:
        p, q = (1, 2, 3)
    except ValueError as exc:
        print(f"mismatch: {exc}")


if __name__ == "__main__":
    main()
