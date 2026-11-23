"""Shared number helpers that Project Euler problems keep reaching for."""

import math
from collections.abc import Iterator


def sum_multiples(k: int, limit: int) -> int:
    """Sum of k, 2k, 3k, ... below ``limit`` in O(1): k * m(m+1)/2."""
    m = (limit - 1) // k
    return k * m * (m + 1) // 2


def fibonacci_below(limit: int) -> Iterator[int]:
    """1, 2, 3, 5, 8, ... (Project Euler's start) while below ``limit``."""
    a, b = 1, 2
    while a < limit:
        yield a
        a, b = b, a + b


def primes_below(limit: int) -> list[int]:
    """Sieve of Eratosthenes: cross off multiples of each prime from its square."""
    if limit <= 2:
        return []
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for p in range(2, math.isqrt(limit - 1) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(range(p * p, limit, p)))  # one slice, no loop
    return [n for n, flag in enumerate(sieve) if flag]


def is_prime(n: int) -> bool:
    """Trial division by 2, 3 and then 6k +/- 1 up to sqrt(n)."""
    if n < 4:
        return n >= 2
    if n % 2 == 0 or n % 3 == 0:
        return False
    return all(n % d and n % (d + 2) for d in range(5, math.isqrt(n) + 1, 6))


def nth_prime(n: int) -> int:
    """The n-th prime (1-based), sieving up to the bound n(ln n + ln ln n)."""
    limit = 15 if n < 6 else int(n * (math.log(n) + math.log(math.log(n)))) + 1
    return primes_below(limit)[n - 1]


def prime_factors(n: int) -> list[int]:
    """Factors with multiplicity; dividing them out shrinks the search to sqrt(rest)."""
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2  # after 2, only odd candidates
    if n > 1:
        factors.append(n)  # what is left has no factor <= its square root: prime
    return factors


def collatz_sequence(n: int) -> list[int]:
    """n, then n/2 if even or 3n+1 if odd, until 1."""
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def collatz_length(n: int, cache: dict[int, int] | None = None) -> int:
    """Number of terms in n's Collatz sequence; share ``cache`` across calls to memoise."""
    cache = {1: 1} if cache is None else cache
    cache.setdefault(1, 1)
    path = []
    while n not in cache:  # iterative: long chains cannot overflow the stack
        path.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    for value in reversed(path):
        length += 1
        cache[value] = length
    return length
