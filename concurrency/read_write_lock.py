"""A readers-writer lock: many readers together, or one writer alone.

Reads that do not mutate can safely overlap, so we let any number of them hold
the lock at once. A write must see a consistent snapshot, so it needs the lock
to itself — no readers, no other writer. The guarantee is exclusion between the
two roles, with maximum sharing inside the reader role.

The naive version starves writers: a steady stream of readers never lets the
count reach zero. This one is writer-preferred — once a writer is waiting, new
readers block behind it, so the writer gets in as soon as the current readers
drain. A single Condition guards the bookkeeping (active reader count, whether a
writer holds it, how many writers wait); readers and writers wait on it and are
woken when the relevant count changes. Context managers make acquire/release
exception-safe.
"""

import threading
import time
from contextlib import contextmanager
from typing import Iterator


class RWLock:
    def __init__(self) -> None:
        self._cond = threading.Condition()
        self._readers = 0
        self._writer = False
        self._writers_waiting = 0

    @contextmanager
    def read(self) -> Iterator[None]:
        with self._cond:
            # Defer to any writer that is holding or waiting: no starvation.
            while self._writer or self._writers_waiting > 0:
                self._cond.wait()
            self._readers += 1
        try:
            yield
        finally:
            with self._cond:
                self._readers -= 1
                if self._readers == 0:
                    self._cond.notify_all()

    @contextmanager
    def write(self) -> Iterator[None]:
        with self._cond:
            self._writers_waiting += 1
            while self._writer or self._readers > 0:
                self._cond.wait()
            self._writers_waiting -= 1
            self._writer = True
        try:
            yield
        finally:
            with self._cond:
                self._writer = False
                self._cond.notify_all()


def main() -> None:
    lock = RWLock()
    log: list[str] = []
    log_lock = threading.Lock()
    peak_readers = [0]
    live_readers = [0]

    def record(msg: str) -> None:
        with log_lock:
            log.append(msg)

    def reader(i: int) -> None:
        with lock.read():
            with log_lock:
                live_readers[0] += 1
                peak_readers[0] = max(peak_readers[0], live_readers[0])
            time.sleep(0.05)  # overlap window so readers actually coincide
            with log_lock:
                live_readers[0] -= 1

    writer_saw_readers = [False]

    def writer() -> None:
        with lock.write():
            # If exclusion works, no reader is active while we hold the lock.
            with log_lock:
                if live_readers[0] != 0:
                    writer_saw_readers[0] = True
            record("write start")
            time.sleep(0.02)
            record("write end")

    readers = [threading.Thread(target=reader, args=(i,)) for i in range(5)]
    for t in readers:
        t.start()
    for t in readers:
        t.join()
    print(f"peak concurrent readers: {peak_readers[0]} of 5 (readers share)")

    threads = [threading.Thread(target=reader, args=(i,)) for i in range(3)]
    threads.append(threading.Thread(target=writer))
    threads += [threading.Thread(target=reader, args=(i,)) for i in range(3, 6)]
    for t in threads:
        t.start()
        time.sleep(0.005)  # stagger so the writer lands mid-stream
    for t in threads:
        t.join()
    print(f"writer ever overlapped a reader: {writer_saw_readers[0]} (must be False)")
    print(f"write was exclusive: start/end adjacent = "
          f"{log == ['write start', 'write end']}")

    print("\nedge cases")
    solo = RWLock()
    with solo.read():
        pass  # acquire and release with nobody contending
    with solo.write():
        pass
    print("  uncontended read then write: fine")
    print(f"  live threads at exit: {threading.active_count()} (only MainThread)")


if __name__ == "__main__":
    main()
