"""Customising class creation: class decorators, `__init_subclass__`, metaclasses.

Sometimes you want code to run when a *class* is defined, not when an
instance is made: to register plugins, to check that a subclass filled in what
it must, or to add methods automatically. Python offers three tools, from
simplest to most powerful:

    class decorator     a function that receives the finished class and
                        returns it (possibly modified); affects one class
    __init_subclass__   a hook on a base class that runs for every subclass;
                        the standard way to build plugin registries
    metaclass           the class of a class; controls class creation itself

Prefer them in that order. Almost everything people once used metaclasses for
is now done more simply with the first two. Metaclasses remain for framework
authors (ORMs, enum, abc), and they come with sharp edges.
"""

from typing import Any


def auto_repr(cls: type) -> type:
    """Give cls a __repr__ that lists the instance's attributes."""

    def __repr__(self: Any) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({fields})"

    cls.__repr__ = __repr__  # type: ignore[method-assign]
    return cls  # a class decorator must return the class (or a replacement)


@auto_repr
class Book:
    def __init__(self, title: str, pages: int) -> None:
        self.title = title
        self.pages = pages


def class_decorator_demo() -> None:
    # @auto_repr above is exactly: Book = auto_repr(Book)
    print(Book("Dune", 412))
    # @dataclass, @functools.total_ordering and @enum.unique are all class
    # decorators from the standard library.


class Exporter:
    registry: dict[str, type["Exporter"]] = {}

    def __init_subclass__(cls, /, fmt: str, **kwargs: Any) -> None:
        # Runs once for each subclass, right after its class body executes.
        # Keyword arguments in the class line (fmt="csv") arrive here.
        super().__init_subclass__(**kwargs)
        cls.fmt = fmt
        Exporter.registry[fmt] = cls

    @classmethod
    def for_format(cls, fmt: str) -> "Exporter":
        return cls.registry[fmt]()

    def export(self, rows: list[dict[str, Any]]) -> str:
        raise NotImplementedError


class CsvExporter(Exporter, fmt="csv"):
    def export(self, rows: list[dict[str, Any]]) -> str:
        header = ",".join(rows[0])
        lines = [",".join(str(v) for v in row.values()) for row in rows]
        return "\n".join([header, *lines])


class MarkdownExporter(Exporter, fmt="md"):
    def export(self, rows: list[dict[str, Any]]) -> str:
        def row(cells: list[str]) -> str:
            return "| " + " | ".join(cells) + " |"

        lines = [row(list(rows[0])), row(["---"] * len(rows[0]))]
        lines += [row([str(v) for v in r.values()]) for r in rows]
        return "\n".join(lines)


def registry_demo() -> None:
    # Defining a subclass was enough to register it: no list to keep updated.
    print(f"registered formats: {sorted(Exporter.registry)}")
    rows = [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41}]
    for fmt in ("csv", "md"):
        print(f"--- {fmt} ---")
        print(Exporter.for_format(fmt).export(rows))


class Command:
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Fail when the class is *defined*, not later when someone uses it.
        if not isinstance(cls.__dict__.get("name"), str):
            raise TypeError(f"{cls.__name__} must set a class attribute 'name'")


class Greet(Command):
    name = "greet"


def subclass_check_demo() -> None:
    print(f"Greet is a valid command named {Greet.name!r}")
    try:
        class Broken(Command):  # forgot name
            pass
    except TypeError as exc:
        print(f"TypeError while defining the class: {exc}")


class CountingMeta(type):
    """A metaclass: its instances are classes."""

    created: list[str] = []

    def __new__(
        mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> "CountingMeta":
        CountingMeta.created.append(name)
        return super().__new__(mcls, name, bases, namespace)


class Model(metaclass=CountingMeta):
    pass


class Customer(Model):  # the metaclass is inherited by subclasses
    pass


class OtherMeta(type):
    pass


class Widget(metaclass=OtherMeta):
    pass


def metaclass_demo() -> None:
    # Every class is an instance of a metaclass; normally that is `type`.
    print(f"type(42) is int: {type(42) is int}; type(int) is type: {type(int) is type}")

    # type(name, bases, namespace) builds a class at runtime, which is what
    # the class statement does for you behind the scenes.
    Dog = type("Dog", (), {"sound": lambda self: "woof"})
    print(f"a class built by type(): {Dog.__name__}, says {Dog().sound()}")

    print(f"CountingMeta saw: {CountingMeta.created}")
    print(f"type(Customer) is CountingMeta: {type(Customer) is CountingMeta}")

    # The sharp edge: a class cannot mix bases with unrelated metaclasses.
    # __init_subclass__ (stage above) did the registering job without this.
    try:
        class Both(Model, Widget):
            pass
    except TypeError as exc:
        print(f"TypeError: {str(exc).splitlines()[0]}")


def main() -> None:
    class_decorator_demo()
    print()
    registry_demo()
    print()
    subclass_check_demo()
    print()
    metaclass_demo()


if __name__ == "__main__":
    main()
