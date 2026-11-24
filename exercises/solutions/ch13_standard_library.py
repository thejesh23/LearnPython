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

import re
import runpy
from collections import Counter
from collections import defaultdict
from collections import deque
from datetime import date, timedelta
from functools import cache
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


def moving_average(values: list[float], window: int) -> list[float]:
    if window < 1:
        raise ValueError(f"window must be at least 1, got {window}")
    recent: deque[float] = deque(maxlen=window)
    averages: list[float] = []
    for value in values:
        recent.append(value)  # the oldest value falls off the other end
        if len(recent) == window:
            averages.append(sum(recent) / window)
    return averages


def check_moving_average() -> None:
    report("3. moving_average", EXERCISES["test_moving_average"], moving_average)


def add_business_days(start: date, days: int) -> date:
    current = start
    remaining = days
    while remaining > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday=0 ... Friday=4
            remaining -= 1
    return current


def check_add_business_days() -> None:
    report("4. add_business_days", EXERCISES["test_add_business_days"],
           add_business_days)


# Compile once at import time; \b keeps 112/31/20267 from matching.
US_DATE = re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b")


def us_to_iso(text: str) -> str:
    # \3, \1, \2 put the captured year, month and day back in a new order.
    return US_DATE.sub(r"\3-\1-\2", text)


def check_us_to_iso() -> None:
    report("5. us_to_iso", EXERCISES["test_us_to_iso"], us_to_iso)


@cache
def count_paths(rows: int, cols: int) -> int:
    if rows == 1 or cols == 1:
        return 1
    # Each sub-grid is computed once; repeated calls are dictionary lookups.
    return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)


def check_count_paths() -> None:
    report("6. count_paths", EXERCISES["test_count_paths"], count_paths)


def main() -> None:
    check_top_words()
    check_group_by_length()
    check_moving_average()
    check_add_business_days()
    check_us_to_iso()
    check_count_paths()


if __name__ == "__main__":
    main()
