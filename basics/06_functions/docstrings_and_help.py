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


def main() -> None:
    docstring_demo()


if __name__ == "__main__":
    main()
