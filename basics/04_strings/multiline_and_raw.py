"""Triple-quoted strings, raw strings, and escape sequences.

Triple quotes (`\"\"\"` or `'''`) span lines and keep the newlines you typed.
They are also how docstrings are written — the string at the top of a module,
function, or class becomes its documentation, readable at runtime as
`__doc__`.

A raw string (`r"..."`) turns off backslash escapes. Use it for regular
expressions and Windows paths, where `\\n` should mean backslash-n, not a
newline.
"""

import textwrap


def main() -> None:
    poem = """Roses are red,
Violets are blue,
Python has triple quotes,
And so do you."""
    print(poem)
    print("-" * 40)

    # A leading backslash suppresses the first newline; textwrap.dedent
    # removes the shared indentation that the source layout added.
    indented = """\
        line one
        line two
    """
    print(textwrap.dedent(indented), end="")
    print("-" * 40)

    # Escapes inside a normal string.
    print("tab:\tafter\nnewline above, quote: \" backslash: \\")

    # Raw string: the escapes are left alone.
    pattern = r"\d+\.\d+"
    print(f"raw   = {pattern}")
    print(f"normal= {'\\d+\\.\\d+'}")
    print(f"same? {pattern == '\\d+\\.\\d+'}")

    # Where raw strings earn their keep.
    import re

    print(re.findall(r"\b\w+@\w+\.\w+\b", "mail ada@example.com or alan@x.org"))

    # This module's own docstring is just a string object.
    print(f"module docstring starts: {__doc__.splitlines()[0]!r}")


if __name__ == "__main__":
    main()
