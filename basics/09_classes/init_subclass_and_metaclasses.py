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


def main() -> None:
    class_decorator_demo()
    print()
    registry_demo()


if __name__ == "__main__":
    main()
