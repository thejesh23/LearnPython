"""A bounded thread pool built by hand, so the moving parts are visible.

Workers are long-lived threads that loop on a shared queue. The queue itself is
thread-safe, so dispatch needs no locking; each task carries its submission
index, and results are collected and sorted by that index at the end. Shutdown
uses one sentinel per worker — a worker that takes a sentinel puts nothing back
and exits, so every worker gets exactly one and none is left waiting.

A task that raises must not kill its worker or the whole pool, so the exception
is caught and stored alongside the successes; the caller decides what to do
with it. Results are indexed by submission order rather than completion order,
which is what makes the output deterministic even though the execution is not.
This is `concurrent.futures.ThreadPoolExecutor` in miniature — use that in real
code, and use processes instead of threads when the work is CPU-bound.
"""

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from queue import Queue
from typing import Any


@dataclass
class Result:
    index: int
    value: Any = None
    error: BaseException | None = None
    worker: str = ""

    @property
    def ok(self) -> bool:
        return self.error is None


class ThreadPool:
    def __init__(self, workers: int = 4) -> None:
        self.tasks: Queue[tuple[int, Callable[[], Any]] | None] = Queue()
        self.results: list[Result] = []
        self.lock = threading.Lock()
        self.threads = [
            threading.Thread(target=self._run, name=f"w{i}", daemon=True)
            for i in range(workers)
        ]
        self._started = False
        self._next_index = 0

    def _run(self) -> None:
        name = threading.current_thread().name
        while (item := self.tasks.get()) is not None:
            index, fn = item
            try:
                slot = Result(index, value=fn(), worker=name)
            except Exception as exc:  # a bad task must not kill the worker
                slot = Result(index, error=exc, worker=name)
            with self.lock:
                self.results.append(slot)
            self.tasks.task_done()
        self.tasks.task_done()  # account for the sentinel too

    def submit(self, fn: Callable[[], Any]) -> None:
        if self._started:
            raise RuntimeError("pool already shut down")
        self.tasks.put((self._next_index, fn))
        self._next_index += 1

    def run(self) -> list[Result]:
        """Start the workers, drain the queue, then shut down gracefully."""
        self._started = True
        for t in self.threads:
            t.start()
        for _ in self.threads:
            self.tasks.put(None)  # one sentinel each, after all real work
        for t in self.threads:
            t.join()
        return sorted(self.results, key=lambda r: r.index)


def make_task(n: int) -> Callable[[], int]:
    def task() -> int:
        time.sleep(0.01)  # stand-in for I/O; threads overlap this happily
        if n % 7 == 3:
            raise ValueError(f"task {n} refuses to compute")
        return n * n
    return task


def main() -> None:
    pool = ThreadPool(workers=4)
    for n in range(12):
        pool.submit(make_task(n))

    start = time.perf_counter()
    results = pool.run()
    elapsed = time.perf_counter() - start

    for r in results:
        status = f"{r.value}" if r.ok else f"{type(r.error).__name__}: {r.error}"
        print(f"  task {r.index:>2} on {r.worker}: {status}")

    ok = [r for r in results if r.ok]
    print(f"\n  {len(ok)} succeeded, {len(results) - len(ok)} failed")
    print(f"  order preserved: {[r.index for r in results]}")
    print(f"  wall time {elapsed:.2f}s vs {12 * 0.01:.2f}s serial "
          "(4 workers overlap the sleeps)")
    print(f"  all workers finished: {not any(t.is_alive() for t in pool.threads)}")

    print("\nedge cases")
    empty = ThreadPool(workers=3)
    print(f"  pool with no tasks: {empty.run()}")
    try:
        empty.submit(lambda: 1)
    except RuntimeError as exc:
        print(f"  submit after shutdown: {exc}")

    solo = ThreadPool(workers=1)
    solo.submit(lambda: 1 / 0)
    solo.submit(lambda: "fine")
    out = solo.run()
    print(f"  a crashing task does not stop the next one: "
          f"{[type(r.error).__name__ if not r.ok else r.value for r in out]}")


if __name__ == "__main__":
    main()
