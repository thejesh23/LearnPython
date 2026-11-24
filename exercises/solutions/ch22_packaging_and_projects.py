"""Solutions: packaging and projects (chapter 22).

Worked answers for exercises/ch22_packaging_and_projects.py. Try each
exercise yourself before reading its solution; the struggle is where the
learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch22_packaging_and_projects.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch22_packaging_and_projects.py")
)
report = EXERCISES["report"]


def bump_version(version: str, part: str) -> str:
    pieces = version.split(".")
    if len(pieces) != 3:
        raise ValueError(f"expected MAJOR.MINOR.PATCH, got {version!r}")
    major, minor, patch = map(int, pieces)  # int("x") raises ValueError
    match part:
        case "major":
            major, minor, patch = major + 1, 0, 0
        case "minor":
            minor, patch = minor + 1, 0
        case "patch":
            patch += 1
        case _:
            raise ValueError(f"part must be major, minor or patch, not {part!r}")
    return f"{major}.{minor}.{patch}"


def check_bump_version() -> None:
    report("1. bump_version", EXERCISES["test_bump_version"], bump_version)


def main() -> None:
    check_bump_version()


if __name__ == "__main__":
    main()
