"""Monte Carlo estimation: answering hard maths by throwing darts at it.

If you can write a quantity as the average of some function over random inputs,
you can estimate it by drawing samples and averaging. Throwing points into the
unit square and counting how many land inside the quarter circle estimates pi/4.
Averaging f(x) over uniform x in [a, b] and multiplying by (b - a) estimates the
integral of f, whether or not f has an antiderivative.

The convergence rate is the important part, and it is disappointing. The standard
error of a sample mean is sigma/sqrt(n), so ten times the accuracy costs a hundred
times the samples. The saving grace is that the rate does not depend on dimension,
which is why Monte Carlo wins in high dimensions where grid methods die.

Since the constant sigma is the only thing you can change, variance reduction is
where the real gains live. Stratified sampling splits [0, 1] into equal strata and
draws one point from each, removing the clumping that plain uniform sampling
suffers, and typically cuts the error by a large factor for smooth integrands.
Antithetic pairing, drawing x and 1 - x together, does something similar for
monotone integrands.
"""

import math
import random
from typing import Callable


def estimate_pi(n: int, rng: random.Random) -> float:
    """Fraction of darts inside the quarter circle, times four."""
    inside = 0
    for _ in range(n):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4 * inside / n


def mc_integrate(f: Callable[[float], float], a: float, b: float, n: int,
                 rng: random.Random) -> tuple[float, float]:
    """Return (estimate, standard error) of the integral of f over [a, b]."""
    total = 0.0
    total_sq = 0.0
    for _ in range(n):
        v = f(a + (b - a) * rng.random())
        total += v
        total_sq += v * v
    mean = total / n
    variance = max(total_sq / n - mean * mean, 0.0)
    return (b - a) * mean, (b - a) * math.sqrt(variance / n)


def stratified_integrate(f: Callable[[float], float], a: float, b: float,
                         n: int, rng: random.Random) -> float:
    """One sample per stratum: the samples cannot clump or leave gaps."""
    width = (b - a) / n
    total = 0.0
    for i in range(n):
        total += f(a + (i + rng.random()) * width)
    return width * total


def antithetic_integrate(f: Callable[[float], float], a: float, b: float,
                         n: int, rng: random.Random) -> float:
    """Pair each sample with its mirror image; an odd n loses the last sample."""
    pairs = n // 2
    if pairs == 0:
        raise ValueError("need at least two samples for an antithetic pair")
    total = 0.0
    for _ in range(pairs):
        u = rng.random()
        total += f(a + (b - a) * u) + f(a + (b - a) * (1 - u))
    return (b - a) * total / (2 * pairs)


def rmse(runs: list[float], truth: float) -> float:
    return math.sqrt(sum((r - truth) ** 2 for r in runs) / len(runs))


def main() -> None:
    rng = random.Random(2718)

    print("estimating pi by rejection sampling")
    print(f"  one run of 100000 darts: {estimate_pi(100_000, rng):.6f}")
    # A single run's error is itself random, so average over 30 runs; only then
    # does the 1/sqrt(n) law show through instead of luck.
    print("\n  samples    rmse over 30 runs   rmse * sqrt(n)")
    for n in (100, 1_000, 10_000, 100_000):
        runs = [estimate_pi(n, random.Random(s)) for s in range(30)]
        err = rmse(runs, math.pi)
        print(f"  {n:>8}         {err:.6f}          {err * math.sqrt(n):>6.3f}")
    print("  the last column stays roughly flat: error shrinks like 1/sqrt(n)")

    # A function with no elementary antiderivative, so sampling earns its keep.
    def f(x: float) -> float:
        return math.exp(-x * x)

    truth = math.sqrt(math.pi) / 2 * math.erf(1.0)  # integral of e^-x^2 on [0,1]
    print(f"\nintegral of exp(-x^2) over [0, 1] = {truth:.10f}")
    print("  samples    estimate      error   reported std err")
    for n in (100, 1_000, 10_000, 100_000):
        est, se = mc_integrate(f, 0.0, 1.0, n, rng)
        print(f"  {n:>8}  {est:.8f}  {abs(est - truth):.8f}  {se:.8f}")

    print("\nroot mean squared error over 200 independent runs, n = 1000")
    plain, strat, anti = [], [], []
    for seed in range(200):
        r = random.Random(seed)
        plain.append(mc_integrate(f, 0.0, 1.0, 1000, r)[0])
        strat.append(stratified_integrate(f, 0.0, 1.0, 1000, r))
        anti.append(antithetic_integrate(f, 0.0, 1.0, 1000, r))
    e_plain = rmse(plain, truth)
    e_strat = rmse(strat, truth)
    e_anti = rmse(anti, truth)
    print(f"  plain uniform: {e_plain:.3e}")
    print(f"  stratified:    {e_strat:.3e}  ({e_plain / e_strat:.1f}x better)")
    print(f"  antithetic:    {e_anti:.3e}  ({e_plain / e_anti:.1f}x better)")

    print("\nstratified sampling converges faster than 1/sqrt(n) here")
    print("  samples   plain rmse   stratified rmse")
    for n in (100, 400, 1_600, 6_400):
        p = [mc_integrate(f, 0.0, 1.0, n, random.Random(s))[0]
             for s in range(60)]
        s_ = [stratified_integrate(f, 0.0, 1.0, n, random.Random(s))
              for s in range(60)]
        print(f"  {n:>7}   {rmse(p, truth):.3e}    {rmse(s_, truth):.3e}")

    print("\na four-dimensional integral, where grids become hopeless")
    # Integral of x1*x2*x3*x4 over the unit hypercube is (1/2)^4.
    r = random.Random(99)
    n = 200_000
    total = sum(r.random() * r.random() * r.random() * r.random()
                for _ in range(n))
    print(f"  estimate {total / n:.6f}, exact {0.5 ** 4:.6f}")
    print(f"  a grid with 10 points per axis would need {10 ** 4} evaluations "
          f"and still be crude")

    print("\nedge cases")
    r = random.Random(1)
    print(f"  one sample for pi: {estimate_pi(1, r)} (either 0 or 4)")
    print(f"  constant f = 1 over [0, 1]: "
          f"{mc_integrate(lambda x: 1.0, 0.0, 1.0, 100, r)[0]:.6f} "
          f"(std err {mc_integrate(lambda x: 1.0, 0.0, 1.0, 100, r)[1]:.1e})")
    print(f"  zero-width interval [2, 2]: "
          f"{mc_integrate(f, 2.0, 2.0, 100, r)[0]:.6f}")
    print(f"  reversed interval [1, 0] flips the sign: "
          f"{mc_integrate(f, 1.0, 0.0, 1000, r)[0]:.6f}")
    print(f"  antithetic with odd n uses 2 of 3 samples: "
          f"{antithetic_integrate(f, 0.0, 1.0, 3, r):.6f}")
    try:
        antithetic_integrate(f, 0.0, 1.0, 1, r)
    except ValueError as exc:
        print(f"  antithetic with n = 1: ValueError({exc})")


if __name__ == "__main__":
    main()
