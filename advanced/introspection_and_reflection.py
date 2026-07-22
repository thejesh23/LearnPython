"""Introspection — asking objects about themselves at runtime.

`getattr`/`setattr`/`hasattr` work with attribute *names as strings*, which is
how plugin loaders, serialisers, and CLI dispatchers turn data into calls.
`inspect` goes further: signatures, source, the call stack, class hierarchies.

Dynamic attribute access is powerful and easy to abuse. If a name comes from
user input, validate it against an allow-list — `getattr(obj, user_input)` is
an arbitrary-attribute read.
"""

import inspect


class Service:
    """A tiny dispatcher built entirely on introspection."""

    version = "1.0"

    def cmd_hello(self, name: str = "world") -> str:
        """Greet someone."""
        return f"hello {name}"

    def cmd_add(self, a: int, b: int = 0) -> int:
        """Add two numbers."""
        return a + b

    def _private(self) -> None: ...

    def dispatch(self, command: str, *args) -> object:
        handler = getattr(self, f"cmd_{command}", None)
        if handler is None or not callable(handler):
            raise ValueError(f"unknown command {command!r}")
        return handler(*args)

    def commands(self) -> dict[str, str]:
        return {
            name.removeprefix("cmd_"): (inspect.getdoc(member) or "").splitlines()[0]
            for name, member in inspect.getmembers(self, inspect.ismethod)
            if name.startswith("cmd_")
        }


def main() -> None:
    svc = Service()
    print(f"commands: {svc.commands()}")
    print(f"dispatch('hello', 'Ada') -> {svc.dispatch('hello', 'Ada')}")
    print(f"dispatch('add', 2, 3)    -> {svc.dispatch('add', 2, 3)}")

    # Attribute access by name.
    print(f"getattr version -> {getattr(svc, 'version')}")
    setattr(svc, "version", "1.1")
    print(f"after setattr   -> {svc.version}")
    print(f"hasattr('nope') -> {hasattr(svc, 'nope')}, default -> {getattr(svc, 'nope', 'fallback')}")

    # Signatures: parameter names, defaults, annotations.
    sig = inspect.signature(svc.cmd_add)
    print(f"signature: {sig}")
    for name, param in sig.parameters.items():
        print(f"  {name}: annotation={param.annotation.__name__} default={param.default!r}")
    bound = sig.bind(5)
    bound.apply_defaults()
    print(f"bound arguments: {bound.arguments}")

    # Classification helpers.
    print(f"isfunction(Service.cmd_add) = {inspect.isfunction(Service.cmd_add)}")
    print(f"ismethod(svc.cmd_add)       = {inspect.ismethod(svc.cmd_add)}")
    print(f"isclass(Service)            = {inspect.isclass(Service)}")

    # Where am I? Useful for logging decorators.
    def who_called_me() -> str:
        return inspect.stack()[1].function

    print(f"caller of who_called_me: {who_called_me()}")

    # dir() and vars() round out the picture.
    print(f"public attributes: {[n for n in dir(svc) if not n.startswith('_')]}")
    print(f"instance vars: {vars(svc)}")


if __name__ == "__main__":
    main()
