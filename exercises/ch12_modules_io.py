"""Practice: modules, files and I/O (chapter 12).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch12_modules_io.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch12_modules_io.py: try first, peek second. The lessons
for this chapter are in basics/12_modules_io/.
"""

import tempfile
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

def count_lines(path: Path) -> int:
    """Return how many lines in the text file at `path` are not blank.

    A line holding only spaces or tabs counts as blank. Read with
    path.read_text(encoding="utf-8") or open the file and loop over it.
    A missing file should raise FileNotFoundError (do not catch it).
    """
    raise NotImplementedError


def test_count_lines(impl: Callable[[Path], int]) -> None:
    # Every test works in a fresh temporary folder that is deleted afterwards.
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        cases = {
            "three.txt": ("one\ntwo\nthree\n", 3),
            "gaps.txt": ("one\n\n   \n\ttwo\n\n", 2),
            "no_newline.txt": ("first\nlast", 2),
            "empty.txt": ("", 0),
        }
        for name, (text, expected) in cases.items():
            (folder / name).write_text(text, encoding="utf-8")
            got = impl(folder / name)
            assert got == expected, (
                f"{text!r} has {expected} non-blank lines, got {got}"
            )
        try:
            impl(folder / "missing.txt")
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("a missing file should raise FileNotFoundError")


def check_count_lines() -> None:
    report("1. count_lines", test_count_lines, count_lines)


def main() -> None:
    check_count_lines()


if __name__ == "__main__":
    main()
