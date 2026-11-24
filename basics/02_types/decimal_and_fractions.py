"""Exact arithmetic: why floats drift, and what to use instead.

A float stores numbers in base 2. Most decimal fractions, such as 0.1, have no
exact base-2 form (just as 1/3 has no exact base-10 form), so the computer
stores the nearest value it can. The tiny errors are usually invisible, until
you compare with == or add the same amount thousands of times.

Three tools, picked by what the numbers mean:

    float + math.isclose   measurements and science, where "close" is fine
    decimal.Decimal        money and anything with fixed decimal places
    fractions.Fraction     exact ratios like 1/3 that no decimal can hold

basics/02_types/int_and_float.py shows the problem in one line; this file
explains it and works through the fixes. advanced/decimal_and_precision.py
goes further into float limits and precision contexts.
"""

import math
from decimal import Decimal
from decimal import ROUND_HALF_EVEN
from decimal import ROUND_HALF_UP


def float_error_demo() -> None:
    total = 0.1 + 0.2
    print(f"0.1 + 0.2 = {total!r}")
    print(f"0.1 + 0.2 == 0.3 -> {total == 0.3}")

    # Decimal(some_float) reveals the exact value the float really holds.
    print(f"0.1 is really stored as {Decimal(0.1)}")

    # The error builds up when you repeat an operation in a loop.
    ten_dimes = 0.0
    for _ in range(10):
        ten_dimes += 0.1
    print(f"ten times 0.1 = {ten_dimes!r}, equal to 1.0? {ten_dimes == 1.0}")

    # For floats, ask "close enough?" rather than "equal?".
    print(f"math.isclose(0.1 + 0.2, 0.3) -> {math.isclose(total, 0.3)}")
    # Near zero a relative tolerance never matches, so give an absolute one.
    tiny = 1e-17
    print(f"isclose(1e-17, 0.0) -> {math.isclose(tiny, 0.0)}")
    print(f"isclose(1e-17, 0.0, abs_tol=1e-9) -> "
          f"{math.isclose(tiny, 0.0, abs_tol=1e-9)}")


def to_cents(amount: Decimal) -> Decimal:
    """Round a money amount to two decimal places, halves rounding up."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def decimal_money_demo() -> None:
    # Build a Decimal from a string. From a float you inherit the float's error.
    print(f"Decimal('0.1') = {Decimal('0.1')}")
    print(f"Decimal(0.1)   = {Decimal(0.1)}")

    print(f"Decimal 0.1 + 0.2 == 0.3 -> "
          f"{Decimal('0.1') + Decimal('0.2') == Decimal('0.3')}")

    # A small invoice. Decimal keeps every digit, so totals are exact.
    prices = [Decimal("19.99"), Decimal("5.25"), Decimal("0.10")]
    subtotal = sum(prices, Decimal("0"))
    print(f"subtotal = {subtotal}")

    # Multiplying adds decimal places; quantize brings it back to cents.
    discount = subtotal * Decimal("0.15")
    print(f"15% discount, raw     = {discount}")
    print(f"15% discount, rounded = {to_cents(discount)}")
    print(f"amount due            = {subtotal - to_cents(discount)}")

    # Mixing Decimal with float is refused, so errors cannot sneak back in.
    try:
        Decimal("1.10") + 0.1  # type: ignore[operator]
    except TypeError as exc:
        print(f"TypeError: {exc}")


def rounding_modes_demo() -> None:
    # Python's round() uses "banker's rounding": a tie goes to the even
    # neighbour. Over many values this avoids always pushing totals upward.
    print(f"round(0.5), round(1.5), round(2.5) = "
          f"{round(0.5)}, {round(1.5)}, {round(2.5)}")

    # Decimal lets you choose the rule. Shops and tax forms often want HALF_UP.
    whole = Decimal("1")
    print(f"{'value':>6} {'HALF_EVEN':>10} {'HALF_UP':>8}")
    for text in ["0.5", "1.5", "2.5", "2.6"]:
        value = Decimal(text)
        even = value.quantize(whole, rounding=ROUND_HALF_EVEN)
        up = value.quantize(whole, rounding=ROUND_HALF_UP)
        print(f"{text:>6} {even!s:>10} {up!s:>8}")

    # Floats surprise you here too: 2.675 is stored a hair below 2.675.
    print(f"round(2.675, 2) = {round(2.675, 2)}   (float)")
    print(f"Decimal quantize = {to_cents(Decimal('2.675'))}   (Decimal, HALF_UP)")


def main() -> None:
    float_error_demo()
    print()
    decimal_money_demo()
    print()
    rounding_modes_demo()


if __name__ == "__main__":
    main()
