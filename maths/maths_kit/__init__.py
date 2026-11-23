"""maths_kit: exact integer maths on Python's big ints.

    >>> from maths.maths_kit import gcd, power_mod, prime_factors, to_base
    >>> gcd(84, 36, 120), power_mod(2, 100, 1_000_000_007)
    (12, 976371285)
    >>> prime_factors(360), to_base(255, 16)
    ({2: 3, 3: 2, 5: 1}, 'ff')
"""

from .arithmetic import comb, from_base, gcd, isqrt, lcm, power_mod, to_base
from .primes import is_prime, prime_factors, primes_below

__all__ = [
    "gcd",
    "lcm",
    "power_mod",
    "isqrt",
    "comb",
    "to_base",
    "from_base",
    "is_prime",
    "primes_below",
    "prime_factors",
]
