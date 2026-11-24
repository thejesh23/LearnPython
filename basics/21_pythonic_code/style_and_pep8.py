"""Style and PEP 8 — writing code that other people (and future you) can read.

PEP 8 is Python's style guide. Code is read far more often than it is
written, so a shared style means anyone can open any Python file and find
their way around. The main points:

    naming     snake_case functions and variables, PascalCase classes,
               UPPER_CASE constants, a leading _ for "internal"
    layout     4-space indents, spaces around = and after commas, two blank
               lines between top-level definitions, short lines
    imports    one per line, at the top, grouped: standard library, then
               third-party, then your own modules, a blank line between
    docstrings a triple-quoted summary line on every public function,
               class and module (PEP 257)

Nobody checks these by hand any more. The usual tools (installed with pip,
not part of the standard library):

    ruff    a very fast linter: unused imports, bad names, likely bugs,
            import order. `ruff check .`  (`ruff check --fix .` repairs many)
    black   a formatter: rewrites layout so you never argue about it again.
            `black .`  (ruff also has a formatter: `ruff format .`)
    mypy    a type checker: reads your type hints and finds mismatches
            before the code runs. `mypy yourfile.py`
"""

import inspect
import keyword
import re
import sys


# BEFORE: it works, but every line makes the reader stop and decode it.
def CalcStats( l,Flag = False ):
    t=0;n=0;M=None
    for i in range(len(l)):
        if l[i]!=None :
            t=t+l[i];n=n+1
            if M==None or l[i]>M : M=l[i]
    if Flag==True: return (t/n if n>0 else 0,M)
    else : return t/n if n>0 else 0


# AFTER: same behaviour, PEP 8 names and layout, a docstring, type hints.
def mean_and_max(
    values: list[float | None], *, include_max: bool = False
) -> float | tuple[float, float | None]:
    """Average the values that are not None, optionally with the maximum.

    Returns 0 for the mean when there is nothing to average.
    """
    present = [v for v in values if v is not None]
    mean = sum(present) / len(present) if present else 0
    if include_max:
        return mean, max(present, default=None)
    return mean


def before_after_demo() -> None:
    samples: list[list[float | None]] = [[3, None, 9, 6], [], [None, 2.5]]
    for data in samples:
        old = CalcStats(data, True)
        new = mean_and_max(data, include_max=True)
        print(f"{data!s:<18} old={old!s:<10} new={new!s:<10} same: {old == new}")
    # What changed: descriptive names; `is not None` instead of `!= None`;
    # no semicolons or one-line ifs; a keyword-only flag so callers write
    # include_max=True rather than a mysterious positional True; and the
    # loop over range(len(...)) became a comprehension.


NAMING_RULES = {
    "function": re.compile(r"_?[a-z][a-z0-9_]*"),  # snake_case
    "variable": re.compile(r"_?[a-z][a-z0-9_]*"),
    "class": re.compile(r"_?[A-Z][a-zA-Z0-9]*"),  # PascalCase
    "constant": re.compile(r"_?[A-Z][A-Z0-9_]*"),  # UPPER_CASE
}


def check_name(kind: str, name: str) -> str:
    """Return "ok" or a short complaint, like a linter would."""
    if keyword.iskeyword(name):
        return "is a keyword"
    if not NAMING_RULES[kind].fullmatch(name):
        return f"not a good {kind} name"
    if len(name) == 1 and name in "lOI":
        return "looks like 1 or 0"  # PEP 8 bans these three on their own
    return "ok"


def naming_demo() -> None:
    examples = [
        ("function", "calc_stats"), ("function", "CalcStats"),
        ("class", "ShoppingCart"), ("class", "shopping_cart"),
        ("constant", "MAX_RETRIES"), ("constant", "maxRetries"),
        ("variable", "l"), ("variable", "_cache"),
    ]
    for kind, name in examples:
        print(f"  {kind:<9} {name:<14} {check_name(kind, name)}")


def import_group(line: str) -> int:
    """0 standard library, 1 third-party, 2 our own package, 3 relative."""
    module = line.split()[1]
    if module.startswith("."):
        return 3
    top = module.split(".")[0]
    if top in sys.stdlib_module_names:  # the full list ships with Python
        return 0
    return 2 if top == "myapp" else 1


def sort_imports(lines: list[str]) -> list[str]:
    """Group; inside a group put plain imports first, then sort by module."""

    def key(line: str) -> tuple[int, bool, str]:
        return import_group(line), line.startswith("from"), line.split()[1]

    result: list[str] = []
    for line in sorted(lines, key=key):
        if result and import_group(result[-1]) != import_group(line):
            result.append("")  # a blank line between groups
        result.append(line)
    return result


def imports_demo() -> None:
    messy = [
        "import requests",
        "from myapp.models import User",
        "import os",
        "from . import helpers",
        "import json",
        "from pathlib import Path",
        "import numpy as np",
    ]
    # This is what ruff's "I" rules (isort) do for you automatically.
    print("sorted imports:")
    for line in sort_imports(messy):
        print(f"  {line}" if line else "")


def shipping_cost(weight_kg: float, express: bool = False) -> float:
    """Return the shipping cost in euros for a parcel.

    The first line is a one-sentence summary ending in a period. Details,
    arguments and edge cases go in the following paragraphs.

    Args:
        weight_kg: Parcel weight; must be positive.
        express: Next-day delivery, which doubles the price.

    Raises:
        ValueError: If weight_kg is not positive.
    """
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    cost = 4.0 + 1.5 * weight_kg
    return cost * 2 if express else cost


def docstring_demo() -> None:
    # A docstring is not a comment: it is stored on the object, so help(),
    # editors and documentation generators can show it.
    doc = inspect.getdoc(shipping_cost) or ""
    print(f"summary line: {doc.splitlines()[0]}")
    print(f"signature   : shipping_cost{inspect.signature(shipping_cost)}")
    print(f"cost(2.0)   : {shipping_cost(2.0)}")
    # Comments explain WHY a line is the way it is; docstrings explain WHAT
    # a function does and how to call it. Neither should repeat the code.


def main() -> None:
    before_after_demo()
    print()
    naming_demo()
    print()
    imports_demo()
    print()
    docstring_demo()


if __name__ == "__main__":
    main()
