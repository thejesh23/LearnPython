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

import importlib
import sys
import tempfile
import tomllib
from collections.abc import Iterator
from contextlib import contextmanager
from importlib import metadata
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


PYPROJECT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "greetkit"
version = "0.1.0"
description = "Friendly greetings"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8"]

[project.scripts]
greet = "greetkit.cli:main"
"""


def pyproject_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_files(root, FILES | {"pyproject.toml": PYPROJECT})
        # tomllib only reads TOML; open the file in binary mode.
        with open(root / "pyproject.toml", "rb") as f:
            config = tomllib.load(f)
    project = config["project"]
    print(f"name={project['name']} version={project['version']}")
    print(f"needs Python {project['requires-python']}")
    print(f"dependencies: {project['dependencies']}")
    print(f"extras: {project['optional-dependencies']}")
    print(f"built by: {config['build-system']['build-backend']}")


@contextmanager
def importable(folder: Path) -> Iterator[None]:
    """Let `folder` be imported from, then undo it so nothing leaks."""
    sys.path.insert(0, str(folder))
    try:
        yield
    finally:
        sys.path.remove(str(folder))
        for name in [m for m in sys.modules if m.split(".")[0] == "greetkit"]:
            del sys.modules[name]


def import_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        write_files(Path(tmp), FILES)
        with importable(Path(tmp)):
            import greetkit

            print(greetkit.greet("  ada   lovelace "))
            print(f"greetkit.__version__ = {greetkit.__version__}")
            # `from greetkit import *` copies only the names in __all__.
            namespace: dict[str, object] = {}
            exec("from greetkit import *", namespace)
            public = sorted(k for k in namespace if not k.startswith("__"))
            print(f"star-import gives: {public}")
            # Internals are still reachable if you ask for them by path.
            from greetkit._text import tidy

            print(f"internal helper works too: {tidy('grace  hopper')}")
    print(f"cleaned up: {'greetkit' not in sys.modules}")


def run_entry_point(target: str, argv: list[str]) -> int:
    # "greetkit.cli:main" means: import greetkit.cli, call its main().
    # This is what the `greet` script that pip creates does for you.
    module_name, func_name = target.split(":")
    func = getattr(importlib.import_module(module_name), func_name)
    old_argv, sys.argv = sys.argv, ["greet", *argv]
    try:
        return func()
    finally:
        sys.argv = old_argv


def entry_point_demo() -> None:
    config = tomllib.loads(PYPROJECT)
    with tempfile.TemporaryDirectory() as tmp:
        write_files(Path(tmp), FILES)
        with importable(Path(tmp)):
            for command, target in config["project"]["scripts"].items():
                print(f"$ {command} ada linus   # runs {target}")
                code = run_entry_point(target, ["ada", "linus"])
                print(f"exit code {code}")
    # Installed packages register their commands the same way.
    scripts = metadata.entry_points(group="console_scripts")
    names = sorted(ep.name for ep in scripts)[:3]
    print(f"some installed console scripts: {names or 'none'}")


def main() -> None:
    layout_demo()
    print()
    pyproject_demo()
    print()
    import_demo()
    print()
    entry_point_demo()


if __name__ == "__main__":
    main()
