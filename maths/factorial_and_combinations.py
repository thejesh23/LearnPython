"""Factorials, binomial coefficients, and Pascal's triangle.

n! is the number of ways to arrange n distinct items: n choices for the first
slot, n-1 for the next, and so on. It grows faster than any exponential, so
even 100! has 158 digits. Python integers are arbitrary precision, so nothing
overflows, but big integers are slow to multiply and worth avoiding.

The binomial coefficient nCr counts the ways to choose r items out of n when
order does not matter. Writing it as n! / (r! (n-r)!) is correct but wasteful:
it builds three enormous numbers only to cancel almost all of them. The better
route multiplies and divides in step, using the identity that after k factors
the running product is already exactly divisible by k. That keeps every
intermediate no larger than the answer, and costs O(r) small operations.

Pascal's triangle is the same numbers laid out so each entry is the sum of the
two above it, which is the recurrence C(n, r) = C(n-1, r-1) + C(n-1, r).
"""

import math


def factorial_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is undefined for negative n")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is undefined for negative n")
    if n <= 1:
        return 1  # 0! == 1: there is exactly one way to arrange nothing
    return n * factorial_recursive(n - 1)


def combinations(n: int, r: int) -> int:
    """n choose r, keeping every intermediate value no bigger than the answer."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)  # C(n, r) == C(n, n-r); the smaller one is less work
    result = 1
    for k in range(1, r + 1):
        # result is C(n, k-1) here, so result * (n-k+1) is divisible by k.
        result = result * (n - k + 1) // k
    return result


def permutations(n: int, r: int) -> int:
    """Ordered selections: n * (n-1) * ... * (n-r+1)."""
    if r < 0 or r > n:
        return 0
    result = 1
    for k in range(r):
        result *= n - k
    return result


def pascal_row(n: int) -> list[int]:
    """Row n of Pascal's triangle, built from the previous entry in the row."""
    row = [1]
    for r in range(n):
        row.append(row[-1] * (n - r) // (r + 1))
    return row


def pascal_triangle(rows: int) -> list[list[int]]:
    return [pascal_row(n) for n in range(rows)]


def main() -> None:
    print(f"factorial_iterative(10) = {factorial_iterative(10)}")
    print(f"factorial_recursive(10) = {factorial_recursive(10)}")
    print(f"math.factorial(10)      = {math.factorial(10)}")
    print(f"0! = {factorial_iterative(0)}, 1! = {factorial_iterative(1)}")

    print(f"C(5, 2)   = {combinations(5, 2)}")
    print(f"C(52, 5)  = {combinations(52, 5)}")
    print(f"C(100, 50) has {len(str(combinations(100, 50)))} digits")
    print(f"P(5, 2)   = {permutations(5, 2)}")

    # Edge cases: r out of range, and the two trivial ends of a row.
    print(f"C(5, 0) = {combinations(5, 0)}, C(5, 5) = {combinations(5, 5)}")
    print(f"C(5, 6) = {combinations(5, 6)}, C(5, -1) = {combinations(5, -1)}")

    for row in pascal_triangle(6):
        print(" ".join(f"{v:3d}" for v in row))

    matches = all(combinations(n, r) == math.comb(n, r)
                  for n in range(30) for r in range(n + 1))
    print(f"agrees with math.comb for n < 30: {matches}")


if __name__ == "__main__":
    main()
