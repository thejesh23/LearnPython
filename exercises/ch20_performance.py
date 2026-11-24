"""Practice: performance (chapter 20).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch20_performance.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

Timings change from machine to machine, so no test here uses a stopwatch.
Instead each test checks the *shape* of a fast solution: how many times
the data is read, how many times a function really runs, whether results
arrive lazily. If those are right, the speed follows.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch20_performance.py: try first, peek second. The
lessons for this chapter are in basics/20_performance/.
"""

from collections.abc import Callable
from collections.abc import Hashable
from collections.abc import Iterable
from collections.abc import Iterator
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

def has_duplicates(items: Iterable[Hashable]) -> bool:
    """Return True if any item appears more than once.

    The slow way compares every item with every other one: O(n**2). Do it
    in one pass instead: remember the items seen so far in a set (O(1)
    lookups) and return True the moment an item is already in it.

    `items` can be any iterable, including a generator that can only be
    read once, so do not call len() on it or loop over it twice. Stopping
    early matters too: the test counts how much of the input you read.
    """
    raise NotImplementedError


def test_has_duplicates(impl: Callable[[Iterable[Hashable]], bool]) -> None:
    cases = [([], False), ([1, 2, 3], False), ([1, 2, 1], True),
             ("hello", True), (("a", "b"), False), ([0, 0.0], True)]
    for items, want in cases:
        got = impl(items)
        assert got == want, f"has_duplicates({items!r}) gave {got}, expected {want}"

    read: list[int] = []

    def stream() -> Iterator[int]:
        # 100,000 numbers; the 6th one repeats the 3rd.
        for i in range(100_000):
            read.append(i)
            yield 2 if i == 5 else i

    got = impl(stream())
    assert got is True, f"a generator with a repeat gave {got}"
    assert len(read) == 6, (
        f"the repeat is item 6, but {len(read):,} items were read: stop early"
    )


def check_has_duplicates() -> None:
    report("1. has_duplicates", test_has_duplicates, has_duplicates)


def main() -> None:
    check_has_duplicates()


if __name__ == "__main__":
    main()
