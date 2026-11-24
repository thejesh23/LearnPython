"""Solutions: modules, files and I/O (chapter 12).

Worked answers for exercises/ch12_modules_io.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch12_modules_io.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch12_modules_io.py")
)
report = EXERCISES["report"]


def count_lines(path: Path) -> int:
    # strip() turns a whitespace-only line into "", which is falsy.
    with path.open(encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def check_count_lines() -> None:
    report("1. count_lines", EXERCISES["test_count_lines"], count_lines)


def main() -> None:
    check_count_lines()


if __name__ == "__main__":
    main()
