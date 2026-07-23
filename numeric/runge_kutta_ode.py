"""Runge-Kutta: integrate an ODE initial value problem step by step.

Given y' = f(t, y) and a starting value y(t0), we march forward in steps of h.
Euler's method takes the slope at the current point and steps along it; it is
simple but crude, with error per step of order h^2 and accumulated error of
order h, so halving the step only halves the error.

RK4 samples the slope four times inside each step — at the start, twice at the
midpoint, and at the end — and blends them with weights 1, 2, 2, 1. That
cancels the low-order error terms, giving accumulated error of order h^4: halve
the step and the error drops roughly sixteenfold. The two are compared on
y' = y with y(0) = 1, whose exact solution is e^t, so the true error is known
and RK4's advantage is stark even at a coarse step.
"""

from collections.abc import Callable

ODE = Callable[[float, float], float]


def euler(f: ODE, y0: float, t0: float, t1: float, n: int) -> list[tuple[float, float]]:
    h = (t1 - t0) / n
    t, y = t0, y0
    path = [(t, y)]
    for _ in range(n):
        y += h * f(t, y)
        t += h
        path.append((t, y))
    return path


def rk4(f: ODE, y0: float, t0: float, t1: float, n: int) -> list[tuple[float, float]]:
    h = (t1 - t0) / n
    t, y = t0, y0
    path = [(t, y)]
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
        path.append((t, y))
    return path


def main() -> None:
    import math

    # y' = y, y(0) = 1  =>  y(t) = e^t.  Integrate to t = 2.
    f = lambda t, y: y
    exact = math.e**2

    for n in (10, 20, 40):
        ye = euler(f, 1.0, 0.0, 2.0, n)[-1][1]
        yr = rk4(f, 1.0, 0.0, 2.0, n)[-1][1]
        print(f"n={n:>3}  euler err {abs(ye - exact):.3e}   "
              f"rk4 err {abs(yr - exact):.3e}")
    print(f"exact e^2 = {exact:.10f}")

    # RK4 error drops ~16x when the step is halved (order h^4).
    e1 = abs(rk4(f, 1.0, 0.0, 2.0, 20)[-1][1] - exact)
    e2 = abs(rk4(f, 1.0, 0.0, 2.0, 40)[-1][1] - exact)
    print(f"rk4 error ratio on halving step: {e1 / e2:.1f}x (expect ~16)")

    # A second problem with a known solution: y' = -2 t y, y(0) = 1 => e^(-t^2).
    g = lambda t, y: -2 * t * y
    exact_g = math.exp(-4)  # at t = 2
    yr = rk4(g, 1.0, 0.0, 2.0, 40)[-1][1]
    print(f"rk4 gaussian ODE: {yr:.10f}  exact {exact_g:.10f}  "
          f"err {abs(yr - exact_g):.2e}")


if __name__ == "__main__":
    main()
