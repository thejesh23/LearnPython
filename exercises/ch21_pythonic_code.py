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


def main() -> None:
    check_scoreboard()


if __name__ == "__main__":
    main()
