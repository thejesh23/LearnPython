"""Digit dynamic programming: count numbers in a range by a digit property.

Many counting questions have the shape "how many integers in [0, N] satisfy a
property that depends only on the decimal digits?" Digit DP walks the digits of
N from most significant to least, choosing each digit in turn, and carries just
enough state to decide validity: here the running digit sum modulo k, plus a
"tight" flag saying whether the prefix chosen so far still equals N's prefix.

The tight flag is the heart of it. While tight, the next digit may not exceed
N's digit at this position, or we would overshoot N. The moment we place a digit
strictly smaller, every remaining position is free (0..9) and the count from
there depends only on how many positions remain and the carried state — so those
subproblems memoise and are shared across many prefixes.

This file counts integers in [0, N] whose digit sum is divisible by k. It uses
functools.lru_cache for the loose states and cross-checks against a direct loop.

Complexity: O(digits * k * 10) states, each O(10) work.
"""

from functools import lru_cache


def count_digit_sum_divisible(n: int, k: int) -> int:
    """Count integers in [0, n] whose digit sum is a multiple of k."""
    if n < 0:
        return 0
    digits = [int(c) for c in str(n)]
    length = len(digits)

    @lru_cache(maxsize=None)
    def solve(pos: int, rem: int, tight: bool) -> int:
        if pos == length:
            return 1 if rem == 0 else 0
        upper = digits[pos] if tight else 9
        total = 0
        for d in range(upper + 1):
            total += solve(pos + 1, (rem + d) % k, tight and d == upper)
        return total

    result = solve(0, 0, True)
    solve.cache_clear()  # cache keyed to this n; drop before returning
    return result


def brute_force(n: int, k: int) -> int:
    return sum(1 for x in range(n + 1)
               if sum(int(c) for c in str(x)) % k == 0)


def main() -> None:
    for n, k in [(20, 3), (100, 5), (0, 1), (9, 4)]:
        dp = count_digit_sum_divisible(n, k)
        print(f"[0, {n}] digit-sum divisible by {k}: {dp}")
        assert dp == brute_force(n, k), (n, k)

    print("\nlarger cross-checks against brute force:")
    for n in (999, 5000, 12345):
        for k in (2, 3, 7):
            assert count_digit_sum_divisible(n, k) == brute_force(n, k)
    print(f"  n up to 12345, k in 2,3,7: all agree")

    # A huge N where brute force would be far too slow, but digit DP is instant.
    big = 10 ** 18
    print(f"\n[0, 10**18] digit-sum divisible by 9: "
          f"{count_digit_sum_divisible(big, 9)}")


if __name__ == "__main__":
    main()
