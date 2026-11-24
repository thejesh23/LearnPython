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

import re
from collections.abc import Callable
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


def main() -> None:
    check_bump_version()
    check_parse_requirement()


if __name__ == "__main__":
    main()
