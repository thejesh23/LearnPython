"""Descriptors — the protocol behind property, classmethod, and methods themselves.

Any class defining `__get__` (and optionally `__set__`/`__delete__`) is a
descriptor. Put an instance of it in a *class* body and attribute access on the
instances routes through it.

The distinction that decides everything:
  data descriptor      defines __set__ or __delete__ -> wins over the instance dict
  non-data descriptor  only __get__                  -> the instance dict wins

`property` is a data descriptor. A plain function is a non-data descriptor —
which is exactly how `obj.method` becomes a bound method.

`__set_name__` (3.6+) tells the descriptor the attribute name it was assigned
to, removing the old boilerplate of passing the name in by hand.
"""


class Typed:
    """A reusable validating attribute — the classic descriptor use case."""

    def __init__(self, expected: type) -> None:
        self.expected = expected

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # accessed on the class, not an instance
        return getattr(obj, self.private)

    def __set__(self, obj, value) -> None:
        if not isinstance(value, self.expected):
            raise TypeError(
                f"{self.name} must be {self.expected.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, self.private, value)


class Lazy:
    """Non-data descriptor: computes once, then the instance dict shadows it."""

    def __init__(self, factory) -> None:
        self.factory = factory

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"  computing {self.name} (this prints only once)")
        value = self.factory(obj)
        obj.__dict__[self.name] = value  # future lookups skip the descriptor
        return value


class Order:
    quantity = Typed(int)
    label = Typed(str)

    def __init__(self, quantity: int, label: str) -> None:
        self.quantity = quantity
        self.label = label

    @Lazy
    def total(self) -> int:
        return self.quantity * 10


def main() -> None:
    order = Order(3, "widgets")
    print(f"{order.quantity} {order.label}")

    try:
        order.quantity = "many"
    except TypeError as exc:
        print(f"TypeError: {exc}")

    print(f"total -> {order.total}")
    print(f"total -> {order.total}  (cached in __dict__: {'total' in order.__dict__})")

    # Functions are non-data descriptors; that is where bound methods come from.
    def plain(self) -> str:
        return "called"

    print(f"function has __get__: {hasattr(plain, '__get__')}")
    print(f"Order.__init__ is a {type(Order.__init__).__name__}, "
          f"order.__init__ is a {type(order.__init__).__name__}")

    # Data descriptors win over the instance dict; non-data ones do not.
    order.__dict__["quantity"] = 999
    print(f"instance dict says 999, descriptor still returns {order.quantity}")


if __name__ == "__main__":
    main()
