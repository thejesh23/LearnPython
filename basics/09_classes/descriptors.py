"""Descriptors — the machinery under `property`, methods and `classmethod`.

A descriptor is any object, stored as a *class* attribute, that defines one or
more of these methods:

    __get__(self, instance, owner)   called when the attribute is read
    __set__(self, instance, value)   called when it is assigned
    __set_name__(self, owner, name)  called once, when the class is created,
                                     telling the descriptor its own name

When you write `obj.attr`, Python finds `attr` on the class, sees it has
`__get__`, and returns whatever `__get__` returns instead of the object
itself. `property` is just a descriptor written in C; so are functions (that
is how `self` gets bound) and `classmethod`.

You rarely need to write one. When you do, the usual reason is a validation
rule shared by many attributes, which would otherwise need a property each.
"""

from collections.abc import Callable
from typing import Any


class Loud:
    """A minimal descriptor: reports every read."""

    def __get__(self, instance: Any, owner: type) -> str:
        if instance is None:
            # Accessed on the class itself (Robot.greeting), not an instance.
            return "<Loud descriptor>"
        return f"HELLO FROM {instance.name.upper()}"


class Robot:
    greeting = Loud()  # must live on the class, not in __init__

    def __init__(self, name: str) -> None:
        self.name = name


def get_demo() -> None:
    r = Robot("r2")
    print(f"r.greeting     -> {r.greeting}")
    print(f"Robot.greeting -> {Robot.greeting}")
    # What Python did for r.greeting, spelled out by hand:
    descriptor = Robot.__dict__["greeting"]
    print(f"by hand        -> {descriptor.__get__(r, Robot)}")


class my_property:
    """Enough of the built-in property to show how it works."""

    def __init__(self, fget: Callable[[Any], Any]) -> None:
        self.fget = fget
        self.fset: Callable[[Any, Any], None] | None = None

    def setter(self, fset: Callable[[Any, Any], None]) -> "my_property":
        self.fset = fset
        return self  # the same descriptor, now with a setter too

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance: Any, value: Any) -> None:
        if self.fset is None:
            raise AttributeError("read-only attribute")
        self.fset(instance, value)


class Celsius:
    def __init__(self, degrees: float) -> None:
        self.degrees = degrees  # goes through the setter below

    @my_property
    def degrees(self) -> float:
        return self._degrees

    @degrees.setter
    def degrees(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"{value} is below absolute zero")
        self._degrees = value


def property_demo() -> None:
    c = Celsius(20)
    c.degrees = 25
    print(f"my_property works: {c.degrees}")
    try:
        c.degrees = -300
    except ValueError as exc:
        print(f"ValueError: {exc}")
    # The real property has the same methods.
    print(f"property has __get__ and __set__: "
          f"{hasattr(property, '__get__') and hasattr(property, '__set__')}")


class Positive:
    """A number field that must be > 0. Write it once, use it everywhere."""

    def __set_name__(self, owner: type, name: str) -> None:
        # Called when the owning class is created: price = Positive() tells
        # this object its name is "price", so it needs no arguments.
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{self.public_name} must be > 0, got {value!r}")
        setattr(instance, self.private_name, value)


class Product:
    price = Positive()
    quantity = Positive()  # no copy-pasted property for each field

    def __init__(self, name: str, price: float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self) -> float:
        return self.price * self.quantity


def validated_field_demo() -> None:
    p = Product("pen", 1.5, 4)
    print(f"{p.name}: {p.quantity} x {p.price} = {p.total()}")
    print(f"stored as: {vars(p)}")
    for field, bad in (("price", -2), ("quantity", "ten")):
        try:
            setattr(p, field, bad)
        except ValueError as exc:
            print(f"ValueError: {exc}")


def main() -> None:
    get_demo()
    print()
    property_demo()
    print()
    validated_field_demo()


if __name__ == "__main__":
    main()
