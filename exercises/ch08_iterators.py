"""Practice exercises for basics/08_iterators: next(), generators, itertools.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch08_iterators.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

Several exercises ask for a generator: a function that uses `yield`. The
tests turn its output into a list to check it, and some feed it endless or
one-shot input to make sure it really works lazily, one value at a time.
Nothing here needs more than basics/00 to basics/08 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch08_iterators.py. Try each exercise yourself first.
"""

import itertools
from collections.abc import Callable, Iterable, Iterator
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


def first_or_default(iterable: Iterable[Any], default: Any = None) -> Any:
    """Return the first item of any iterable, or default when it is empty.

    It must work on endless iterators too, so do not turn the input into a
    list: take just the one item you need.

    first_or_default([3, 4])             -> 3
    first_or_default([])                 -> None
    first_or_default("", "nothing")      -> "nothing"
    first_or_default(itertools.count(5)) -> 5     an endless iterator
    """
    raise NotImplementedError


def test_first_or_default(fn: Callable[..., Any]) -> None:
    got = fn([3, 4])
    assert got == 3, f"first_or_default([3, 4]) returned {got!r}, expected 3"
    got = fn([])
    assert got is None, f"first_or_default([]) returned {got!r}, expected None"
    got = fn("abc")
    assert got == "a", f"first_or_default('abc') returned {got!r}, expected 'a'"
    got = fn("", "nothing")
    assert got == "nothing", (
        f"first_or_default('', 'nothing') returned {got!r}, expected 'nothing'"
    )
    got = fn(n * n for n in [9, 10])
    assert got == 81, f"first_or_default on a generator returned {got!r}, expected 81"

    def five_then_stop() -> Iterator[int]:
        # Stands in for an endless stream: reading a second value is a bug.
        yield 5
        raise RuntimeError(
            "first_or_default read past the first item; take just one with next()"
        )

    got = fn(five_then_stop())
    assert got == 5, (
        f"first_or_default on a stream starting with 5 returned {got!r}, expected 5"
    )


def check_first_or_default() -> None:
    report("1. first_or_default", test_first_or_default, first_or_default)


def countdown(n: int) -> Iterator[int]:
    """A generator that yields n, n - 1, ... down to 1.

    Use `yield`: the function should hand out one number at a time rather
    than build and return a list.

    list(countdown(3)) -> [3, 2, 1]
    list(countdown(0)) -> []
    """
    raise NotImplementedError


def test_countdown(fn: Callable[..., Any]) -> None:
    result = fn(3)
    assert hasattr(result, "__next__"), (
        f"countdown(3) returned {type(result).__name__} {result!r}; "
        "it should be a generator that yields its values"
    )
    for n, want in [(3, [3, 2, 1]), (1, [1]), (0, []), (5, [5, 4, 3, 2, 1])]:
        got = list(fn(n))
        assert got == want, f"list(countdown({n})) gave {got!r}, expected {want!r}"


def check_countdown() -> None:
    report("2. countdown", test_countdown, countdown)


def running_total(numbers: Iterable[int]) -> Iterator[int]:
    """Yield the running total after each number.

    numbers may be endless, so yield each total as soon as you have it;
    never collect the input first.

    list(running_total([1, 2, 3, 4])) -> [1, 3, 6, 10]
    list(running_total([]))           -> []
    first four of running_total(itertools.count(1)) -> [1, 3, 6, 10]
    """
    raise NotImplementedError


def test_running_total(fn: Callable[..., Any]) -> None:
    cases = [([1, 2, 3, 4], [1, 3, 6, 10]), ([], []), ([5, -5, 2], [5, 0, 2])]
    for numbers, want in cases:
        got = list(fn(numbers))
        assert got == want, (
            f"list(running_total({numbers!r})) gave {got!r}, expected {want!r}"
        )

    def four_then_stop() -> Iterator[int]:
        # Stands in for an endless stream: reading a fifth value is a bug.
        yield from [1, 2, 3, 4]
        raise RuntimeError(
            "running_total read past the numbers it needed; "
            "yield each total before reading the next number"
        )

    got = list(itertools.islice(fn(four_then_stop()), 4))
    assert got == [1, 3, 6, 10], (
        f"the first four running totals of 1, 2, 3, 4 were {got!r}, "
        "expected [1, 3, 6, 10]"
    )


def check_running_total() -> None:
    report("3. running_total", test_running_total, running_total)


def chunks(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """Yield lists of `size` items; the last list may be shorter.

    items can be any iterable, including a one-shot generator, so slicing
    items directly will not work.

    list(chunks([1, 2, 3, 4, 5], 2)) -> [[1, 2], [3, 4], [5]]
    list(chunks("abcdef", 3))        -> [["a", "b", "c"], ["d", "e", "f"]]
    list(chunks([], 4))              -> []

    Hint: itertools has a function made for this; it yields tuples.
    """
    raise NotImplementedError


def test_chunks(fn: Callable[..., Any]) -> None:
    cases = [
        (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
        (("abcdef", 3), [["a", "b", "c"], ["d", "e", "f"]]),
        (([], 4), []),
        (([1, 2], 5), [[1, 2]]),
    ]
    for args, want in cases:
        got = list(fn(*args))
        assert got == want, f"list(chunks{args}) gave {got!r}, expected {want!r}"
    got = list(fn((n for n in range(7)), 3))
    assert got == [[0, 1, 2], [3, 4, 5], [6]], (
        f"chunks of a generator over range(7), size 3, gave {got!r}, "
        "expected [[0, 1, 2], [3, 4, 5], [6]]"
    )


def check_chunks() -> None:
    report("4. chunks", test_chunks, chunks)


def run_lengths(text: str) -> list[tuple[str, int]]:
    """Return each run of repeated characters as a (character, count) pair.

    run_lengths("aaabccdd") -> [("a", 3), ("b", 1), ("c", 2), ("d", 2)]
    run_lengths("abab")     -> [("a", 1), ("b", 1), ("a", 1), ("b", 1)]
    run_lengths("")         -> []

    Hint: itertools.groupby groups *consecutive* equal items.
    """
    raise NotImplementedError


def test_run_lengths(fn: Callable[..., Any]) -> None:
    cases = [
        ("aaabccdd", [("a", 3), ("b", 1), ("c", 2), ("d", 2)]),
        ("abab", [("a", 1), ("b", 1), ("a", 1), ("b", 1)]),
        ("zzzz", [("z", 4)]),
        ("", []),
        ("x", [("x", 1)]),
    ]
    for text, want in cases:
        got = fn(text)
        assert got == want, f"run_lengths({text!r}) returned {got!r}, expected {want!r}"


def check_run_lengths() -> None:
    report("5. run_lengths", test_run_lengths, run_lengths)


def main() -> None:
    check_first_or_default()
    check_countdown()
    check_running_total()
    check_chunks()
    check_run_lengths()


if __name__ == "__main__":
    main()
