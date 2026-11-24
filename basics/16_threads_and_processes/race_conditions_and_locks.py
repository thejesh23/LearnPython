"""Race conditions, and the locks that prevent them.

When two threads read a shared value, change it, and write it back, they can
interleave like this:

    thread A reads count = 100
    thread B reads count = 100
    thread A writes 100 + 1 = 101
    thread B writes 100 + 1 = 101      <- A's update is lost

Nothing crashes; the answer is just wrong, and differently wrong on each run.
That is a *race condition*. The fix is to make the read-change-write step
happen as one unit that only one thread may be inside at a time:

    Lock     one holder at a time; `with lock:` acquires and always releases
    RLock    a lock the same thread may acquire again while holding it
    Event    a flag one thread sets and others wait for

CPython's GIL keeps the interpreter itself from being corrupted, but it does
not stop your own read-change-write steps from interleaving.
"""

import threading
import time
from collections.abc import Callable


THREADS = 4
INCREMENTS = 100


class Counter:
    def __init__(self) -> None:
        self.value = 0


def unsafe_add_one(counter: Counter) -> None:
    current = counter.value  # 1. read
    # The pause stands in for any real work between reading and writing.
    # In real code a thread switch lands here only once in a while, which is
    # why races slip through testing; the pause makes it happen every time.
    time.sleep(0.0001)
    counter.value = current + 1  # 2. write back a value that may be stale


def run_threads(work: Callable[[Counter], None], counter: Counter) -> None:
    def loop() -> None:
        for _ in range(INCREMENTS):
            work(counter)

    threads = [threading.Thread(target=loop) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def race_demo() -> None:
    counter = Counter()
    run_threads(unsafe_add_one, counter)
    expected = THREADS * INCREMENTS
    print(f"{THREADS} threads x {INCREMENTS} increments, expected {expected}")
    # The exact number changes from run to run; it is just never right.
    print(f"without a lock, updates were lost: {counter.value < expected}")


class SafeCounter(Counter):
    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()


def safe_add_one(counter: SafeCounter) -> None:
    # Only one thread at a time can be inside the with block. The others wait
    # at the door, so nobody can read a value that is about to change.
    # `with` releases the lock even if the body raises an exception.
    with counter.lock:
        current = counter.value
        time.sleep(0.0001)  # the same pause, now harmless
        counter.value = current + 1


def lock_demo() -> None:
    counter = SafeCounter()
    run_threads(safe_add_one, counter)  # type: ignore[arg-type]
    print(f"with a lock: {counter.value} (exactly right every run)")
    # The price: the locked part now runs one thread at a time. Keep locked
    # sections short, and never sleep or do slow I/O inside them in real code.


class Account:
    def __init__(self, reentrant: bool) -> None:
        self.balance = 0
        self.lock = threading.RLock() if reentrant else threading.Lock()

    def deposit(self, amount: int) -> None:
        with self.lock:
            self.balance += amount

    def deposit_twice(self, amount: int) -> bool:
        with self.lock:
            # deposit() takes the lock again while we already hold it. A plain
            # Lock would wait forever for itself (a deadlock), so we use a
            # timeout here just to show it failing instead of hanging.
            got_it = self.lock.acquire(timeout=0.1)
            if got_it:
                self.lock.release()
                self.deposit(amount)
                self.deposit(amount)
            return got_it


def rlock_demo() -> None:
    plain = Account(reentrant=False)
    print(f"plain Lock, re-acquired by the same thread: {plain.deposit_twice(5)}")

    # An RLock counts how many times its owner acquired it and is only
    # released once the owner has released it the same number of times.
    nested = Account(reentrant=True)
    ok = nested.deposit_twice(5)
    print(f"RLock, re-acquired by the same thread: {ok}, balance={nested.balance}")


def wait_for_config(ready: threading.Event, log: list[str]) -> None:
    log.append("worker: waiting for config")
    ready.wait()  # blocks until another thread calls ready.set()
    log.append("worker: config loaded, starting")


def event_demo() -> None:
    ready = threading.Event()
    log: list[str] = []
    worker = threading.Thread(target=wait_for_config, args=(ready, log))
    worker.start()

    time.sleep(0.05)  # the worker is now stuck in wait()
    log.append("main: config ready, setting the event")
    ready.set()
    worker.join()
    for line in log:
        print(line)

    # wait() can take a timeout and returns whether the flag was set.
    never = threading.Event()
    print(f"never.wait(timeout=0.05) -> {never.wait(timeout=0.05)}")


def main() -> None:
    race_demo()
    print()
    lock_demo()
    print()
    rlock_demo()
    print()
    event_demo()


if __name__ == "__main__":
    main()
