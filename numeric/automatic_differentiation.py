"""Forward-mode automatic differentiation with dual numbers.

A dual number carries a value and a derivative together, written a + b*eps where
eps is a symbol with eps^2 = 0. Feeding x + 1*eps through any function makes the
arithmetic rules replay the chain rule automatically: the eps-part of the result
is the exact derivative at x. So (a + b eps)(c + d eps) = ac + (ad + bc) eps is
just the product rule, and it composes through every operation with no round-off
from a step size.

This is not symbolic differentiation and not a finite difference. It evaluates
the function once, in the augmented number system, and gets the derivative exact
to machine precision in a single pass, at a constant-factor cost over the plain
evaluation. Reverse mode (backprop) is the transpose that wins when there are
many inputs and one output; forward mode shown here wins for one input. Each
derivative below is cross-checked against a central finite difference.
"""

from __future__ import annotations

import math
from typing import Callable, Union

Number = Union[int, float, "Dual"]


class Dual:
    """A value paired with its derivative; operators replay the chain rule."""

    def __init__(self, value: float, deriv: float = 0.0) -> None:
        self.value = value
        self.deriv = deriv

    def _coerce(self, other: Number) -> "Dual":
        return other if isinstance(other, Dual) else Dual(float(other), 0.0)

    def __add__(self, other: Number) -> "Dual":
        o = self._coerce(other)
        return Dual(self.value + o.value, self.deriv + o.deriv)

    __radd__ = __add__

    def __sub__(self, other: Number) -> "Dual":
        o = self._coerce(other)
        return Dual(self.value - o.value, self.deriv - o.deriv)

    def __rsub__(self, other: Number) -> "Dual":
        return self._coerce(other).__sub__(self)

    def __mul__(self, other: Number) -> "Dual":
        o = self._coerce(other)
        return Dual(self.value * o.value,
                    self.deriv * o.value + self.value * o.deriv)

    __rmul__ = __mul__

    def __truediv__(self, other: Number) -> "Dual":
        o = self._coerce(other)
        # Quotient rule: (u/v)' = (u'v - u v') / v^2.
        return Dual(self.value / o.value,
                    (self.deriv * o.value - self.value * o.deriv) / o.value ** 2)

    def __rtruediv__(self, other: Number) -> "Dual":
        return self._coerce(other).__truediv__(self)

    def __pow__(self, p: float) -> "Dual":
        # Power rule for a constant exponent: (u^p)' = p u^(p-1) u'.
        return Dual(self.value ** p,
                    p * self.value ** (p - 1) * self.deriv)

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.deriv)

    def __repr__(self) -> str:
        return f"Dual(value={self.value:.6g}, deriv={self.deriv:.6g})"


def sin(x: Dual) -> Dual:
    return Dual(math.sin(x.value), math.cos(x.value) * x.deriv)


def cos(x: Dual) -> Dual:
    return Dual(math.cos(x.value), -math.sin(x.value) * x.deriv)


def exp(x: Dual) -> Dual:
    e = math.exp(x.value)
    return Dual(e, e * x.deriv)


def log(x: Dual) -> Dual:
    return Dual(math.log(x.value), x.deriv / x.value)


def derivative(f: Callable[[Dual], Dual], x: float) -> float:
    """Exact derivative of f at x via one forward-mode pass."""
    return f(Dual(x, 1.0)).deriv


def finite_difference(f: Callable[[float], float], x: float,
                      h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def main() -> None:
    cases: list[tuple[str, Callable[[Dual], Dual],
                      Callable[[float], float], float]] = [
        ("x^3", lambda x: x ** 3, lambda x: x ** 3, 2.0),
        ("sin(x)*exp(x)", lambda x: sin(x) * exp(x),
         lambda x: math.sin(x) * math.exp(x), 1.0),
        ("1/x", lambda x: 1.0 / x, lambda x: 1.0 / x, 3.0),
        ("log(x^2 + 1)", lambda x: log(x * x + 1.0),
         lambda x: math.log(x * x + 1.0), 2.0),
        ("x/(x+1)", lambda x: x / (x + 1.0), lambda x: x / (x + 1.0), 4.0),
    ]

    print(f"{'function':<16}{'x':>5}{'autodiff':>14}{'finite diff':>15}"
          f"{'|diff|':>12}")
    for name, fd_dual, fd_plain, x in cases:
        ad = derivative(fd_dual, x)
        num = finite_difference(fd_plain, x)
        print(f"{name:<16}{x:>5.1f}{ad:>14.8f}{num:>15.8f}"
              f"{abs(ad - num):>12.1e}")

    # Known-exact spot checks.
    print("\nexact spot checks")
    print(f"  d/dx x^3 at 2 = {derivative(lambda x: x ** 3, 2.0):.6f} "
          f"(expect 12)")
    print(f"  d/dx sin at 0 = {derivative(sin, 0.0):.6f} (expect 1)")
    print(f"  d/dx exp at 0 = {derivative(exp, 0.0):.6f} (expect 1)")
    print(f"  d/dx log at 1 = {derivative(log, 1.0):.6f} (expect 1)")

    # The value part is the ordinary evaluation, carried alongside for free.
    r = (lambda x: sin(x) * exp(x))(Dual(1.0, 1.0))
    print(f"\nsin(1)*exp(1): value {r.value:.6f}, derivative {r.deriv:.6f}")


if __name__ == "__main__":
    main()
