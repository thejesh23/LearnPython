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


def main() -> None:
    get_demo()


if __name__ == "__main__":
    main()
