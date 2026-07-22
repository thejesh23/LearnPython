"""Floating point, Decimal, and Fraction — picking the right numeric type.

A binary float cannot represent 0.1 exactly, so 0.1 + 0.2 != 0.3. That is not
a Python quirk; it is IEEE-754, and every language with binary floats has it.

Choose by domain:
    float     measurements, geometry, anything already approximate. Fast.
    Decimal   money and anything with statutory rounding rules. Exact base-10,
              configurable precision and rounding mode.
    Fraction  exact rational arithmetic — ratios, probabilities, symbolic work.

Never compare floats with ==; use math.isclose. Never use float for money.
"""

import math
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, getcontext, localcontext
from fractions import Fraction


def main() -> None:
    print(f"0.1 + 0.2       = {0.1 + 0.2!r}")
    print(f"== 0.3          -> {0.1 + 0.2 == 0.3}")
    print(f"isclose         -> {math.isclose(0.1 + 0.2, 0.3)}")
    print(f"what 0.1 really is: {Decimal(0.1)}")

    print(f"\nfloat limits: eps={2**-52:.3e}, max={1.8e308:.1e}, "
          f"1e308*10 = {1e308 * 10}")
    print(f"catastrophic cancellation: {(1e16 + 1) - 1e16} (expected 1.0)")
    print(f"summation order matters: {sum([1e16, 1, -1e16])} vs {sum([1e16, -1e16, 1])}")
    print(f"math.fsum fixes it: {math.fsum([1e16, 1, -1e16])}")

    print("\nDecimal — exact base-10:")
    print(f"  0.1 + 0.2 = {Decimal('0.1') + Decimal('0.2')}")
    print(f"  from a string, not a float: {Decimal('0.1')} vs {Decimal(0.1)}")
    getcontext().prec = 28
    print(f"  1/3 to 28 places: {Decimal(1) / Decimal(3)}")

    price = Decimal("19.99")
    tax = (price * Decimal("0.0825")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    print(f"  19.99 + 8.25% tax = {price + tax} (tax {tax}, rounded half-up)")

    print(f"  banker's rounding: 2.5 -> "
          f"{Decimal('2.5').quantize(Decimal('1'), ROUND_HALF_EVEN)}, 3.5 -> "
          f"{Decimal('3.5').quantize(Decimal('1'), ROUND_HALF_EVEN)}")
    print(f"  Python's round() uses the same rule: {round(2.5)}, {round(3.5)}")

    with localcontext() as ctx:  # scoped precision change
        ctx.prec = 5
        print(f"  inside localcontext(prec=5): {Decimal(1) / Decimal(7)}")
    print(f"  outside again: {Decimal(1) / Decimal(7)}")

    print("\nFraction — exact rationals:")
    third = Fraction(1, 3)
    print(f"  1/3 + 1/6 = {third + Fraction(1, 6)}")
    print(f"  sum of three thirds = {third * 3} (exactly 1)")
    print(f"  float 0.75 -> {Fraction(0.75)}, from string -> {Fraction('2/7')}")
    print(f"  limit_denominator: pi ~= {Fraction(math.pi).limit_denominator(1000)}")

    print("\nmoney in floats accumulates error:")
    total_float = sum(0.1 for _ in range(10))
    total_dec = sum(Decimal("0.10") for _ in range(10))
    print(f"  10 x 0.10 as float: {total_float!r}, as Decimal: {total_dec}")


if __name__ == "__main__":
    main()
