"""Bracketing root finders: bisection and a simplified Brent's method.

If f is continuous and f(a), f(b) have opposite signs, a root sits between
them. Bisection exploits only that: halve the interval, keep the half that
still brackets the sign change, repeat. It cannot fail and cannot leave the
bracket, but it is slow — one bit of accuracy per step, linear convergence.

Brent's method keeps that guarantee while going faster. When three points are
available it fits an inverse quadratic through them and jumps to where that
curve hits zero; when the fit would step outside the bracket or make poor
progress it falls back to a bisection step. The result stays bracketed like
bisection yet usually converges superlinearly, so on smooth functions it needs
far fewer iterations, as the comparison below shows.
"""

from collections.abc import Callable


def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-12,
    max_iter: int = 200,
) -> tuple[float, int]:
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must straddle a root")
    for i in range(1, max_iter + 1):
        m = 0.5 * (a + b)
        fm = f(m)
        if fm == 0.0 or 0.5 * (b - a) < tol:
            return m, i
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b), max_iter


def brent(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, int]:
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must straddle a root")
    if abs(fa) < abs(fb):  # keep b as the best (closest to zero) estimate
        a, b, fa, fb = b, a, fb, fa
    c, fc = a, fa  # c is the previous iterate
    for i in range(1, max_iter + 1):
        if abs(b - a) < tol or fb == 0.0:
            return b, i
        if fa != fc and fb != fc:  # inverse quadratic interpolation
            s = (
                a * fb * fc / ((fa - fb) * (fa - fc))
                + b * fa * fc / ((fb - fa) * (fb - fc))
                + c * fa * fb / ((fc - fa) * (fc - fb))
            )
        else:  # secant step
            s = b - fb * (b - a) / (fb - fa)
        if not (a < s < b or b < s < a):  # outside bracket: use bisection
            s = 0.5 * (a + b)
        fs = f(s)
        c, fc = b, fb
        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs
        if abs(fa) < abs(fb):
            a, b, fa, fb = b, a, fb, fa
    return b, max_iter


def main() -> None:
    # x^3 - x - 2 has a single real root near 1.5213797...
    f = lambda x: x**3 - x - 2
    exact = 1.5213797068045675

    root_b, iters_b = bisection(f, 1.0, 2.0)
    root_r, iters_r = brent(f, 1.0, 2.0)
    print(f"bisection: {root_b:.15f} in {iters_b} iters")
    print(f"brent:     {root_r:.15f} in {iters_r} iters")
    print(f"exact:     {exact:.15f}")
    print(f"brent used {iters_b // max(iters_r, 1)}x fewer iterations")

    # cos(x) - x has a root at the Dottie number 0.739085...
    import math

    g = lambda x: math.cos(x) - x
    root_b, iters_b = bisection(g, 0.0, 1.0)
    root_r, iters_r = brent(g, 0.0, 1.0)
    print(f"cos(x)=x bisection: {root_b:.12f} ({iters_b} iters)")
    print(f"cos(x)=x brent:     {root_r:.12f} ({iters_r} iters)")

    # A bad bracket (no sign change) is rejected rather than looping forever.
    try:
        bisection(f, 3.0, 4.0)
    except ValueError as e:
        print(f"rejected bad bracket: {e}")


if __name__ == "__main__":
    main()
