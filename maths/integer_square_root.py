"""Integer square root: the largest k with k * k <= n, computed exactly.

The obvious int(n ** 0.5) is wrong for large n. A Python float has 53 bits of
mantissa, so any integer beyond 2**53 cannot be represented exactly; the
conversion rounds, the square root of a rounded value is off, and the result
can land one either side of the true answer. For a number near 2**60 the error
is routine, and it fails silently, which is worse.

Newton's method fixes this using only integer arithmetic. To solve x**2 == n,
iterate x <- (x + n // x) // 2. Each step roughly doubles the number of
correct digits, so it converges in O(log log n) iterations, and integer
division means no rounding is ever introduced. The iteration decreases while
above the answer and then oscillates, so stopping the moment the next estimate
is not smaller lands exactly on floor(sqrt(n)).

Starting from a bit-length estimate rather than from n itself saves a handful
of iterations on large inputs.
"""

import math


def isqrt(n: int) -> int:
    """floor(sqrt(n)) for n >= 0, exact for arbitrarily large integers."""
    if n < 0:
        raise ValueError("isqrt is undefined for negative n")
    if n < 2:
        return n
    # 2 ** ceil(bits / 2) is at least sqrt(n), which Newton's method needs.
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:  # stop the moment the sequence stops decreasing
            return x
        x = y


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def icbrt(n: int) -> int:
    """The same idea for cube roots: x <- (2x + n // x**2) // 3."""
    if n < 0:
        raise ValueError("icbrt is defined here for n >= 0")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y


def main() -> None:
    for n in (0, 1, 2, 3, 4, 15, 16, 17, 10**6):
        print(f"isqrt({n}) = {isqrt(n)}")

    print(f"is_perfect_square(144) = {is_perfect_square(144)}")
    print(f"is_perfect_square(145) = {is_perfect_square(145)}")
    print(f"is_perfect_square(-4)  = {is_perfect_square(-4)}")

    # Where float sqrt breaks down: n is a perfect square just past 2**53.
    n = (2**60 + 1) ** 2
    exact = isqrt(n)
    floaty = int(n**0.5)
    print("n = (2**60 + 1)**2")
    print(f"  isqrt(n)      = {exact}")
    print(f"  int(n ** 0.5) = {floaty}")
    print(f"  exact is right: {exact * exact == n}")
    print(f"  float is right: {floaty * floaty == n}")

    print(f"matches math.isqrt up to 5000: "
          f"{all(isqrt(k) == math.isqrt(k) for k in range(5000))}")

    print(f"icbrt(27) = {icbrt(27)}, icbrt(26) = {icbrt(26)}")
    print(f"icbrt(10**18) = {icbrt(10**18)}")


if __name__ == "__main__":
    main()
