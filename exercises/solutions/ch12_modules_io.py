"""Solutions: modules, files and I/O (chapter 12).

Worked answers for exercises/ch12_modules_io.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch12_modules_io.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import csv
import importlib.util
import json
import runpy
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any
from typing import TextIO


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


def csv_totals(path: Path) -> dict[str, float]:
    totals: dict[str, float] = {}
    with path.open(newline="", encoding="utf-8") as f:
        # DictReader uses the header row as keys and handles quoted commas.
        for row in csv.DictReader(f):
            category = row["category"]
            totals[category] = totals.get(category, 0.0) + float(row["amount"])
    return totals


def check_csv_totals() -> None:
    report("4. csv_totals", EXERCISES["test_csv_totals"], csv_totals)


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # executes the file's top-level code
    return module


def check_load_module() -> None:
    report("5. load_module", EXERCISES["test_load_module"], load_module)


@contextmanager
def atomic_write(path: Path) -> Iterator[TextIO]:
    temp = path.with_name(path.name + ".tmp")
    try:
        with temp.open("w", encoding="utf-8") as f:
            yield f  # the body of the caller's with block runs here
        # Same folder, same filesystem: replace() swaps the files in one step.
        temp.replace(path)
    except BaseException:
        temp.unlink(missing_ok=True)  # clean up, then let the error continue
        raise


def check_atomic_write() -> None:
    report("6. atomic_write", EXERCISES["test_atomic_write"], atomic_write)


def main() -> None:
    check_count_lines()
    check_write_scores()
    check_load_settings()
    check_csv_totals()
    check_load_module()
    check_atomic_write()


if __name__ == "__main__":
    main()
