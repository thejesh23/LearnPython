"""Practice: Pythonic code (chapter 21).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch21_pythonic_code.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

Several exercises show a tempting first attempt that has a bug. Work out
why it fails before writing your own version.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch21_pythonic_code.py: try first, peek second. The
lessons for this chapter are in basics/21_pythonic_code/.
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

def scoreboard(names: list[str], scores: list[int]) -> list[str]:
    """Number the players in finishing order: ["1. Ada (90)", "2. Bo (75)"].

    names[i] scored scores[i], and the lists are already in finishing
    order. Write it without range(len(...)) or a counter variable:
    enumerate(..., start=1) numbers things, zip pairs two lists up.

    If the lists have different lengths, raise ValueError instead of
    quietly dropping the extra items. zip(..., strict=True) does exactly that.
    """
    raise NotImplementedError


def test_scoreboard(impl: Callable[[list[str], list[int]], list[str]]) -> None:
    got = impl(["Ada", "Bo", "Cy"], [90, 75, 75])
    want = ["1. Ada (90)", "2. Bo (75)", "3. Cy (75)"]
    assert got == want, f"expected {want}, got {got}"
    got = impl([], [])
    assert got == [], f"no players should give [], got {got}"
    for names, scores in ((["Ada", "Bo"], [90]), (["Ada"], [90, 75])):
        try:
            impl(names, scores)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{names} with {scores} should raise ValueError")


def check_scoreboard() -> None:
    report("1. scoreboard", test_scoreboard, scoreboard)


# --- Exercise 2 -------------------------------------------------------------

def remove_short(words: list[str], min_length: int) -> None:
    """Remove, in place, every word shorter than min_length. Return None.

    The tempting version skips words:
        for word in words:
            if len(word) < min_length:
                words.remove(word)
    Removing an item shifts the rest left, so the loop jumps over the word
    right after each one removed. Callers hold a reference to this list, so
    it must be the same list object afterwards: build the kept words and
    assign them with words[:] = ..., rather than words = ...
    """
    raise NotImplementedError


def test_remove_short(impl: Callable[[list[str], int], None]) -> None:
    words = ["a", "an", "the", "of", "to", "python", "is", "fun"]
    same = words
    result = impl(words, 3)
    assert result is None, "change the list in place and return None"
    assert words is same, "it must still be the same list object"
    want = ["the", "python", "fun"]
    assert words == want, f"expected {want}, got {words}"
    words = ["ok", "no", "no", "no"]
    impl(words, 3)
    assert words == [], f"every word was short, but {words} is left"


def check_remove_short() -> None:
    report("2. remove_short", test_remove_short, remove_short)


# --- Exercise 3 -------------------------------------------------------------

def make_multipliers(n: int) -> list[Callable[[int], int]]:
    """Return n functions; the k-th one (counting from 0) multiplies by k.

        times = make_multipliers(4)
        [f(10) for f in times]  ->  [0, 10, 20, 30]

    The tempting one-liner gives [30, 30, 30, 30]:
        return [lambda x: x * k for k in range(n)]
    Each lambda looks k up when it is *called*, and by then the loop has
    finished and k is 3. Make each function remember its own k: a default
    argument (lambda x, k=k: ...) or functools.partial both work.
    """
    raise NotImplementedError


def test_make_multipliers(impl: Callable[[int], list[Callable[[int], int]]]) -> None:
    times = impl(4)
    assert len(times) == 4, f"make_multipliers(4) gave {len(times)} functions, not 4"
    got = [f(10) for f in times]
    assert got == [0, 10, 20, 30], f"[f(10) for f in times] gave {got}"
    got = [f(1) for f in impl(3)]
    assert got == [0, 1, 2], f"make_multipliers(3) on 1 gave {got}"
    assert impl(0) == [], "make_multipliers(0) should give []"


def check_make_multipliers() -> None:
    report("3. make_multipliers", test_make_multipliers, make_multipliers)


# --- Exercise 4 -------------------------------------------------------------

def load_port(path: Path, default: int = 8000) -> int:
    """Read a port number from a one-line text file.

    - No such file: that is normal, return `default`.
    - The file holds a whole number from 1 to 65535 (spaces and a newline
      around it are fine): return it as an int.
    - Anything else is a mistake someone must fix, so raise ValueError:
      "eighty" (int() raises it for you) or 70000 (raise it yourself).

    "Errors should never pass silently." The tempting version is
        try:
            return int(path.read_text())
        except Exception:
            return default
    which hides the typo in the file. Put only the line that can raise
    FileNotFoundError inside the try, and catch only that.
    """
    raise NotImplementedError


def test_load_port(impl: Callable[..., int]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "port.txt"
        got = impl(path)
        assert got == 8000, f"a missing file should give the default 8000, got {got}"
        got = impl(path, default=5000)
        assert got == 5000, f"default=5000 with no file should give 5000, got {got}"
        path.write_text(" 8080\n")
        got = impl(path)
        assert got == 8080, f"a file holding ' 8080' should give 8080, got {got!r}"
        for bad in ("eighty", "", "70000", "0", "-1"):
            path.write_text(bad)
            try:
                got = impl(path)
            except ValueError:
                continue
            raise AssertionError(f"a file holding {bad!r} should raise ValueError")


def check_load_port() -> None:
    report("4. load_port", test_load_port, load_port)


# --- Exercise 5 -------------------------------------------------------------

def get_nested(data: Any, *keys: Any, default: Any = None) -> Any:
    """Follow keys and indexes into nested dicts and lists.

        user = {"name": "Ada", "langs": ["py", "c"]}
        data = {"users": [user]}
        get_nested(data, "users", 0, "langs", -1)   ->  "c"
        get_nested(data, "users", 3, "name")        ->  None   (no user 3)
        get_nested(data, "users", 0, "age", default=0)  ->  0

    Checking first (LBYL) gets messy: is it a dict? does the key exist? is
    it a list? is the index in range? Ask forgiveness instead (EAFP): just
    do current = current[key] for each key, and if that fails with
    KeyError, IndexError or TypeError (as in a_list["x"]), return default.
    With no keys, return data itself.

    Catch only those three. Any other error is a real bug and must reach
    the caller, so do not use a bare except or `except Exception`.
    """
    raise NotImplementedError


class Explosive(dict[str, Any]):
    """Test helper: a dict whose "boom" key has a bug behind it."""

    def __getitem__(self, key: str) -> Any:
        if key == "boom":
            raise ZeroDivisionError("a bug in the data source")
        return super().__getitem__(key)


def test_get_nested(impl: Callable[..., Any]) -> None:
    data = {"users": [{"name": "Ada", "langs": ["py", "c"]}], "count": 1}
    cases: list[tuple[tuple[Any, ...], Any]] = [
        (("users", 0, "name"), "Ada"),
        (("users", 0, "langs", -1), "c"),
        (("users", 3, "name"), None),
        (("users", "0"), None),
        (("count", "x"), None),
        (("missing",), None),
        (("users", 0, "name", 0), "A"),
        ((), data),
    ]
    for keys, want in cases:
        got = impl(data, *keys)
        assert got == want, f"get_nested(data, {keys}) gave {got!r}, expected {want!r}"
    got = impl(data, "users", 0, "age", default=0)
    assert got == 0, f"a missing key with default=0 should give 0, got {got!r}"
    try:
        impl({"source": Explosive(ok=1)}, "source", "boom")
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("an unrelated error (ZeroDivisionError) was swallowed")


def check_get_nested() -> None:
    report("5. get_nested", test_get_nested, get_nested)


def main() -> None:
    check_scoreboard()
    check_remove_short()
    check_make_multipliers()
    check_load_port()
    check_get_nested()


if __name__ == "__main__":
    main()
