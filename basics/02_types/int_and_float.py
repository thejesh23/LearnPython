"""`int` and `float` — Python's two everyday number types.

The headline difference from most languages: Python `int` has **no maximum**.
It grows to whatever memory allows, so 2**200 is an exact integer, not an
overflow. `float` is an ordinary 64-bit IEEE-754 double and therefore *does*
have limits and rounding error.

Two division operators exist on purpose:
  /   true division, always produces a float
  //  floor division, rounds toward negative infinity
"""

from decimal import Decimal
from fractions import Fraction


def main() -> None:
    big = 2**200
    print(f"2**200 = {big}")
    print(f"digits: {len(str(big))}")

    print(f"7 / 2  = {7 / 2}")  # 3.5   — float
    print(f"7 // 2 = {7 // 2}")  # 3     — int
    print(f"-7 // 2 = {-7 // 2}")  # -4  — floors, does not truncate
    print(f"7 % 2  = {7 % 2}")
    print(f"divmod(7, 2) = {divmod(7, 2)}")

    # Floats cannot represent 0.1 exactly, so this famous check fails.
    print(f"0.1 + 0.2 == 0.3 -> {0.1 + 0.2 == 0.3}")
    print(f"0.1 + 0.2 = {0.1 + 0.2!r}")

    # Two exact alternatives from the standard library:
    print(f"Decimal: {Decimal('0.1') + Decimal('0.2')}")
    print(f"Fraction: {Fraction(1, 10) + Fraction(2, 10)}")

    # Readability: underscores are allowed inside numeric literals.
    population = 1_400_000_000
    print(f"population = {population:,}")


if __name__ == "__main__":
    main()
