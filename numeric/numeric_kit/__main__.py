"""Examples and self-check: python3 -m numeric.numeric_kit"""

import itertools
import math
import random
import sys

from . import (
    bisect_root,
    derivative,
    determinant,
    dominant_eigen,
    integrate,
    mat_vec,
    newton_root,
    rk4,
    solve,
)


def cubic(x: float) -> float:
    """Newton's own worked example from 1669."""
    return x**3 - 2 * x - 5


def examples() -> None:
    print("1. d/dx sin at 0:", round(derivative(math.sin, 0.0), 9), "(exact 1)")
    print("2. root of x^3 - 2x - 5: bisection", round(bisect_root(cubic, 2, 3), 10),
          "| Newton", round(newton_root(cubic, 2.0), 10))
    print("3. integral of exp(-x^2) over [-5, 5]:", round(integrate(lambda x: math.exp(-x * x), -5, 5), 10),
          "| sqrt(pi):", round(math.sqrt(math.pi), 10))
    t, y = rk4(lambda t, y: y, 1.0, 0.0, 1.0, steps=10)[-1]
    print(f"4. y' = y from y(0) = 1, 10 RK4 steps: y({t:g}) = {y:.8f} | e = {math.e:.8f}")
    A, b = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]
    print("5. solve 3x3:", [round(x, 9) for x in solve(A, b)], "| det", round(determinant(A), 9))
    lam, v = dominant_eigen([[2, 1], [1, 2]])
    print("6. dominant eigenpair of [[2,1],[1,2]]:", round(lam, 9), [round(x, 6) for x in v])


def det_by_permutations(A: list[list[float]]) -> float:
    """Leibniz formula: O(n!) but obviously correct, used as the reference."""
    n, total = len(A), 0.0
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        total += (-1) ** inversions * math.prod(A[i][perm[i]] for i in range(n))
    return total


def self_check() -> None:
    rng = random.Random(3)
    for _ in range(100):
        c = rng.uniform(0.5, 100)
        assert math.isclose(bisect_root(lambda x: x * x - c, 0, c + 1), math.sqrt(c), rel_tol=1e-9)
        assert math.isclose(newton_root(lambda x: x * x - c, c + 1), math.sqrt(c), rel_tol=1e-9)
        k, x = rng.randint(1, 5), rng.uniform(0.5, 2)
        assert math.isclose(derivative(lambda t: t**k, x), k * x ** (k - 1), rel_tol=1e-6)
        hi = rng.uniform(0.1, 3)
        assert math.isclose(integrate(lambda t: t**k, 0, hi), hi ** (k + 1) / (k + 1), rel_tol=1e-9)
        n = rng.randint(1, 5)
        A = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
        assert math.isclose(determinant(A), det_by_permutations(A), rel_tol=1e-9, abs_tol=1e-9)
        x_true = [rng.uniform(-5, 5) for _ in range(n)]
        if abs(determinant(A)) > 1e-3:
            x = solve(A, mat_vec(A, x_true))
            assert all(math.isclose(p, q, abs_tol=1e-6) for p, q in zip(x, x_true))
        # A^T A is symmetric with eigenvalues >= 0, so the dominant one is unique.
        S = [[sum(A[k][i] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        lam, v = dominant_eigen(S)
        assert all(math.isclose(p, lam * q, abs_tol=1e-6 * lam) for p, q in zip(mat_vec(S, v), v))
    errors = [abs(rk4(lambda t, y: y, 1.0, 0.0, 1.0, steps=n)[-1][1] - math.e) for n in (20, 40)]
    assert errors[1] < 1e-7 and 14 < errors[0] / errors[1] < 18, "RK4 should be 4th order"
    for bad in (lambda: solve([[1, 2], [2, 4]], [1, 2]), lambda: bisect_root(math.exp, 0, 1)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
