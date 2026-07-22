"""Class decorators and mixins — composition without a metaclass.

A class decorator receives the class after it is built and returns a
replacement (usually the same object, modified). That covers most of what
people write metaclasses for — registration, injecting methods, validation —
in code anyone can read.

A mixin is a small class contributing behaviour, meant to sit *before* the base
in the MRO so its `super()` calls reach the real implementation. Keep mixins
stateless and single-purpose; a mixin with an `__init__` that does not
cooperate with `super().__init__` is a future bug.
"""

import functools


REGISTRY: dict[str, type] = {}


def register(name: str):
    """Parameterised class decorator: record the class under a name."""

    def decorator(cls: type) -> type:
        REGISTRY[name] = cls
        cls.registered_as = name
        return cls

    return decorator


def auto_repr(cls: type) -> type:
    """Give any class a repr built from its instance dict."""

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({pairs})"

    cls.__repr__ = __repr__
    return cls


def singleton(cls: type):
    """One instance per class — implemented by replacing the class with a factory."""
    instances: dict[type, object] = {}

    @functools.wraps(cls, updated=())
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class LoggingMixin:
    """Wraps whatever comes next in the MRO — cooperative by design."""

    def save(self) -> str:
        result = super().save()
        print(f"    [log] save -> {result}")
        return result


class TimestampMixin:
    def save(self) -> str:
        return f"{super().save()} at 12:00"


class Record:
    def save(self) -> str:
        return "saved"


class AuditedRecord(LoggingMixin, TimestampMixin, Record):
    """MRO: AuditedRecord -> LoggingMixin -> TimestampMixin -> Record."""


@register("json")
@auto_repr
class JsonCodec:
    def __init__(self, indent: int = 2) -> None:
        self.indent = indent


@register("csv")
@auto_repr
class CsvCodec:
    def __init__(self, delimiter: str = ",") -> None:
        self.delimiter = delimiter


@singleton
class Config:
    def __init__(self, env: str = "prod") -> None:
        self.env = env


def main() -> None:
    print("class decorators:")
    print(f"  registry: {REGISTRY}")
    print(f"  auto_repr: {JsonCodec(4)}")
    print(f"  attribute injected: {CsvCodec.registered_as}")

    print("singleton:")
    a, b = Config("dev"), Config("ignored")
    print(f"  same object: {a is b}, env stayed {b.env!r}")

    print("mixins (decorators stack bottom-up, mixins resolve left-to-right):")
    print(f"  {AuditedRecord().save()}")
    print(f"  MRO: {[c.__name__ for c in AuditedRecord.__mro__[:-1]]}")

    print("order matters — swapping the mixins changes the output:")

    class Swapped(TimestampMixin, LoggingMixin, Record):
        pass

    print(f"  {Swapped().save()}")


if __name__ == "__main__":
    main()
