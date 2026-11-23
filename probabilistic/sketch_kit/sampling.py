"""Answers from random samples: reservoir sampling and Monte Carlo estimation.

Every function takes a ``random.Random`` so results are reproducible.
"""

import math
import random
from collections.abc import Callable, Iterable


def reservoir_sample[T](stream: Iterable[T], k: int, rng: random.Random) -> list[T]:
    """k items chosen uniformly from a stream of unknown length, in one pass."""
    reservoir: list[T] = []
    if k <= 0:
        return reservoir
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        elif (j := rng.randint(0, i)) < k:  # keep item i with probability k/(i+1)
            reservoir[j] = item
    return reservoir


def estimate_pi(n: int, rng: random.Random) -> float:
    """Four times the fraction of random points that land in the quarter circle."""
    inside = sum(rng.random() ** 2 + rng.random() ** 2 <= 1.0 for _ in range(n))
    return 4 * inside / n


def mc_integrate(f: Callable[[float], float], a: float, b: float, n: int,
                 rng: random.Random) -> tuple[float, float]:
    """Plain Monte Carlo: (estimate, standard error) of the integral over [a, b]."""
    values = [f(a + (b - a) * rng.random()) for _ in range(n)]
    mean = sum(values) / n
    variance = max(sum(v * v for v in values) / n - mean * mean, 0.0)
    return (b - a) * mean, (b - a) * math.sqrt(variance / n)


def stratified_integrate(f: Callable[[float], float], a: float, b: float, n: int,
                         rng: random.Random) -> float:
    """One sample in each of n equal strata: no clumps, no gaps, far less variance."""
    width = (b - a) / n
    return width * sum(f(a + (i + rng.random()) * width) for i in range(n))
