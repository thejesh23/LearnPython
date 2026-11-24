"""Instance methods, `@classmethod` and `@staticmethod`.

    instance method   gets `self`: works with one particular object
    @classmethod      gets `cls`: works with the class itself
    @staticmethod     gets neither: a plain function kept in the class

The everyday use of @classmethod is the *alternative constructor*: a second
way to build an object, such as `Date.from_string("2024-03-15")`. Because it
receives `cls`, it builds the right type even when called on a subclass.
@staticmethod is for a helper that belongs with the class but needs nothing
from it.
"""

from __future__ import annotations


class Money:
    def __init__(self, cents: int, currency: str) -> None:
        self.cents = cents
        self.currency = currency

    @classmethod
    def from_string(cls, text: str) -> Money:
        # "12.50 EUR" -> Money(1250, "EUR"). cls is Money here, or a subclass.
        amount, currency = text.split()
        return cls(round(float(amount) * 100), currency)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.cents / 100:.2f} {self.currency})"


def alternative_constructor_demo() -> None:
    print(Money(999, "USD"))
    print(Money.from_string("12.50 EUR"))


def main() -> None:
    alternative_constructor_demo()


if __name__ == "__main__":
    main()
