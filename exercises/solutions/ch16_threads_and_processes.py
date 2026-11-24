"""Solutions: threads and processes (chapter 16).

Worked answers for exercises/ch16_threads_and_processes.py. Try each exercise
yourself before reading its solution; the struggle is where the learning
happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch16_threads_and_processes.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch16_threads_and_processes.py")
)
report = EXERCISES["report"]


def parallel_map(
    func: Callable[[int], int], items: list[int], workers: int
) -> list[int]:
    # Leaving the with block waits for every task and shuts the pool down.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(func, items))  # map keeps the input order


def check_parallel_map() -> None:
    report("1. parallel_map", EXERCISES["test_parallel_map"], parallel_map)


class SafeCounter:
    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> None:
        # Only one thread at a time may do the read-add-write.
        with self._lock:
            self.value += amount


def check_safe_counter() -> None:
    report("2. SafeCounter", EXERCISES["test_safe_counter"], SafeCounter)


def main() -> None:
    check_parallel_map()
    check_safe_counter()


if __name__ == "__main__":
    main()
