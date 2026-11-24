"""Turning a folder of code into a package other people can install.

A *package* is a directory of modules with an `__init__.py`. The `__init__.py`
runs when the package is imported and decides what `from pkg import *` gives,
through a list of names called `__all__`.

To make the package *installable*, add a `pyproject.toml` next to it. That one
TOML file holds everything pip needs:

    [build-system]   which tool builds the package (setuptools, hatchling...)
    [project]        name, version, Python versions, dependencies
    [project.scripts] command-line programs to create on install

With that file in place, `python -m pip install -e .` installs the project in
"editable" mode (imports read your source folder directly, so edits show up at
once) and `python -m build` makes a wheel you could upload to PyPI.

This file builds a tiny package in a temporary folder, reads its
pyproject.toml with `tomllib` (in the standard library since 3.11), and
imports it without installing anything by putting its folder on `sys.path`.
"""

import tempfile
from pathlib import Path


FILES = {
    "greetkit/__init__.py": """\
"greetkit: friendly greetings."
from greetkit.core import greet, shout

__all__ = ["greet", "shout"]  # the public names
__version__ = "0.1.0"
""",
    "greetkit/core.py": """\
from greetkit._text import tidy


def greet(name: str) -> str:
    return f"Hello, {tidy(name)}!"


def shout(name: str) -> str:
    return greet(name).upper()
""",
    # A leading underscore marks a module as internal by convention.
    "greetkit/_text.py": """\
def tidy(name: str) -> str:
    return " ".join(name.split()).title()
""",
    "greetkit/cli.py": """\
import sys

from greetkit import greet


def main() -> int:
    for name in sys.argv[1:] or ["world"]:
        print(greet(name))
    return 0
""",
}


def write_files(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def show_tree(root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            print(f"  {path.relative_to(root).as_posix()}")


def layout_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        write_files(Path(tmp), FILES)
        print("package files:")
        show_tree(Path(tmp))
        print("greetkit/__init__.py:")
        for line in FILES["greetkit/__init__.py"].splitlines():
            print(f"  | {line}".rstrip())


def main() -> None:
    layout_demo()


if __name__ == "__main__":
    main()
