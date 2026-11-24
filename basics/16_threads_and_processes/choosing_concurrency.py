"""Threads, processes or asyncio? It depends on what your program is waiting for.

Two kinds of slow:
    I/O-bound   the program mostly waits: for the network, a disk, a database,
                a sleep. The CPU is idle during the wait.
    CPU-bound   the program is busy computing: parsing, maths, image work.

CPython has a *Global Interpreter Lock* (GIL): only one thread runs Python
bytecode at any moment. A thread gives the GIL up while it waits on I/O, so
threads overlap waiting nicely. But two threads doing pure Python arithmetic
just take turns, and finish no sooner than one thread doing both jobs.

The rough guide this file measures:
    many waits, a few dozen at once        threads
    many waits, thousands at once          asyncio (cheap tasks, one thread)
    heavy pure-Python computation          processes (each has its own GIL)

(Python 3.13 also ships an experimental "free-threaded" build without the GIL.
The standard build that most people run still has it.)
"""

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor


def timed(fn: Callable[[], object]) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def wait_for_io(_: int) -> None:
    time.sleep(0.05)  # sleeping releases the GIL, just like real I/O does


def io_bound_demo() -> None:
    jobs = range(6)
    one_by_one = timed(lambda: [wait_for_io(j) for j in jobs])

    def with_threads() -> None:
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(wait_for_io, jobs))

    threaded = timed(with_threads)
    print("I/O-bound: six 0.05s waits")
    print(f"  threads overlapped the waits: {threaded < one_by_one / 2}")
    # Six threads waiting at once took about as long as one wait.


def main() -> None:
    io_bound_demo()


if __name__ == "__main__":
    main()
