"""Solutions: async and await (chapter 10).

Worked answers for exercises/ch10_async.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch10_async.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import asyncio
import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch10_async.py")
)
report = EXERCISES["report"]


async def add_later(a: int, b: int, delay: float) -> int:
    # asyncio.sleep hands control back to the event loop while it waits;
    # time.sleep would freeze every other task too.
    await asyncio.sleep(delay)
    return a + b


def check_add_later() -> None:
    report("1. add_later", EXERCISES["test_add_later"], add_later)


def main() -> None:
    check_add_later()


if __name__ == "__main__":
    main()
