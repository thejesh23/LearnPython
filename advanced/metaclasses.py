"""Metaclasses — classes that create classes.

`class Foo: ...` is roughly `Foo = type('Foo', bases, namespace)`. A metaclass
replaces `type` in that call, so it can inspect or rewrite a class *at
definition time*: registering subclasses, validating required methods,
injecting slots, enforcing naming.

The honest advice: most jobs people reach for a metaclass to do are better
served by `__init_subclass__` (3.6+) or a class decorator, both of which are
far easier to read. Know metaclasses because ORMs and serialisation libraries
use them, not because your code needs one.
"""


class RegistryMeta(type):
    """Collect every concrete subclass in a registry as it is defined."""

    registry: dict[str, type] = {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace)
        if bases:  # skip the base class itself
            key = name.lower().removesuffix("handler")
            mcls.registry[key] = cls
        return cls


class Handler(metaclass=RegistryMeta):
    def handle(self) -> str:
        raise NotImplementedError


class JsonHandler(Handler):
    def handle(self) -> str:
        return "json"


class XmlHandler(Handler):
    def handle(self) -> str:
        return "xml"


class InterfaceMeta(type):
    """Refuse to define a class that forgets a required method."""

    required = ("save", "load")

    def __new__(mcls, name, bases, namespace, **kwargs):
        if bases:
            missing = [m for m in mcls.required if m not in namespace]
            if missing:
                raise TypeError(f"{name} is missing {missing}")
        return super().__new__(mcls, name, bases, namespace)


class Storage(metaclass=InterfaceMeta):
    pass


class FileStorage(Storage):
    def save(self) -> None: ...
    def load(self) -> None: ...


class PluginBase:
    """The modern alternative: __init_subclass__, no metaclass required."""

    plugins: list[type] = []

    def __init_subclass__(cls, /, priority: int = 0, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.priority = priority
        PluginBase.plugins.append(cls)


class FastPlugin(PluginBase, priority=10):
    pass


class SlowPlugin(PluginBase, priority=1):
    pass


def main() -> None:
    print(f"registry: {RegistryMeta.registry}")
    print(f"dispatch 'json' -> {RegistryMeta.registry['json']().handle()}")

    print(f"FileStorage defined fine: {FileStorage.__name__}")
    try:
        type("BrokenStorage", (Storage,), {"save": lambda self: None})
    except TypeError as exc:
        print(f"TypeError: {exc}")

    print(f"__init_subclass__ plugins: "
          f"{[(p.__name__, p.priority) for p in PluginBase.plugins]}")

    # Classes really are instances of their metaclass.
    print(f"type(JsonHandler) = {type(JsonHandler).__name__}")
    print(f"type(int) = {type(int).__name__}, type(type) = {type(type).__name__}")

    # Building a class by hand, the way the class statement does.
    Dynamic = type("Dynamic", (), {"greet": lambda self: "hi"})
    print(f"type() call built {Dynamic.__name__}: {Dynamic().greet()}")


if __name__ == "__main__":
    main()
