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

import cProfile
import pstats
from collections.abc import Callable
from collections.abc import Hashable
from collections.abc import Iterable
from collections.abc import Iterator
from functools import wraps
from itertools import islice
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


# --- Exercise 3 -------------------------------------------------------------

def parse_readings(lines: Iterable[str]) -> Iterator[float]:
    """Turn lines of text into numbers, lazily.

    Strip each line; skip it if it is empty or starts with "#"; otherwise
    produce float(line). parse_readings(["1.5\n", "\n", "# note\n", " 2 "])
    gives 1.5 and 2.0.

    `lines` may be a huge file or an endless sensor feed, so do not build a
    list: write a generator function (with `yield`) or return a generator
    expression. Then each line is read only when the caller asks for the
    next number, and memory use stays flat however long the input is.
    """
    raise NotImplementedError


def test_parse_readings(impl: Callable[[Iterable[str]], Iterator[float]]) -> None:
    got = list(impl(["1.5\n", "\n", "# note\n", " 2 ", "-3e2", "   \n"]))
    want = [1.5, 2.0, -300.0]
    assert got == want, f"expected {want}, got {got}"

    read: list[str] = []

    def long_feed() -> Iterator[str]:
        # 100,000 lines; a real feed might never end at all.
        for n in range(1, 100_001):
            line = "# heartbeat\n" if n % 3 == 0 else f"{n}.5\n"
            read.append(line)
            yield line

    readings = impl(long_feed())
    assert iter(readings) is readings, "return an iterator (a generator), not a list"
    assert read == [], "nothing should be read before the first number is asked for"
    first = list(islice(readings, 4))
    assert first == [1.5, 2.5, 4.5, 5.5], f"the first four readings were {first}"
    assert len(read) == 5, f"5 lines give 4 readings, but {len(read)} were read"


def check_parse_readings() -> None:
    report("3. parse_readings", test_parse_readings, parse_readings)


# --- Exercise 4 -------------------------------------------------------------

def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: remember each result so repeated calls are instant.

    Keep a dict from the positional arguments (a tuple, so hashable) to the
    result. On a call, return the stored result if there is one; otherwise
    call func, store the result and return it. Two traps:
      - A result can be None, 0 or "", so test `args in cache`, not
        `if cache.get(args)`.
      - Use @functools.wraps(func) on the wrapper so it keeps func's
        __name__ and docstring.
    functools.cache does all this for real; writing it once shows how.
    """
    raise NotImplementedError


def test_memoize(impl: Callable[[Callable[..., Any]], Callable[..., Any]]) -> None:
    calls: list[tuple[int, ...]] = []

    def area(width: int, height: int) -> int:
        """Area of a rectangle."""
        calls.append((width, height))
        return width * height

    fast = impl(area)
    assert fast.__name__ == "area", "use functools.wraps to keep the name"
    assert fast.__doc__ == "Area of a rectangle.", "wraps also keeps the docstring"
    got = [fast(2, 3), fast(4, 5), fast(2, 3), fast(3, 2), fast(2, 3)]
    assert got == [6, 20, 6, 6, 6], f"results were {got}"
    assert calls == [(2, 3), (4, 5), (3, 2)], f"area really ran for {calls}"

    nothing_calls: list[int] = []

    @impl
    def find_nothing(n: int) -> None:
        nothing_calls.append(n)
        return None

    find_nothing(1)
    find_nothing(1)
    assert nothing_calls == [1], "a stored None is still a stored result"

    fib_calls = 0

    @impl
    def fib(n: int) -> int:
        nonlocal fib_calls
        fib_calls += 1
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    got = fib(25)
    assert got == 75025, f"fib(25) is 75025, got {got}"
    assert fib_calls == 26, (
        f"memoised fib(25) needs 26 real calls, not {fib_calls:,}"
    )


def check_memoize() -> None:
    report("4. memoize", test_memoize, memoize)


# --- Exercise 5 -------------------------------------------------------------

def most_called(func: Callable[[], object]) -> tuple[str, int]:
    """Profile func() and return (name, calls) of its busiest Python function.

    "Busiest" means called the most times, counting recursive calls too.
    Call counts are exact, unlike times, so they are safe to test.

        profiler = cProfile.Profile()
        profiler.runcall(func)
        stats = pstats.Stats(profiler).get_stats_profile()

    stats.func_profiles maps each function name to a record with
    .ncalls, a string such as "100" or, for recursion, "41/1" (total
    calls / outside calls: you want the first number), and .file_name,
    which is "~" for built-ins written in C such as str.split. Skip
    those: only functions written in Python count.
    """
    raise NotImplementedError


def tokenize(text: str) -> list[str]:
    return text.split()


def normalize(word: str) -> str:
    return word.lower().strip(".,")


def count_words(texts: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for text in texts:
        for word in tokenize(text):
            key = normalize(word)
            counts[key] = counts.get(key, 0) + 1
    return counts


def depth(n: int) -> int:
    return 0 if n == 0 else 1 + depth(n - 1)


def test_most_called(impl: Callable[[Callable[[], object]], tuple[str, int]]) -> None:
    def word_job() -> None:
        # 20 texts, 100 words: normalize runs 100 times, tokenize 20.
        count_words(["The cat sat.", "The cat ran, and the dog sat."] * 10)

    got = impl(word_job)
    assert tuple(got) == ("normalize", 100), f"expected ('normalize', 100), got {got}"

    def recursive_job() -> None:
        depth(40)  # 41 calls, but only 1 of them from outside
        for word in ["a"] * 30:
            normalize(word)

    got = impl(recursive_job)
    assert tuple(got) == ("depth", 41), (
        f"recursive calls count too: expected ('depth', 41), got {got}"
    )


def check_most_called() -> None:
    report("5. most_called", test_most_called, most_called)


def main() -> None:
    check_has_duplicates()
    check_common_words()
    check_parse_readings()
    check_memoize()
    check_most_called()


if __name__ == "__main__":
    main()
