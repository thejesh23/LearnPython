"""Practice: packaging and projects (chapter 22).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch22_packaging_and_projects.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

These exercises rebuild small pieces of what pip and test runners do, using
only the standard library. Nothing is installed or downloaded.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch22_packaging_and_projects.py: try first, peek second.
The lessons for this chapter are in basics/22_packaging_and_projects/.
"""

import collections
import contextlib
import io
import json
import os.path
import re
import sys
import tempfile
import tomllib
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

def bump_version(version: str, part: str) -> str:
    """Return the next version for a release of kind `part`.

    Versions here are "MAJOR.MINOR.PATCH" (semantic versioning):
        bump_version("1.4.2", "patch")  ->  "1.4.3"   bug fixes only
        bump_version("1.4.2", "minor")  ->  "1.5.0"   new features
        bump_version("1.4.2", "major")  ->  "2.0.0"   breaking changes
    Bumping a part resets the parts after it to 0. Work with ints, not
    characters: "1.9.9" bumped by minor is "1.10.0".

    Raise ValueError for any other `part`, and for a version that is not
    exactly three whole numbers ("1.2", "1.2.x").
    """
    raise NotImplementedError


def test_bump_version(impl: Callable[[str, str], str]) -> None:
    cases = [
        ("1.4.2", "patch", "1.4.3"), ("1.4.2", "minor", "1.5.0"),
        ("1.4.2", "major", "2.0.0"), ("1.9.9", "minor", "1.10.0"),
        ("0.0.9", "patch", "0.0.10"), ("9.12.3", "major", "10.0.0"),
    ]
    for version, part, want in cases:
        got = impl(version, part)
        call = f"bump_version({version!r}, {part!r})"
        assert got == want, f"{call} gave {got!r}, not {want!r}"
    for version, part in (("1.4.2", "build"), ("1.2", "patch"), ("1.2.x", "minor")):
        try:
            impl(version, part)
        except ValueError:
            pass
        else:
            call = f"bump_version({version!r}, {part!r})"
            raise AssertionError(f"{call} should raise ValueError")


def check_bump_version() -> None:
    report("1. bump_version", test_bump_version, bump_version)


# --- Exercise 2 -------------------------------------------------------------

def parse_requirement(line: str) -> tuple[str, str] | None:
    """Split one line of requirements.txt into (name, version specifier).

        "requests>=2.31"              ->  ("requests", ">=2.31")
        "  Flask == 3.0.0   # web"    ->  ("flask", "==3.0.0")
        "typing_extensions>=4, <5"    ->  ("typing-extensions", ">=4,<5")
        "PyYAML"                      ->  ("pyyaml", "")
        "# just a comment" or ""      ->  None

    - Drop everything from "#" on, then surrounding spaces.
    - The name is letters, digits, ".", "_" and "-". pip treats "PyYAML",
      "pyyaml", "typing_extensions" and "typing-extensions" as the same
      package, so normalise it: lower case, and every run of ".", "_" or
      "-" becomes one "-" (re.sub(r"[-_.]+", "-", name)).
    - The specifier is the rest of the line with all spaces removed.
    - A line that does not start with a name, like ">=1.0", is an error:
      raise ValueError.
    """
    raise NotImplementedError


def test_parse_requirement(impl: Callable[[str], tuple[str, str] | None]) -> None:
    cases = [
        ("requests>=2.31", ("requests", ">=2.31")),
        ("  Flask == 3.0.0   # web framework", ("flask", "==3.0.0")),
        ("typing_extensions>=4, <5", ("typing-extensions", ">=4,<5")),
        ("PyYAML", ("pyyaml", "")),
        ("zope.interface~=6.0", ("zope-interface", "~=6.0")),
        ("Some__Odd-.Name!=1.0", ("some-odd-name", "!=1.0")),
        ("# just a comment", None),
        ("", None),
        ("    \n", None),
    ]
    for line, want in cases:
        got = impl(line)
        if got is not None:
            got = tuple(got)
        assert got == want, f"parse_requirement({line!r}) gave {got!r}, not {want!r}"
    try:
        impl(">=1.0")
    except ValueError:
        pass
    else:
        raise AssertionError("'>=1.0' has no package name and should raise ValueError")


def check_parse_requirement() -> None:
    report("2. parse_requirement", test_parse_requirement, parse_requirement)


# --- Exercise 3 -------------------------------------------------------------

def read_project(path: Path) -> dict[str, Any]:
    """Read the [project] table of a pyproject.toml file.

    Return a dict with exactly these keys:
        "name"          str
        "version"       str
        "dependencies"  list of str, [] if the file lists none
        "scripts"       dict from the [project.scripts] table, {} if none

    tomllib (standard library since 3.11) only reads bytes: open the file
    with "rb" and call tomllib.load(f). If there is no [project] table, or
    it has no name or version, raise ValueError. Broken TOML already raises
    tomllib.TOMLDecodeError (a kind of ValueError); let it.
    """
    raise NotImplementedError


FULL_PYPROJECT = """
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "greetkit"
version = "0.3.1"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31",
    "rich",
]

[project.scripts]
greet = "greetkit.cli:main"
"""


