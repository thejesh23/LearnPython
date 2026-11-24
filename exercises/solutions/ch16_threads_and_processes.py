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

import queue
import runpy
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path
from typing import Any


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


def run_all(funcs: list[Callable[[], Any]]) -> tuple[list[Any], list[str]]:
    results: list[Any] = []
    errors: list[str] = []
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(func) for func in funcs]
        for future in futures:  # submission order, not finishing order
            try:
                results.append(future.result())
            except Exception as exc:  # the worker's exception, re-raised here
                errors.append(f"{type(exc).__name__}: {exc}")
    return results, errors


def check_run_all() -> None:
    report("3. run_all", EXERCISES["test_run_all"], run_all)


def fastest(tasks: dict[str, Callable[[], Any]]) -> str:
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        names = {pool.submit(func): name for name, func in tasks.items()}
        # as_completed yields each future as soon as it is done.
        winner = next(as_completed(names))
    return names[winner]


def check_fastest() -> None:
    report("4. fastest", EXERCISES["test_fastest"], fastest)


def process_queue(
    func: Callable[[int], int], items: list[int], workers: int
) -> list[int]:
    tasks: queue.Queue[int | None] = queue.Queue()
    results: list[int] = []
    results_lock = threading.Lock()

    def worker() -> None:
        while True:
            item = tasks.get()  # blocks until something is on the queue
            if item is None:  # the sentinel: no more work for this thread
                return
            value = func(item)
            with results_lock:
                results.append(value)

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for item in items:
        tasks.put(item)
    for _ in threads:
        tasks.put(None)  # one stop signal per worker
    for thread in threads:
        thread.join()
    return sorted(results)


def check_process_queue() -> None:
    report("5. process_queue", EXERCISES["test_process_queue"], process_queue)


def main() -> None:
    check_parallel_map()
    check_safe_counter()
    check_run_all()
    check_fastest()
    check_process_queue()


if __name__ == "__main__":
    main()
