"""euler_kit: a registry of solved Project Euler problems with their known answers,
plus the prime, Fibonacci and Collatz helpers they share.

    >>> from project_euler.euler_kit import PROBLEMS, prime_factors, run
    >>> PROBLEMS[3].solve(13195), prime_factors(13195)
    (29, [5, 7, 13, 29])
    >>> run(1).ok
    True
"""

from .helpers import (
    collatz_length,
    collatz_sequence,
    fibonacci_below,
    is_prime,
    nth_prime,
    prime_factors,
    primes_below,
    sum_multiples,
)
from .problems import PROBLEMS, Problem, Result, problem, run, run_all

__all__ = [
    "PROBLEMS", "Problem", "Result", "problem", "run", "run_all",
    "sum_multiples", "fibonacci_below", "primes_below", "is_prime", "nth_prime",
    "prime_factors", "collatz_sequence", "collatz_length",
]
