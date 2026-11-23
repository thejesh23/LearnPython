"""Primes three ways: test one number, sieve a range, factor a number."""

from collections import Counter


def is_prime(n: int) -> bool:
    """Trial division by 2, 3 and then 6k +/- 1 up to sqrt(n)."""
    if n < 4:
        return n >= 2
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:  # i * i avoids a float sqrt and its rounding
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def primes_below(limit: int) -> list[int]:
    """Sieve of Eratosthenes: every prime p with 2 <= p < limit."""
    if limit < 3:
        return []
    flags = bytearray([1]) * limit
    flags[0] = flags[1] = 0
    p = 2
    while p * p < limit:
        if flags[p]:
            # Strike p*p, p*p + p, ... in one slice assignment.
            flags[p * p::p] = bytes(len(range(p * p, limit, p)))
        p += 1
    return [i for i, is_p in enumerate(flags) if is_p]


def prime_factors(n: int) -> dict[int, int]:
    """Prime factorisation as {prime: exponent}, e.g. 360 -> {2: 3, 3: 2, 5: 1}."""
    if n < 1:
        raise ValueError("prime_factors is defined for n >= 1")
    factors: Counter[int] = Counter()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1 if d == 2 else 2  # after 2, only odd candidates
    if n > 1:
        factors[n] += 1  # what is left has no factor <= its sqrt: it is prime
    return dict(factors)
