"""The `operator` module, and how Python resolves a binary operation.

`operator.add` is the function behind `+`; `itemgetter`/`attrgetter` are faster,
clearer replacements for the lambdas people write as sort keys.

Resolution order for `a + b`:
    1. If type(b) is a *subclass* of type(a) and overrides __radd__, b wins first.
    2. Otherwise a.__add__(b) runs.
    3. If it returns NotImplemented, b.__radd__(a) runs.
    4. If that also returns NotImplemented, Python raises TypeError.

Returning `NotImplemented` (not raising, not returning False) is what makes
step 3 possible — it is the mechanism for cooperative operator overloading.
"""

import operator
from functools import reduce


class Money:
    def __init__(self, amount: float, currency: str = "USD") -> None:
        self.amount, self.currency = amount, currency

    def __repr__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"

    def __add__(self, other):
        if isinstance(other, Money) and other.currency == self.currency:
            return Money(self.amount + other.amount, self.currency)
        if isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented  # let the other operand try

    def __radd__(self, other):
        # Makes sum() work: sum starts from 0, so 0 + Money is tried first.
        return self.__add__(other)

    def __mul__(self, k):
        return Money(self.amount * k, self.currency) if isinstance(k, (int, float)) else NotImplemented

    __rmul__ = __mul__


def main() -> None:
    print(f"operator.add(2, 3) = {operator.add(2, 3)}")
    print(f"reduce(operator.mul, 1..5) = {reduce(operator.mul, range(1, 6))}")

    people = [("Ada", 36, "eng"), ("Grace", 45, "navy"), ("Alan", 41, "math")]
    print(f"sorted by age:  {sorted(people, key=operator.itemgetter(1))}")
    print(f"two keys:       {sorted(people, key=operator.itemgetter(2, 0))}")
    print(f"pluck a column: {list(map(operator.itemgetter(0), people))}")

    class Row:
        def __init__(self, n: int) -> None:
            self.n = n

    rows = [Row(3), Row(1), Row(2)]
    print(f"attrgetter sort: {[r.n for r in sorted(rows, key=operator.attrgetter('n'))]}")
    print(f"methodcaller: {list(map(operator.methodcaller('upper'), ['a', 'b']))}")

    print("\ncustom operator resolution:")
    a, b = Money(10), Money(5)
    print(f"  Money + Money = {a + b}")
    print(f"  Money + 2.5   = {a + 2.5}")
    print(f"  2.5 + Money   = {2.5 + a}   (float.__add__ returned NotImplemented, __radd__ ran)")
    print(f"  sum([...])    = {sum([a, b, Money(1)])}")
    print(f"  3 * Money     = {3 * a}")

    try:
        a + "cash"
    except TypeError as exc:
        print(f"  TypeError: {exc}")

    print(f"\nin-place operators exist too: iadd -> {operator.iadd([1], [2])}")
    print(f"comparison: lt(1, 2) = {operator.lt(1, 2)}, contains([1,2], 2) = {operator.contains([1, 2], 2)}")


if __name__ == "__main__":
    main()
