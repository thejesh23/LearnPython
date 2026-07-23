"""Futures: a placeholder for a value that another thread will supply later.

A future starts empty. One side (the producer, or "promise") eventually fulfils
it with a result or an exception; other sides call result() and block until it
is set, or register a callback to be run the moment it arrives. The guarantee is
set-once: the value is written exactly one time, and every waiter — whether it
arrived before or after the set — observes that same value. An Event flips from
unset to set and never back, which is precisely the one-way transition a future
needs.

Callbacks let you chain: attach a continuation that runs on completion and,
here, feeds a second future so you can build small pipelines without blocking.
The standard library's `concurrent.futures.Future` is the same idea, hardened;
we mirror it at the end so the hand-built version's semantics are recognisable.
"""

import threading
from concurrent.futures import Future as StdFuture
from typing import Any, Callable


class Future:
    def __init__(self) -> None:
        self._done = threading.Event()
        self._value: Any = None
        self._error: BaseException | None = None
        self._callbacks: list[Callable[["Future"], None]] = []
        self._lock = threading.Lock()

    def set_result(self, value: Any) -> None:
        self._settle(value, None)

    def set_exception(self, error: BaseException) -> None:
        self._settle(None, error)

    def _settle(self, value: Any, error: BaseException | None) -> None:
        with self._lock:
            if self._done.is_set():
                raise RuntimeError("future already settled")  # set-once
            self._value, self._error = value, error
            callbacks = self._callbacks
            self._callbacks = []
            self._done.set()
        for cb in callbacks:  # run outside the lock to avoid re-entrancy stalls
            cb(self)

    def result(self, timeout: float | None = None) -> Any:
        if not self._done.wait(timeout):
            raise TimeoutError("future not settled in time")
        if self._error is not None:
            raise self._error
        return self._value

    def add_done_callback(self, cb: Callable[["Future"], None]) -> None:
        with self._lock:
            if self._done.is_set():
                run_now = True
            else:
                self._callbacks.append(cb)
                run_now = False
        if run_now:  # already settled: fire immediately, like the stdlib
            cb(self)

    def then(self, fn: Callable[[Any], Any]) -> "Future":
        """Chain: return a new future fulfilled with fn(this result)."""
        chained: Future = Future()

        def run(src: "Future") -> None:
            try:
                chained.set_result(fn(src.result()))
            except BaseException as exc:  # propagate failures down the chain
                chained.set_exception(exc)

        self.add_done_callback(run)
        return chained


def main() -> None:
    fut: Future = Future()

    def producer() -> None:
        import time
        time.sleep(0.02)
        fut.set_result(21)

    t = threading.Thread(target=producer)
    t.start()
    doubled = fut.then(lambda x: x * 2)  # continuation attached before it settles
    print(f"awaited result: {fut.result(timeout=1)}")
    print(f"chained continuation: {doubled.result(timeout=1)}")
    t.join()

    # A callback registered after settling still fires (runs immediately).
    seen: list[int] = []
    fut.add_done_callback(lambda f: seen.append(f.result()))
    print(f"late callback still ran: {seen == [21]}")

    # Exceptions travel through result() and down a chain unchanged.
    bad: Future = Future()
    bad.set_exception(ValueError("boom"))
    try:
        bad.result()
    except ValueError as exc:
        print(f"exception surfaced on result(): {exc}")
    chained_err = bad.then(lambda x: x + 1)
    print(f"chain propagates the error: "
          f"{isinstance(chained_err._error, ValueError)}")

    print("\ncontrast: concurrent.futures.Future")
    std: StdFuture = StdFuture()
    std.add_done_callback(lambda f: print(f"  stdlib callback saw {f.result()}"))
    std.set_result(99)
    print(f"  stdlib result(): {std.result()}")

    print("\nedge cases")
    empty: Future = Future()
    try:
        empty.result(timeout=0.01)  # never settled
    except TimeoutError as exc:
        print(f"  waiting on an unset future times out: {exc}")
    once: Future = Future()
    once.set_result(1)
    try:
        once.set_result(2)  # set-once is enforced
    except RuntimeError as exc:
        print(f"  double-set rejected: {exc}")
    print(f"  live threads at exit: {threading.active_count()} (only MainThread)")


if __name__ == "__main__":
    main()
