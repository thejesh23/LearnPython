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
from collections.abc import Callable
from pathlib import Path
from typing import Any


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


def remove_short(words: list[str], min_length: int) -> None:
    # The comprehension reads the old contents in full before anything
    # changes; words[:] = then replaces the contents of the same list.
    words[:] = [word for word in words if len(word) >= min_length]


def check_remove_short() -> None:
    report("2. remove_short", EXERCISES["test_remove_short"], remove_short)


def make_multipliers(n: int) -> list[Callable[[int], int]]:
    # A default value is evaluated when the lambda is *created*, so each
    # lambda stores the k of its own loop round.
    return [lambda x, k=k: x * k for k in range(n)]


def check_make_multipliers() -> None:
    report("3. make_multipliers", EXERCISES["test_make_multipliers"],
           make_multipliers)


def load_port(path: Path, default: int = 8000) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default  # the one failure that is expected and fine
    # Outside the try: a bad value raises ValueError for the caller to see.
    port = int(text)  # int() ignores surrounding whitespace itself
    if not 1 <= port <= 65535:
        raise ValueError(f"port must be 1-65535, got {port} in {path}")
    return port


def check_load_port() -> None:
    report("4. load_port", EXERCISES["test_load_port"], load_port)


def get_nested(data: Any, *keys: Any, default: Any = None) -> Any:
    current = data
    try:
        for key in keys:
            current = current[key]
    except (KeyError, IndexError, TypeError):
        # Exactly the errors a failed lookup raises; anything else is a bug
        # and propagates.
        return default
    return current


def check_get_nested() -> None:
    report("5. get_nested", EXERCISES["test_get_nested"], get_nested)


def main() -> None:
    check_scoreboard()
    check_remove_short()
    check_make_multipliers()
    check_load_port()
    check_get_nested()


if __name__ == "__main__":
    main()
