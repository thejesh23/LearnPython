"""Practice: the operating system and the command line (chapter 17).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch17_os_and_command_line.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch17_os_and_command_line.py: try first, peek second.
The lessons for this chapter are in basics/17_os_and_command_line/.
"""

import argparse
import contextlib
import io
import tempfile
from collections.abc import Callable
from collections.abc import Mapping
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

def env_settings(environ: Mapping[str, str], prefix: str) -> dict[str, str]:
    """Collect the environment variables that start with `prefix`.

    Return them as a dict whose keys have the prefix removed and are in
    lower case. Values stay exactly as they are (always strings).

        env_settings({"APP_PORT": "80", "APP_DEBUG": "1", "HOME": "/home/ada"},
                     "APP_")  ->  {"port": "80", "debug": "1"}

    A real program would call env_settings(os.environ, "APP_"). Taking the
    mapping as a parameter keeps the function easy to test.
    """
    raise NotImplementedError


def test_env_settings(impl: Callable[[Mapping[str, str], str], dict[str, str]]) -> None:
    environ = {
        "APP_PORT": "8080",
        "APP_DEBUG": "yes",
        "APP_LOG_LEVEL": "info",
        "HOME": "/home/ada",
        "MYAPP_PORT": "1",
    }
    got = impl(environ, "APP_")
    expected = {"port": "8080", "debug": "yes", "log_level": "info"}
    assert got == expected, f"expected {expected}, got {got}"
    assert "APP_PORT" in environ, "the environ mapping must not change"
    got = impl(environ, "NOPE_")
    assert got == {}, f"no matching variables should give {{}}, got {got}"


def check_env_settings() -> None:
    report("1. env_settings", test_env_settings, env_settings)


# --- Exercise 2 -------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the parser for a `resize` tool and return it (do not parse yet).

    The tool is used like this:
        resize photo.jpg
        resize photo.jpg --width 300 --quality high --dry-run

    It needs:
      image        positional, required
      --width      converted to int, default 800
      --quality    one of "low", "medium", "high"; default "medium"
      --dry-run    a flag: False when absent, True when given
                   (argparse stores it as args.dry_run)

    Use prog="resize" so error messages name the tool.
    """
    raise NotImplementedError


def test_build_parser(impl: Callable[[], argparse.ArgumentParser]) -> None:
    parser = impl()
    assert isinstance(parser, argparse.ArgumentParser), "return the parser itself"
    # Bad input makes argparse print to stderr; keep the report tidy.
    with contextlib.redirect_stderr(io.StringIO()):
        args = parser.parse_args(["photo.jpg"])
        got = (args.image, args.width, args.quality, args.dry_run)
        want = ("photo.jpg", 800, "medium", False)
        assert got == want, f"defaults: expected {want}, got {got}"
        args = parser.parse_args(
            ["--quality", "high", "cat.png", "--width", "300", "--dry-run"]
        )
        got = (args.image, args.width, args.quality, args.dry_run)
        want = ("cat.png", 300, "high", True)
        assert got == want, f"all options: expected {want}, got {got}"
        for bad in (["a.jpg", "--width", "wide"], ["a.jpg", "--quality", "ultra"], []):
            try:
                parser.parse_args(bad)
            except SystemExit as exit_:
                assert exit_.code == 2, f"{bad} should exit with code 2"
            else:
                raise AssertionError(f"{bad} should be rejected by argparse")


def check_build_parser() -> None:
    report("2. build_parser", test_build_parser, build_parser)


# --- Exercise 3 -------------------------------------------------------------

def find_files(root: Path, suffix: str, skip: set[str]) -> list[str]:
    """List the files under `root` whose names end in `suffix`.

    - Look in every subfolder, however deep.
    - Do not look inside any folder whose name is in `skip` (such as ".git"
      or "venv"), wherever it appears in the tree.
    - Only files count: a folder called "notes.py" is not a match.
    - Return paths relative to root, written with "/" (Path.as_posix()),
      sorted alphabetically: ["a.py", "pkg/b.py", "pkg/sub/c.py"].

    os.walk lets you prune folders by removing names from its `dirs` list
    in place; Path.rglob plus a check on each path's parts works too.
    """
    raise NotImplementedError


def test_find_files(impl: Callable[[Path, str, set[str]], list[str]]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name in (
            "a.py", "README.md", "pkg/b.py", "pkg/sub/c.py", "pkg/sub/data.json",
            ".git/hooks/pre.py", "venv/lib/site.py", "pkg/.git/x.py",
            "notes.py/inner.txt",
        ):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x\n")
        got = impl(root, ".py", {".git", "venv"})
        expected = ["a.py", "pkg/b.py", "pkg/sub/c.py"]
        assert got == expected, f"expected {expected}, got {got}"
        got = impl(root, ".py", set())
        expected = [
            ".git/hooks/pre.py", "a.py", "pkg/.git/x.py", "pkg/b.py",
            "pkg/sub/c.py", "venv/lib/site.py",
        ]
        assert got == expected, f"with nothing skipped: expected {expected}, got {got}"
        got = impl(root, ".json", {"sub"})
        assert got == [], f"data.json is inside a skipped folder, got {got}"


def check_find_files() -> None:
    report("3. find_files", test_find_files, find_files)


def main() -> None:
    check_env_settings()
    check_build_parser()
    check_find_files()


if __name__ == "__main__":
    main()
