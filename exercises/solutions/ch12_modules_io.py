"""Solutions: modules, files and I/O (chapter 12).

Worked answers for exercises/ch12_modules_io.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch12_modules_io.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import json
import runpy
from pathlib import Path
from typing import Any


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


def write_scores(path: Path, scores: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Negate the score so one ascending sort gives "best first, then by name".
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
    lines = [f"{name}: {score}\n" for name, score in ranked]
    path.write_text("".join(lines), encoding="utf-8")


def check_write_scores() -> None:
    report("2. write_scores", EXERCISES["test_write_scores"], write_scores)


def load_settings(path: Path, defaults: dict[str, Any]) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as f:
            from_file = json.load(f)
    except FileNotFoundError:
        from_file = {}
    # {**a, **b} builds a new dict, so `defaults` is never modified.
    return {**defaults, **from_file}


def check_load_settings() -> None:
    report("3. load_settings", EXERCISES["test_load_settings"], load_settings)


def main() -> None:
    check_count_lines()
    check_write_scores()
    check_load_settings()


if __name__ == "__main__":
    main()
