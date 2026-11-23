"""A registry of solved problems with their known answers, and a runner that times them.

Each solver takes the problem's size as a parameter with the real value as the
default, so the small worked example in the problem statement is a free test.
"""

import time
from collections.abc import Callable
from dataclasses import dataclass

from .helpers import collatz_length, fibonacci_below, nth_prime, prime_factors, primes_below, sum_multiples


@dataclass(frozen=True)
class Problem:
    """A solved problem: its solver and the accepted answer."""

    number: int
    title: str
    solve: Callable[..., int]
    answer: int


@dataclass(frozen=True)
class Result:
    """What one run produced, and whether it matched the known answer."""

    problem: Problem
    value: int
    seconds: float

    @property
    def ok(self) -> bool:
        """True when the value equals the accepted answer."""
        return self.value == self.problem.answer


PROBLEMS: dict[int, Problem] = {}


def problem(number: int, title: str, answer: int) -> Callable[[Callable[..., int]], Callable[..., int]]:
    """Decorator that registers a solver under its problem number."""

    def register(solve: Callable[..., int]) -> Callable[..., int]:
        PROBLEMS[number] = Problem(number, title, solve, answer)
        return solve

    return register


@problem(1, "Multiples of 3 or 5", 233168)
def multiples_of_3_or_5(limit: int = 1000) -> int:
    """Inclusion-exclusion in O(1): multiples of 15 were counted twice."""
    return sum_multiples(3, limit) + sum_multiples(5, limit) - sum_multiples(15, limit)


@problem(2, "Even Fibonacci numbers", 4613732)
def even_fibonacci(limit: int = 4_000_000) -> int:
    """Sum of the even Fibonacci terms below ``limit``."""
    return sum(f for f in fibonacci_below(limit) if f % 2 == 0)


@problem(3, "Largest prime factor", 6857)
def largest_prime_factor(n: int = 600851475143) -> int:
    """Factors come out smallest first, so the last one is the largest."""
    return prime_factors(n)[-1]


@problem(7, "10001st prime", 104743)
def ten_thousand_first_prime(n: int = 10001) -> int:
    """The n-th prime from a sieve sized by an upper bound on it."""
    return nth_prime(n)


@problem(10, "Summation of primes", 142913828922)
def sum_of_primes(limit: int = 2_000_000) -> int:
    """One sieve, then a plain sum."""
    return sum(primes_below(limit))


@problem(14, "Longest Collatz sequence", 837799)
def longest_collatz(limit: int = 1_000_000) -> int:
    """Start below ``limit`` with the longest chain; a shared cache cuts each chain short."""
    cache = {1: 1}
    return max(range(1, limit), key=lambda n: collatz_length(n, cache))


def run(number: int) -> Result:
    """Solve one registered problem at full size and time it."""
    if number not in PROBLEMS:
        raise KeyError(f"problem {number} is not solved here; try one of {sorted(PROBLEMS)}")
    start = time.perf_counter()
    value = PROBLEMS[number].solve()
    return Result(PROBLEMS[number], value, time.perf_counter() - start)


def run_all() -> list[Result]:
    """Run every registered problem in number order."""
    return [run(number) for number in sorted(PROBLEMS)]
