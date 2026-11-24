"""Practice: threads and processes (chapter 16).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch16_threads_and_processes.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch16_threads_and_processes.py: try first, peek
second. The lessons for this chapter are in basics/16_threads_and_processes/.
"""

import threading
import time
from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

def parallel_map(
    func: Callable[[int], int], items: list[int], workers: int
) -> list[int]:
    """Return [func(x) for x in items], computed by a pool of worker threads.

    Use concurrent.futures.ThreadPoolExecutor(max_workers=workers) in a with
    block; its map() method keeps the results in the order of items, even
    when they finish in a different order.

    >>> parallel_map(lambda n: n * n, [1, 2, 3], workers=2)
    [1, 4, 9]
    """
    raise NotImplementedError


def test_parallel_map(impl: Callable[..., list[int]]) -> None:
    lock = threading.Lock()
    thread_names: set[str] = set()

    def slow_square(n: int) -> int:
        with lock:
            thread_names.add(threading.current_thread().name)
        time.sleep(0.01 * (n % 3))  # results finish out of order
        return n * n

    got = impl(slow_square, list(range(8)), 4)
    assert got == [n * n for n in range(8)], f"got {got}"
    assert threading.main_thread().name not in thread_names, (
        "func should run in worker threads, not in the main thread"
    )
    assert 1 < len(thread_names) <= 4, (
        f"expected 2 to 4 worker threads, saw {len(thread_names)}"
    )
    assert impl(slow_square, [], 2) == [], "no items should give []"


def check_parallel_map() -> None:
    report("1. parallel_map", test_parallel_map, parallel_map)


def main() -> None:
    check_parallel_map()


if __name__ == "__main__":
    main()
