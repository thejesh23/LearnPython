"""Practice exercises for basics/07_collections: lists, dicts, sets, sorting.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch07_collections.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

Most of these have a short answer once you pick the right collection: a
comprehension, a dict, a set, or sorted() with a key. Nothing here needs
more than basics/00 to basics/07 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch07_collections.py. Try each exercise yourself first.
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


def squares_of_evens(nums: list[int]) -> list[int]:
    """Return the squares of the even numbers, in their original order.

    squares_of_evens([1, 2, 3, 4]) -> [4, 16]
    squares_of_evens([5, -2, 0])   -> [4, 0]
    squares_of_evens([])           -> []
    """
    raise NotImplementedError


def test_squares_of_evens(fn: Callable[..., Any]) -> None:
    cases = [
        ([1, 2, 3, 4], [4, 16]),
        ([5, -2, 0], [4, 0]),
        ([1, 3, 5], []),
        ([], []),
        ([10, 8], [100, 64]),
    ]
    for nums, want in cases:
        got = fn(nums)
        assert got == want, (
            f"squares_of_evens({nums!r}) returned {got!r}, expected {want!r}"
        )


def check_squares_of_evens() -> None:
    report("1. squares_of_evens", test_squares_of_evens, squares_of_evens)


def unique_in_order(items: list[Any]) -> list[Any]:
    """Return the items with duplicates removed, keeping first-seen order.

    unique_in_order(["b", "a", "b", "c", "a"]) -> ["b", "a", "c"]
    unique_in_order([1, 1, 1])                 -> [1]

    Note: set(items) drops duplicates but also loses the order.
    """
    raise NotImplementedError


def test_unique_in_order(fn: Callable[..., Any]) -> None:
    cases = [
        (["b", "a", "b", "c", "a"], ["b", "a", "c"]),
        ([1, 1, 1], [1]),
        ([3, 2, 1], [3, 2, 1]),
        ([], []),
        ([5, 4, 5, 3, 4, 5], [5, 4, 3]),
    ]
    for items, want in cases:
        got = fn(items)
        assert got == want, (
            f"unique_in_order({items!r}) returned {got!r}, expected {want!r}"
        )


def check_unique_in_order() -> None:
    report("2. unique_in_order", test_unique_in_order, unique_in_order)


def word_counts(text: str) -> dict[str, int]:
    """Count how often each word appears, ignoring case.

    Words are separated by whitespace; there is no punctuation. The keys
    are the lower-case words.

    word_counts("the cat and the hat") -> {"the": 2, "cat": 1, "and": 1, "hat": 1}
    word_counts("Go go GO")            -> {"go": 3}
    word_counts("")                    -> {}
    """
    raise NotImplementedError


def test_word_counts(fn: Callable[..., Any]) -> None:
    cases = [
        ("the cat and the hat", {"the": 2, "cat": 1, "and": 1, "hat": 1}),
        ("Go go GO", {"go": 3}),
        ("", {}),
        ("  one\ttwo\n two  ", {"one": 1, "two": 2}),
    ]
    for text, want in cases:
        got = fn(text)
        assert got == want, f"word_counts({text!r}) returned {got!r}, expected {want!r}"


def check_word_counts() -> None:
    report("3. word_counts", test_word_counts, word_counts)


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Group words by their length, keeping each group in original order.

    group_by_length(["hi", "cat", "yo", "a"])
        -> {2: ["hi", "yo"], 3: ["cat"], 1: ["a"]}

    Hint: dict.setdefault(key, []) returns the list for key, creating it
    the first time.
    """
    raise NotImplementedError


def test_group_by_length(fn: Callable[..., Any]) -> None:
    cases = [
        (["hi", "cat", "yo", "a"], {2: ["hi", "yo"], 3: ["cat"], 1: ["a"]}),
        (["same", "size", "word"], {4: ["same", "size", "word"]}),
        ([], {}),
        (["", "x"], {0: [""], 1: ["x"]}),
    ]
    for words, want in cases:
        got = fn(words)
        assert got == want, (
            f"group_by_length({words!r}) returned {got!r}, expected {want!r}"
        )


def check_group_by_length() -> None:
    report("4. group_by_length", test_group_by_length, group_by_length)


def main() -> None:
    check_squares_of_evens()
    check_unique_in_order()
    check_word_counts()
    check_group_by_length()


if __name__ == "__main__":
    main()
