"""Gradient descent: minimise a function by stepping downhill.

The gradient points in the direction of steepest increase, so stepping the
opposite way, scaled by a learning rate, decreases the function. On a convex
surface every local minimum is the global one, and small enough steps are
guaranteed to converge to it.

The learning rate is the whole story. Too small and progress crawls; too large
and each step overshoots the valley, so the iterate bounces to ever-higher
points and diverges. Momentum smooths this by accumulating a velocity — a
running average of past gradients — which damps oscillation across a narrow
valley and accelerates along its floor, reaching the minimum in far fewer
steps. The demo minimises a 2-D quadratic bowl whose exact minimum is the
origin, so convergence is easy to check.
"""

from collections.abc import Callable

Vector = list[float]


def descend(
    grad: Callable[[Vector], Vector],
    start: Vector,
    lr: float,
    steps: int,
    momentum: float = 0.0,
) -> tuple[Vector, list[float]]:
    """Return the final point and the norm of the iterate at each step."""
    x = list(start)
    velocity = [0.0] * len(x)
    history: list[float] = []
    for _ in range(steps):
        g = grad(x)
        for i in range(len(x)):
            velocity[i] = momentum * velocity[i] - lr * g[i]
            x[i] += velocity[i]
        history.append(_norm(x))
    return x, history


def _norm(v: Vector) -> float:
    return sum(c * c for c in v) ** 0.5


def main() -> None:
    # f(x, y) = x^2 + 10 y^2, an elongated bowl; gradient = (2x, 20y).
    grad = lambda p: [2 * p[0], 20 * p[1]]
    start = [5.0, 5.0]

    final, hist = descend(grad, start, lr=0.05, steps=100)
    print(f"lr=0.05:        final {['%.2e' % c for c in final]}, "
          f"dist {hist[-1]:.2e}")

    # Too-large learning rate: the steep y-direction diverges.
    final, hist = descend(grad, start, lr=0.15, steps=30)
    print(f"lr=0.15 (big):  dist grew to {hist[-1]:.2e} (diverged)")

    # Momentum reaches the minimum far faster at the same safe learning rate.
    final_m, hist_m = descend(grad, start, lr=0.05, steps=100, momentum=0.8)
    print(f"lr=0.05 + mom:  final {['%.2e' % c for c in final_m]}, "
          f"dist {hist_m[-1]:.2e}")

    # Count steps to reach a fixed tolerance, with and without momentum.
    def steps_to(momentum: float, tol: float = 1e-3) -> int:
        x, v = list(start), [0.0, 0.0]
        for k in range(1, 5001):
            g = grad(x)
            for i in range(2):
                v[i] = momentum * v[i] - 0.05 * g[i]
                x[i] += v[i]
            if _norm(x) < tol:
                return k
        return -1

    print(f"steps to 1e-3, no momentum:   {steps_to(0.0)}")
    print(f"steps to 1e-3, momentum 0.8:  {steps_to(0.8)}")


if __name__ == "__main__":
    main()
