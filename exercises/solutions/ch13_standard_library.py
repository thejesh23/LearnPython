"""Solutions: the standard library (chapter 13).

Worked answers for exercises/ch13_standard_library.py. Try each exercise
yourself before reading its solution; the struggle is where the learning
happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch13_standard_library.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from collections import Counter
from collections import defaultdict
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch13_standard_library.py")
)
report = EXERCISES["report"]


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    words = (word.strip(".,!?;:").lower() for word in text.split())
    # Counter counts in one pass; the `if word` drops pure punctuation.
    return Counter(word for word in words if word).most_common(n)


def check_top_words() -> None:
    report("1. top_words", EXERCISES["test_top_words"], top_words)


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    groups: defaultdict[int, list[str]] = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)  # a missing key starts as []
    return dict(groups)  # a plain dict: later lookups will not add keys


def check_group_by_length() -> None:
    report("2. group_by_length", EXERCISES["test_group_by_length"], group_by_length)


def main() -> None:
    check_top_words()
    check_group_by_length()


if __name__ == "__main__":
    main()
