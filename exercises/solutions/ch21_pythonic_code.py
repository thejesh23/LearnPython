"""Solutions: Pythonic code (chapter 21).

Worked answers for exercises/ch21_pythonic_code.py. Try each exercise
yourself before reading its solution; the struggle is where the learning
happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch21_pythonic_code.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch21_pythonic_code.py")
)
report = EXERCISES["report"]


def scoreboard(names: list[str], scores: list[int]) -> list[str]:
    # zip pairs the lists (strict=True raises ValueError on a length
    # mismatch); enumerate numbers the pairs, starting at 1.
    pairs = zip(names, scores, strict=True)
    return [f"{place}. {name} ({score})" for place, (name, score)
            in enumerate(pairs, start=1)]


def check_scoreboard() -> None:
    report("1. scoreboard", EXERCISES["test_scoreboard"], scoreboard)


def main() -> None:
    check_scoreboard()


if __name__ == "__main__":
    main()
