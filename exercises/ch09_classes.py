"""Practice: classes (chapter 09).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch09_classes.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch09_classes.py: try first, peek second. The lessons
for this chapter are in basics/09_classes/.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import Self


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

class Rectangle:
    """A rectangle that knows its own area and perimeter.

    Store width and height as attributes and add three methods:
        area()        width * height
        perimeter()   2 * (width + height)
        is_square()   True when width equals height

    >>> r = Rectangle(3, 4)
    >>> r.width, r.height, r.area(), r.perimeter(), r.is_square()
    (3, 4, 12, 14, False)
    """

    def __init__(self, width: float, height: float) -> None:
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

    def is_square(self) -> bool:
        raise NotImplementedError


def test_rectangle(impl: type) -> None:
    r = impl(3, 4)
    assert (r.width, r.height) == (3, 4), "store width and height as attributes"
    assert r.area() == 12, f"Rectangle(3, 4).area() should be 12, got {r.area()}"
    assert r.perimeter() == 14, f"perimeter should be 14, got {r.perimeter()}"
    assert r.is_square() is False, "Rectangle(3, 4) is not a square"
    assert impl(5, 5).is_square() is True, "Rectangle(5, 5) is a square"
    assert impl(0, 7).area() == 0, "a zero-width rectangle has area 0"
    small, big = impl(1, 2), impl(10, 20)
    assert (small.area(), big.area()) == (2, 200), "each object keeps its own sizes"


def check_rectangle() -> None:
    report("1. Rectangle", test_rectangle, Rectangle)


# --- Exercise 2 -------------------------------------------------------------

class BankAccount:
    """A bank account whose balance can be read but not assigned directly.

    - BankAccount(owner, balance=0.0) stores the owner and starting balance.
    - balance is a read-only @property: reading works, `acct.balance = 5`
      raises AttributeError (a property without a setter does that for you).
    - deposit(amount) and withdraw(amount) change the balance and return the
      new balance. Both raise ValueError when amount <= 0, and withdraw also
      raises ValueError when amount is more than the balance.

    >>> acct = BankAccount("ana", 100)
    >>> acct.deposit(50), acct.withdraw(30), acct.balance
    (150, 120, 120)
    """

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        raise NotImplementedError

    @property
    def balance(self) -> float:
        raise NotImplementedError

    def deposit(self, amount: float) -> float:
        raise NotImplementedError

    def withdraw(self, amount: float) -> float:
        raise NotImplementedError


def test_bank_account(impl: type) -> None:
    acct = impl("ana", 100)
    assert acct.owner == "ana", "store the owner as an attribute"
    assert acct.balance == 100, f"starting balance should be 100, got {acct.balance}"
    assert acct.deposit(50) == 150, "deposit(50) should return the new balance 150"
    assert acct.withdraw(30) == 120, "withdraw(30) should return the new balance 120"
    assert acct.balance == 120, f"balance should now be 120, got {acct.balance}"
    assert impl("bo").balance == 0, "the balance should default to 0"
    for bad in (0, -5):
        try:
            acct.deposit(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"deposit({bad}) should raise ValueError")
    try:
        acct.withdraw(500)
    except ValueError:
        pass
    else:
        raise AssertionError("withdrawing more than the balance should raise")
    assert acct.balance == 120, "a failed withdraw must not change the balance"
    try:
        acct.balance = 1_000_000
    except AttributeError:
        pass
    else:
        raise AssertionError("balance should be read-only (no setter)")


def check_bank_account() -> None:
    report("2. BankAccount", test_bank_account, BankAccount)


# --- Exercise 3 -------------------------------------------------------------

class Vector:
    """A 2D vector that works with Python's operators.

    Store x and y, then implement these dunder methods:
        Vector(1, 2) == Vector(1, 2)     True              __eq__
        repr(Vector(1, 2))               'Vector(1, 2)'    __repr__
        Vector(1, 2) + Vector(3, 4)      Vector(4, 6)      __add__
        Vector(1, 2) * 3                 Vector(3, 6)      __mul__
        abs(Vector(3, 4))                5.0               __abs__

    When the other operand is not a Vector (or, for *, not a number), return
    the special value NotImplemented: Python then raises TypeError for you,
    and Vector(1, 2) == (1, 2) is simply False.
    """

    def __init__(self, x: float, y: float) -> None:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __add__(self, other: "Vector") -> "Vector":
        raise NotImplementedError

    def __mul__(self, factor: float) -> "Vector":
        raise NotImplementedError

    def __abs__(self) -> float:
        raise NotImplementedError


def test_vector(impl: type) -> None:
    a, b = impl(1, 2), impl(3, 4)
    assert (a.x, a.y) == (1, 2), "store x and y as attributes"
    assert a == impl(1, 2), "two vectors with the same x and y should be =="
    assert a != b, "Vector(1, 2) and Vector(3, 4) should not be equal"
    assert repr(a) == "Vector(1, 2)", f"repr should be 'Vector(1, 2)', got {a!r}"
    assert a + b == impl(4, 6), f"Vector(1, 2) + Vector(3, 4) gave {a + b!r}"
    assert a * 3 == impl(3, 6), f"Vector(1, 2) * 3 gave {a * 3!r}"
    assert abs(b) == 5.0, f"abs(Vector(3, 4)) should be 5.0, got {abs(b)}"
    assert (a == (1, 2)) is False, "comparing with a tuple should give False"
    try:
        a + 5
    except TypeError:
        pass
    else:
        raise AssertionError("Vector + 5 should raise TypeError")
    assert (a.x, a.y) == (1, 2), "operators must return new vectors, not mutate"


def check_vector() -> None:
    report("3. Vector", test_vector, Vector)


# --- Exercise 4 -------------------------------------------------------------

@dataclass(frozen=True, order=True)
class Version:
    """A version number like 1.10.2 that sorts the right way.

    The fields and order=True are given, so versions already compare field by
    field: Version(1, 10, 0) > Version(1, 9, 9). Add two methods:
      - from_string(text): a @classmethod that parses "1.10.2" into
        Version(1, 10, 2). A missing patch part means 0, so "2.0" gives
        Version(2, 0, 0). Anything without 2 or 3 parts raises ValueError.
        Return cls(...), not Version(...), so subclasses get their own type.
      - __str__: str(Version(1, 10, 2)) == "1.10.2".
    """

    major: int
    minor: int
    patch: int = 0

    @classmethod
    def from_string(cls, text: str) -> Self:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


def test_version(impl: type) -> None:
    v = impl.from_string("1.10.2")
    assert v == impl(1, 10, 2), f'from_string("1.10.2") gave {v!r}'
    assert impl.from_string("2.0") == impl(2, 0, 0), '"2.0" should mean 2.0.0'
    assert str(v) == "1.10.2", f"str() should be '1.10.2', got {str(v)!r}"
    assert str(impl(3, 1)) == "3.1.0", "str() should always show three parts"
    texts = ["1.10.0", "1.9.3", "1.2", "0.9.9"]
    ordered = [str(x) for x in sorted(impl.from_string(t) for t in texts)]
    expected = ["0.9.9", "1.2.0", "1.9.3", "1.10.0"]
    assert ordered == expected, f"sorted versions came out as {ordered}"
    for bad in ("1", "1.2.3.4", "one.two"):
        try:
            impl.from_string(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"from_string({bad!r}) should raise ValueError")


def check_version() -> None:
    report("4. Version.from_string", test_version, Version)


def main() -> None:
    check_rectangle()
    check_bank_account()
    check_vector()
    check_version()


if __name__ == "__main__":
    main()