def test_read_project(impl: Callable[[Path], dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pyproject.toml"
        path.write_text(FULL_PYPROJECT, encoding="utf-8")
        got = impl(path)
        want = {
            "name": "greetkit", "version": "0.3.1",
            "dependencies": ["requests>=2.31", "rich"],
            "scripts": {"greet": "greetkit.cli:main"},
        }
        assert got == want, f"expected {want}, got {got}"

        path.write_text('[project]\nname = "tiny"\nversion = "1.0"\n')
        got = impl(path)
        want = {"name": "tiny", "version": "1.0", "dependencies": [], "scripts": {}}
        assert got == want, f"a minimal project: expected {want}, got {got}"

        for text in ('[tool.black]\nline-length = 88\n', '[project]\nname = "x"\n',
                     "[project\nname = "):
            path.write_text(text)
            try:
                impl(path)
            except ValueError:
                pass
            else:
                raise AssertionError(f"a file holding {text!r} should raise ValueError")


def check_read_project() -> None:
    report("3. read_project", test_read_project, read_project)


# --- Exercise 4 -------------------------------------------------------------

def load_entry_point(target: str) -> Any:
    """Find the object an entry point such as "greetkit.cli:main" names.

    This is what the `greet` command pip creates does on every run: import
    the module before the colon, then fetch the attribute after it. The
    part after the colon may be dotted, to reach inside a class:
        load_entry_point("json:dumps")                 ->  json.dumps
        load_entry_point("os.path:join")               ->  os.path.join
        load_entry_point("collections:Counter.fromkeys")
                                     ->  collections.Counter.fromkeys

    Use importlib.import_module for the module and getattr for each name
    after the colon. A target without exactly one ":" raises ValueError; a
    missing module or attribute raises whatever import_module or getattr
    raise (ModuleNotFoundError, AttributeError): let those through.
    """
    raise NotImplementedError


def test_load_entry_point(impl: Callable[[str], Any]) -> None:
    cases = [
        ("json:dumps", json.dumps),
        ("os.path:join", os.path.join),
        ("collections:Counter.fromkeys", collections.Counter.fromkeys),
        ("collections:OrderedDict", collections.OrderedDict),
    ]
    for target, want in cases:
        got = impl(target)
        assert got == want, f"{target!r} should give {want!r}, got {got!r}"
    errors = [
        ("json", ValueError), ("json:dumps:extra", ValueError),
        ("json:nope", AttributeError), ("no_such_module_lp22:main", ImportError),
    ]
    for target, kind in errors:
        try:
            impl(target)
        except kind:
            pass
        else:
            raise AssertionError(f"{target!r} should raise {kind.__name__}")


def check_load_entry_point() -> None:
    report("4. load_entry_point", test_load_entry_point, load_entry_point)


# --- Exercise 5 -------------------------------------------------------------

def run_tests(folder: Path) -> tuple[int, int]:
    """Find and run every test in `folder`; return (tests run, tests not passed).

    This is `python -m unittest discover` as a function:
        suite = unittest.TestLoader().discover(str(folder))
    finds every test*.py file and collects its TestCase methods. Run the
    suite with unittest.TextTestRunner(stream=io.StringIO()), so its report
    goes into a string instead of the screen. The result object has
    .testsRun, and lists .failures (an assert failed) and .errors (the test
    crashed); count both as not passed.
    """
    raise NotImplementedError


SAMPLE_TESTS = """
import unittest

from helper_lp22 import double


class DoubleTests(unittest.TestCase):
    def test_small(self):
        self.assertEqual(double(2), 4)

    def test_zero(self):
        self.assertEqual(double(0), 0)

    def test_wrong_on_purpose(self):
        self.assertEqual(double(3), 7)

    def test_crashes_on_purpose(self):
        double(None)
"""


def test_run_tests(impl: Callable[[Path], tuple[int, int]]) -> None:
    folders: list[str] = []
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, empty = root / "project", root / "empty"
            project.mkdir()
            empty.mkdir()
            folders += [str(project), str(empty)]
            helper = "def double(n):\n    return n * 2\n"
            (project / "helper_lp22.py").write_text(helper)
            (project / "test_lp22_double.py").write_text(SAMPLE_TESTS)
            (project / "notes.txt").write_text("not a test\n")
            with contextlib.redirect_stderr(io.StringIO()):
                got = tuple(impl(project))
                assert got == (4, 2), f"4 tests, 2 not passing; got {got}"
                (empty / "readme.txt").write_text("no tests here\n")
                got = tuple(impl(empty))
                assert got == (0, 0), f"a folder without tests gives (0, 0), got {got}"
    finally:
        # discover() put the folders on sys.path and imported modules from
        # them; undo that so nothing leaks into the rest of this file.
        sys.path[:] = [entry for entry in sys.path if entry not in folders]
        for name in ("helper_lp22", "test_lp22_double"):
            sys.modules.pop(name, None)


def check_run_tests() -> None:
    report("5. run_tests", test_run_tests, run_tests)


def main() -> None:
    check_bump_version()
    check_parse_requirement()
    check_read_project()
    check_load_entry_point()
    check_run_tests()


if __name__ == "__main__":
    main()
