"""Worked solutions for exercises/ch07_collections.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from pathlib import Path
from typing import Any


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch07_collections.py")
)
report = EXERCISES["report"]


def squares_of_evens(nums: list[int]) -> list[int]:
    # Filter with the trailing `if`, transform with the leading expression.
    return [n * n for n in nums if n % 2 == 0]


def check_squares_of_evens() -> None:
    report("1. squares_of_evens", EXERCISES["test_squares_of_evens"],
           squares_of_evens)


def unique_in_order(items: list[Any]) -> list[Any]:
    # Dict keys are unique and keep insertion order, so dict.fromkeys is an
    # ordered set. A loop with a `seen` set works too.
    return list(dict.fromkeys(items))


def check_unique_in_order() -> None:
    report("2. unique_in_order", EXERCISES["test_unique_in_order"],
           unique_in_order)


def word_counts(text: str) -> dict[str, int]:
    # get(word, 0) reads the count so far, treating a new word as 0.
    # collections.Counter does the same job in one call.
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def check_word_counts() -> None:
    report("3. word_counts", EXERCISES["test_word_counts"], word_counts)


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    # setdefault returns the existing list, or inserts and returns a new
    # one, so a single line both creates and appends.
    groups: dict[int, list[str]] = {}
    for word in words:
        groups.setdefault(len(word), []).append(word)
    return groups


def check_group_by_length() -> None:
    report("4. group_by_length", EXERCISES["test_group_by_length"],
           group_by_length)


def common_items(a: list[Any], b: list[Any]) -> list[Any]:
    # Sets drop duplicates and & keeps what both share; sorted() turns the
    # unordered result into a predictable list.
    return sorted(set(a) & set(b))


def check_common_items() -> None:
    report("5. common_items", EXERCISES["test_common_items"], common_items)


def main() -> None:
    check_squares_of_evens()
    check_unique_in_order()
    check_word_counts()
    check_group_by_length()
    check_common_items()


if __name__ == "__main__":
    main()
