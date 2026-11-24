"""Solutions: performance (chapter 20).

Worked answers for exercises/ch20_performance.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch20_performance.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from collections.abc import Hashable
from collections.abc import Iterable
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch20_performance.py")
)
report = EXERCISES["report"]


def has_duplicates(items: Iterable[Hashable]) -> bool:
    seen: set[Hashable] = set()
    for item in items:
        if item in seen:  # O(1) on average, however big `seen` grows
            return True  # stop at once: the rest of the input is never read
        seen.add(item)
    return False


def check_has_duplicates() -> None:
    report("1. has_duplicates", EXERCISES["test_has_duplicates"], has_duplicates)


def common_words(first: list[str], second: list[str]) -> list[str]:
    wanted = set(second)  # one O(n) pass; every lookup after this is O(1)
    result: list[str] = []
    for word in first:
        if word in wanted:
            result.append(word)
            wanted.discard(word)  # so a repeated word is not listed twice
    return result


def check_common_words() -> None:
    report("2. common_words", EXERCISES["test_common_words"], common_words)


def main() -> None:
    check_has_duplicates()
    check_common_words()


if __name__ == "__main__":
    main()
