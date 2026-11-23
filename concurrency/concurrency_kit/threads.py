"""Thread coordination: a readers-writer lock, a chainable future, a worker pool."""

import threading
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from queue import Queue
from typing import Any


class RWLock:
    """Many readers together or one writer alone; waiting writers go first."""

    def __init__(self) -> None:
        self._cond = threading.Condition()
        self._readers = 0
        self._writer = False
        self._writers_waiting = 0

    @contextmanager
    def read(self) -> Iterator[None]:
        """Shared access: blocks only while a writer holds or awaits the lock."""
        with self._cond:
            while self._writer or self._writers_waiting:
                self._cond.wait()
            self._readers += 1
        try:
            yield
        finally:
            with self._cond:
                self._readers -= 1
                if not self._readers:
                    self._cond.notify_all()

    @contextmanager
    def write(self) -> Iterator[None]:
        """Exclusive access: waits for active readers and writers to leave."""
        with self._cond:
            self._writers_waiting += 1
            while self._writer or self._readers:
                self._cond.wait()
            self._writers_waiting -= 1
            self._writer = True
        try:
            yield
        finally:
            with self._cond:
                self._writer = False
                self._cond.notify_all()


class Future:
    """A set-once result slot; ``then`` chains a continuation without blocking."""

    def __init__(self) -> None:
        self._done = threading.Event()
        self._lock = threading.Lock()
        self._value: Any = None
        self._error: BaseException | None = None
        self._callbacks: list[Callable[["Future"], None]] = []

    def set_result(self, value: Any) -> None:
        """Fulfil the future; a second settle raises RuntimeError."""
        self._settle(value, None)

    def set_exception(self, error: BaseException) -> None:
        """Fail the future; waiters see ``error`` raised from ``result()``."""
        self._settle(None, error)

    def _settle(self, value: Any, error: BaseException | None) -> None:
        with self._lock:
            if self._done.is_set():
                raise RuntimeError("future already settled")
            self._value, self._error = value, error
            callbacks, self._callbacks = self._callbacks, []
            self._done.set()
        for cb in callbacks:  # outside the lock, so callbacks may touch us
            cb(self)

    def result(self, timeout: float | None = None) -> Any:
        """Block until settled; re-raise a stored exception."""
        if not self._done.wait(timeout):
            raise TimeoutError("future not settled in time")
        if self._error is not None:
            raise self._error
        return self._value

    def add_done_callback(self, cb: Callable[["Future"], None]) -> None:
        """Run ``cb(self)`` once settled, or right away if it already is."""
        with self._lock:
            if not self._done.is_set():
                self._callbacks.append(cb)
                return
        cb(self)

    def then(self, fn: Callable[[Any], Any]) -> "Future":
        """A new future settled with ``fn(result)``, or with this one's error."""
        chained = Future()

        def run(src: Future) -> None:
            try:
                chained.set_result(fn(src.result()))
            except BaseException as exc:
                chained.set_exception(exc)

        self.add_done_callback(run)
        return chained


@dataclass
class Result:
    """One task's outcome, tagged with its submission index."""

    index: int
    value: Any = None
    error: BaseException | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def pool_map(fn: Callable[[Any], Any], items: Iterable[Any], workers: int = 4) -> list[Result]:
    """Run ``fn`` over items on worker threads; results come back in input order."""
    tasks: Queue[tuple[int, Any] | None] = Queue()
    results: list[Result] = []
    lock = threading.Lock()

    def worker() -> None:
        while (job := tasks.get()) is not None:
            i, item = job
            try:
                out = Result(i, value=fn(item))
            except Exception as exc:  # a bad task must not kill its worker
                out = Result(i, error=exc)
            with lock:
                results.append(out)

    for job in enumerate(items):
        tasks.put(job)
    threads = [threading.Thread(target=worker) for _ in range(max(1, workers))]
    for t in threads:
        tasks.put(None)  # one sentinel per worker, queued after the real work
        t.start()
    for t in threads:
        t.join()
    return sorted(results, key=lambda r: r.index)
