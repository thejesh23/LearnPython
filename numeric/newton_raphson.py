"""Newton-Raphson: find a root of a scalar f by riding its tangent line.

From a guess x, the tangent to f at x crosses zero at x - f(x)/f'(x); that
crossing is the next guess. Near a simple root each step roughly squares the
error, so correct digits double every iteration — quadratic convergence.

The speed comes with sharp edges. If f'(x) is near zero the step explodes and
the iterate flies off; certain shapes make the guesses oscillate between two
values forever; and a poor start can converge to a different root than intended.
When you have no formula for f' you can replace it with a finite difference
using two recent points — that is the secant method, which converges a little
slower (order about 1.618) but needs only f.
"""

from collections.abc import Callable


def newton(
    f: Callable[[float], float],
    fprime: Callable[[float], float],
    x0: float,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> tuple[float, int, bool]:
    """Return (root, iterations, converged) using the exact derivative."""
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        if abs(fx) < tol:
            return x, i, True
        dfx = fprime(x)
        if dfx == 0.0:
            return x, i, False  # flat tangent: step is undefined
        x_next = x - fx / dfx
        if not _is_finite(x_next) or abs(x_next) > 1e12:
            return x_next, i, False  # diverged
        x = x_next
    return x, max_iter, abs(f(x)) < tol


def secant(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> tuple[float, int, bool]:
    """Newton with f' approximated from the last two points (no derivative)."""
    f0, f1 = f(x0), f(x1)
    for i in range(1, max_iter + 1):
        if abs(f1) < tol:
            return x1, i, True
        if f1 == f0:
            return x1, i, False  # secant slope is zero
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, f0 = x1, f1
        x1, f1 = x2, f(x2)
    return x1, max_iter, abs(f1) < tol


def _is_finite(x: float) -> bool:
    return x == x and abs(x) != float("inf")


def main() -> None:
    # sqrt(2) is the positive root of x^2 - 2; f' = 2x.
    root, iters, ok = newton(lambda x: x * x - 2, lambda x: 2 * x, x0=1.0)
    print(f"newton sqrt(2): {root:.15f} in {iters} iters, converged={ok}")
    print(f"exact sqrt(2):  {2 ** 0.5:.15f}")

    # Quadratic convergence: error roughly squares each step.
    x, errors = 1.0, []
    for _ in range(5):
        x = x - (x * x - 2) / (2 * x)
        errors.append(abs(x - 2 ** 0.5))
    print(f"errors per step: {['%.1e' % e for e in errors]}")

    # Divergence: x^3 - 2x + 2 with x0 = 0 oscillates 0, 1, 0, 1, ...
    _, _, ok = newton(
        lambda x: x**3 - 2 * x + 2, lambda x: 3 * x * x - 2, x0=0.0, max_iter=20
    )
    print(f"oscillating case converged: {ok}")

    # Flat tangent: f'(x) = 0 at the start is caught, not a crash.
    _, _, ok = newton(lambda x: x * x, lambda x: 2 * x, x0=0.0)
    print(f"start at the root's flat point converged: {ok}")

    # Secant fallback needs no derivative; still finds sqrt(2).
    root, iters, ok = secant(lambda x: x * x - 2, x0=1.0, x1=2.0)
    print(f"secant sqrt(2): {root:.15f} in {iters} iters, converged={ok}")


if __name__ == "__main__":
    main()
