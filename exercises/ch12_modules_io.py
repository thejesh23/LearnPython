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

import json
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


# --- Exercise 2 -------------------------------------------------------------

def write_scores(path: Path, scores: dict[str, int]) -> None:
    """Write one "name: score" line per player to `path`, best score first.

    Players with the same score are sorted by name. Every line ends with a
    newline, and no players means an empty file. Create any missing parent
    folders first (path.parent.mkdir with parents=True, exist_ok=True), and
    write with encoding="utf-8" so names like "zoë" work everywhere.

    write_scores(p, {"bo": 20, "cy": 30, "ana": 20}) writes:
        cy: 30
        ana: 20
        bo: 20
    """
    raise NotImplementedError


def test_write_scores(impl: Callable[[Path, dict[str, int]], None]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "reports" / "2026" / "scores.txt"
        impl(target, {"bo": 20, "cy": 30, "ana": 20, "zoë": 5})
        assert target.exists(), "the file (and its folders) should be created"
        text = target.read_text(encoding="utf-8")
        expected = "cy: 30\nana: 20\nbo: 20\nzoë: 5\n"
        assert text == expected, f"file holds {text!r}, expected {expected!r}"
        impl(target, {"solo": 1})
        text = target.read_text(encoding="utf-8")
        assert text == "solo: 1\n", f"writing again should replace the file: {text!r}"
        impl(target, {})
        text = target.read_text(encoding="utf-8")
        assert text == "", f"no players should give an empty file, got {text!r}"


def check_write_scores() -> None:
    report("2. write_scores", test_write_scores, write_scores)


# --- Exercise 3 -------------------------------------------------------------

def load_settings(path: Path, defaults: dict[str, Any]) -> dict[str, Any]:
    """Load JSON settings from `path` on top of `defaults`.

    - If the file does not exist, return a copy of defaults.
    - Otherwise return defaults updated with the values from the file (the
      file wins), e.g. {"theme": "light", "size": 12} plus a file holding
      {"theme": "dark"} gives {"theme": "dark", "size": 12}.
    - Never change the defaults dict you were given.
    - A file that is not valid JSON raises json.JSONDecodeError; let it.
    """
    raise NotImplementedError


def test_load_settings(impl: Callable[[Path, dict[str, Any]], Any]) -> None:
    defaults = {"theme": "light", "size": 12, "plugins": []}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "settings.json"
        got = impl(path, defaults)
        assert got == defaults, f"a missing file should give the defaults, got {got}"
        assert got is not defaults, "return a copy, not the defaults dict itself"
        path.write_text(json.dumps({"theme": "dark", "plugins": ["git"]}))
        got = impl(path, defaults)
        expected = {"theme": "dark", "size": 12, "plugins": ["git"]}
        assert got == expected, f"expected {expected}, got {got}"
        assert defaults["theme"] == "light", "the defaults dict must not change"
        path.write_text("{not json")
        try:
            impl(path, defaults)
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError("invalid JSON should raise json.JSONDecodeError")


def check_load_settings() -> None:
    report("3. load_settings", test_load_settings, load_settings)


def main() -> None:
    check_count_lines()
    check_write_scores()
    check_load_settings()


if __name__ == "__main__":
    main()
