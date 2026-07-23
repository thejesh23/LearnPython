"""Numerical integration: approximate a definite integral from samples of f.

Quadrature rules replace the true area under f with the area under a simple
interpolant. The trapezoidal rule joins samples by straight lines; its error
shrinks like h^2 as the step h shrinks. Simpson's rule fits parabolas through
triples of points and is exact for cubics, so its error shrinks like h^4 —
doubling the number of panels cuts the error roughly sixteen-fold.

Uniform sampling wastes effort where f is smooth and starves the wiggly parts.
Adaptive Simpson fixes that: it compares a whole-interval Simpson estimate with
the sum of its two halves, and only recurses into a subinterval when the two
disagree by more than the tolerance. Work concentrates where the function
actually curves, so a target accuracy is reached with far fewer evaluations.
The demos compare against integrals whose exact value is known.
"""

from collections.abc import Callable


def trapezoid(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h


def simpson(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    if n % 2 == 1:
        n += 1  # Simpson needs an even number of panels
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(a + i * h)
    return total * h / 3


def adaptive_simpson(
    f: Callable[[float], float], a: float, b: float, tol: float = 1e-10
) -> float:
    def whole(a: float, b: float) -> tuple[float, float]:
        m = 0.5 * (a + b)
        return m, (b - a) / 6 * (f(a) + 4 * f(m) + f(b))

    def recurse(a: float, b: float, m: float, s: float, tol: float) -> float:
        lm, left = whole(a, m)
        rm, right = whole(m, b)
        if abs(left + right - s) <= 15 * tol:  # Richardson error estimate
            return left + right + (left + right - s) / 15
        return recurse(a, m, lm, left, tol / 2) + recurse(m, b, rm, right, tol / 2)

    m, s = whole(a, b)
    return recurse(a, b, m, s, tol)


def main() -> None:
    import math

    # integral of x^3 on [0, 1] is exactly 1/4; Simpson is exact for cubics.
    f = lambda x: x**3
    print(f"trapezoid x^3 (n=100): {trapezoid(f, 0, 1, 100):.10f}")
    print(f"simpson   x^3 (n=10):  {simpson(f, 0, 1, 10):.10f}  (exact 0.25)")

    # integral of sin on [0, pi] is exactly 2.
    print(f"simpson sin (n=100):   {simpson(math.sin, 0, math.pi, 100):.12f}")
    print(f"adaptive sin:          {adaptive_simpson(math.sin, 0, math.pi):.12f}"
          f"  (exact 2)")

    # Error shrinks with more panels; note the h^2 vs h^4 rates.
    g = lambda x: math.exp(x)
    exact = math.e - 1  # integral of e^x on [0, 1]
    print("panels   trap error    simpson error")
    for n in (2, 4, 8, 16, 32):
        te = abs(trapezoid(g, 0, 1, n) - exact)
        se = abs(simpson(g, 0, 1, n) - exact)
        print(f"{n:>5}   {te:.3e}   {se:.3e}")

    # Adaptive shines on a spiky integrand: a narrow Gaussian bump.
    spike = lambda x: math.exp(-100 * (x - 0.5) ** 2)
    exact_spike = math.sqrt(math.pi / 100) * math.erf(5)  # integral over [0,1]
    approx = adaptive_simpson(spike, 0, 1, tol=1e-12)
    print(f"adaptive spike: {approx:.12f}, error {abs(approx - exact_spike):.2e}")


if __name__ == "__main__":
    main()
