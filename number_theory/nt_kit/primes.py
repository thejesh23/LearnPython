"""Primes and factoring: deterministic Miller-Rabin, Pollard's rho, and what they unlock."""

import math
import random

# Enough Miller-Rabin bases to be exact for every n < 3.3 * 10**24.
_WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n: int) -> bool:
    """Miller-Rabin with fixed bases: exact (no false positives) for n < 3.3e24."""
    if n < 2:
        return False
    for p in _WITNESSES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in _WITNESSES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # a is a witness: n is certainly composite
    return True


def next_prime(n: int) -> int:
    """The smallest prime strictly greater than n."""
    candidate = max(n + 1, 2)
    while not is_prime(candidate):
        candidate += 1
    return candidate


def pollard_rho(n: int, rng: random.Random | None = None) -> int:
    """A nontrivial factor of composite n: walk x -> x^2 + c until gcd(|x - y|, n) > 1."""
    if n % 2 == 0:
        return 2
    rng = rng or random.Random()
    while True:
        c = rng.randrange(1, n)
        x = y = rng.randrange(2, n)
        d = 1
        while d == 1:  # Floyd: y moves twice as fast as x
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d  # otherwise this c was unlucky; try another


def factorize(n: int, rng: random.Random | None = None) -> list[int]:
    """Prime factors of n >= 1 with multiplicity, ascending."""
    if n < 1:
        raise ValueError("n must be at least 1")
    factors: list[int] = []
    for p in (2, 3, 5, 7):
        while n % p == 0:
            factors.append(p)
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if is_prime(m):
            factors.append(m)
        else:
            d = pollard_rho(m, rng)
            stack += [d, m // d]
    return sorted(factors)


def divisors(n: int) -> list[int]:
    """Every positive divisor of n, built from its prime factorisation."""
    result = [1]
    for p in factorize(n):
        result += [d * p for d in result]
    return sorted(set(result))


def totient(n: int) -> int:
    """Euler's phi: how many of 1..n are coprime to n, as n * prod(1 - 1/p)."""
    result = n
    for p in set(factorize(n)):
        result -= result // p
    return result
