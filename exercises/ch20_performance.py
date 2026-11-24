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


# --- Exercise 2 -------------------------------------------------------------

def common_words(first: list[str], second: list[str]) -> list[str]:
    """Return the words of `first` that also appear in `second`.

    Keep the order of `first` and list each word once:
        common_words(["the", "cat", "sat", "on", "the", "mat"],
                     ["mat", "the", "dog"])  ->  ["the", "mat"]

    `word in second` scans the whole list every time, which is O(n) per
    word. Build a set from `second` once, before the loop, and look words
    up in that. The test counts how often `second` is read and searched.
    """
    raise NotImplementedError


class CountingList(list[str]):
    """Test helper: a list that counts loops over it and `in` checks on it."""

    def __init__(self, items: Iterable[str]) -> None:
        super().__init__(items)
        self.loops = 0
        self.searches = 0

    def __iter__(self) -> Iterator[str]:
        self.loops += 1
        return super().__iter__()

    def __contains__(self, item: object) -> bool:
        self.searches += 1
        return super().__contains__(item)


def test_common_words(impl: Callable[[list[str], list[str]], list[str]]) -> None:
    first = ["the", "cat", "sat", "on", "the", "mat"]
    second = CountingList(["mat", "the", "dog"])
    got = impl(first, second)
    assert got == ["the", "mat"], f"expected ['the', 'mat'], got {got}"
    assert second.searches == 0, (
        f"`in` was used on the list {second.searches} times: use a set instead"
    )
    assert second.loops == 1, (
        f"the second list was read {second.loops} times; build the set once"
    )
    got = impl(["a", "b"], CountingList([]))
    assert got == [], f"nothing in common should give [], got {got}"


def check_common_words() -> None:
    report("2. common_words", test_common_words, common_words)


def main() -> None:
    check_has_duplicates()
    check_common_words()


if __name__ == "__main__":
    main()
