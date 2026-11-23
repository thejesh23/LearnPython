"""nt_kit: primes, factoring, modular inverses, CRT, square roots and discrete logs.

    >>> from number_theory.nt_kit import crt, factorize, sqrt_mod
    >>> factorize(600851475143)
    [71, 839, 1471, 6857]
    >>> crt([2, 3, 2], [3, 5, 7])
    (23, 105)
    >>> sqrt_mod(10, 13) in (6, 7)
    True
"""

from .modular import crt, discrete_log, extended_gcd, legendre, mod_inverse, sqrt_mod
from .primes import divisors, factorize, is_prime, next_prime, pollard_rho, totient

__all__ = [
    "extended_gcd",
    "mod_inverse",
    "crt",
    "legendre",
    "sqrt_mod",
    "discrete_log",
    "is_prime",
    "next_prime",
    "pollard_rho",
    "factorize",
    "divisors",
    "totient",
]
