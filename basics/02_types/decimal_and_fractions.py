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


def main() -> None:
    float_error_demo()


if __name__ == "__main__":
    main()
