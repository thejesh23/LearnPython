"""Docstrings, help() and inspect: documentation that lives inside the code.

A *docstring* is a string literal written as the first statement of a module,
function, class or method. Python keeps it on the object as `__doc__`, and
tools read it from there: `help()` in the interactive shell, editors showing a
tooltip, documentation generators, and doctest.

Conventions from PEP 257, the docstring style guide:

    - use triple double quotes, even for one line
    - the first line is a short summary ending in a period
    - for longer docstrings, a blank line, then the details

Type hints document a function too. Together with the parameter names and
defaults they form its *signature*, which `inspect.signature` can read back.
"""

import inspect
import pydoc


def area(width: float, height: float = 1.0) -> float:
    """Return the area of a rectangle.

    Both sides are in the same unit; the result is in that unit squared.
    A missing height gives a strip one unit tall.
    """
    return width * height


def no_docs(x: int) -> int:
    return x + 1


class Stack:
    """A last-in, first-out pile of items."""

    def push(self, item: object) -> None:
        """Put item on top."""


def docstring_demo() -> None:
    print(f"area.__doc__ starts: {area.__doc__.splitlines()[0]!r}")
    print(f"no_docs.__doc__ = {no_docs.__doc__!r}")
    print(f"Stack.__doc__ = {Stack.__doc__!r}")
    print(f"Stack.push.__doc__ = {Stack.push.__doc__!r}")

    # Only the *first* statement counts. A string later on is just an
    # expression that is thrown away, and a # comment is never kept.
    def late() -> None:
        x = 1  # noqa: F841
        """Not a docstring: it is not the first statement."""

    print(f"late.__doc__ = {late.__doc__!r}")


def getdoc_demo() -> None:
    # Up to Python 3.12 the raw __doc__ keeps the indentation from the source
    # file; 3.13 strips it when compiling. Either way, do not rely on it.
    print("raw __doc__:")
    for line in area.__doc__.splitlines():
        print(f"  |{line}")

    # inspect.getdoc always gives the clean version, which is what help() uses.
    print("inspect.getdoc:")
    for line in inspect.getdoc(area).splitlines():
        print(f"  |{line}")


def help_demo() -> None:
    # help(area) prints to the screen, and in a terminal it opens a pager.
    # pydoc.render_doc builds the same text as a string, which we can print
    # here without pausing the program. plaintext removes bold formatting.
    text = pydoc.render_doc(area, renderer=pydoc.plaintext)
    print(text.rstrip())
    print("-" * 40)

    # For a class, help() lists the class docstring and every method's.
    # (Only the top part is printed; the rest is boilerplate about __dict__.)
    class_text = pydoc.render_doc(Stack, renderer=pydoc.plaintext)
    for line in class_text.splitlines()[2:9]:
        print(line)


def greet(name: str, *, greeting: str = "Hello", times: int = 1) -> str:
    """Return a greeting, repeated `times` times."""
    return " ".join([f"{greeting}, {name}!"] * times)


def signature_demo() -> None:
    sig = inspect.signature(greet)
    print(f"signature: greet{sig}")
    print(f"returns:   {sig.return_annotation.__name__}")
    for param in sig.parameters.values():
        default = "required" if param.default is param.empty else repr(param.default)
        print(f"  {param.name:<9} {param.annotation.__name__:<4} "
              f"{param.kind.name:<22} {default}")

    # The type hints alone live in __annotations__ as a plain dict.
    for name, hint in greet.__annotations__.items():
        print(f"  __annotations__[{name!r}] = {hint}")

    # Hints are documentation, not enforcement: Python does not check them.
    print(f"greet(42) still runs: {greet(42)!r}")  # type: ignore[arg-type]


def main() -> None:
    docstring_demo()
    print()
    getdoc_demo()
    print()
    help_demo()
    print()
    signature_demo()


if __name__ == "__main__":
    main()
