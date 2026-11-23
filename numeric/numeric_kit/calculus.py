"""Calculus on plain float functions: roots, derivatives, integrals, ODEs.

Each routine only *samples* f, so it works on any Python callable; the price is
a tolerance instead of an exact answer.
"""

import math
from collections.abc import Callable

Func = Callable[[float], float]


def derivative(f: Func, x: float, h: float = 1e-5) -> float:
    """Central difference (f(x+h) - f(x-h)) / 2h; error shrinks like h**2."""
    return (f(x + h) - f(x - h)) / (2 * h)


def bisect_root(f: Func, a: float, b: float, tol: float = 1e-12) -> float:
    """Halve [a, b] until it is tol wide. f(a) and f(b) must differ in sign."""
    fa = f(a)
    if fa * f(b) > 0:
        raise ValueError("f(a) and f(b) must straddle a root")
    while abs(b - a) > tol:
        m = (a + b) / 2
        fm = f(m)
        if fm == 0:
            return m
        if fa * fm < 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2


def newton_root(f: Func, x0: float, fprime: Func | None = None,
                tol: float = 1e-12, max_iter: int = 50) -> float:
    """Follow the tangent line to zero; uses ``derivative`` if fprime is None.

    Converges quadratically near a simple root but can wander off from a bad
    start, so it raises ArithmeticError instead of returning a wrong answer.
    """
    fprime = fprime or (lambda x: derivative(f, x))
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        slope = fprime(x)
        if slope == 0:
            raise ArithmeticError(f"flat tangent at x={x}")
        x -= fx / slope
        if not math.isfinite(x):
            break
    raise ArithmeticError("Newton's method did not converge")


def integrate(f: Func, a: float, b: float, tol: float = 1e-10) -> float:
    """Adaptive Simpson: split only the intervals where the estimate is poor."""

    def simpson(lo: float, hi: float) -> float:
        return (hi - lo) / 6 * (f(lo) + 4 * f((lo + hi) / 2) + f(hi))

    def refine(lo: float, hi: float, whole: float, tol: float, depth: int) -> float:
        mid = (lo + hi) / 2
        left, right = simpson(lo, mid), simpson(mid, hi)
        error = left + right - whole
        if depth == 0 or abs(error) <= 15 * tol:
            return left + right + error / 15  # Richardson extrapolation
        return refine(lo, mid, left, tol / 2, depth - 1) + refine(mid, hi, right, tol / 2, depth - 1)

    return refine(a, b, simpson(a, b), tol, 50)


def rk4(f: Callable[[float, float], float], y0: float, t0: float, t1: float,
        steps: int = 100) -> list[tuple[float, float]]:
    """Solve y' = f(t, y) from y(t0) = y0 to t1 with classic Runge-Kutta.

    Returns the path as (t, y) pairs; the error shrinks like h**4.
    """
    h = (t1 - t0) / steps
    t, y = t0, y0
    path = [(t, y)]
    for i in range(1, steps + 1):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t0 + i * h  # avoids drift from repeatedly adding h
        path.append((t, y))
    return path
