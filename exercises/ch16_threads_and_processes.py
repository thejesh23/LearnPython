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


# --- Exercise 2 -------------------------------------------------------------

class SafeCounter:
    """A counter that many threads can increment at the same time.

    `self.value += 1` is three steps (read, add, write). Two threads can both
    read 5 and both write 6, losing an increment. Store a threading.Lock()
    on the instance and hold it (`with self._lock:`) while changing value.

    - SafeCounter() starts at value 0.
    - increment(amount=1) adds amount to value.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def increment(self, amount: int = 1) -> None:
        raise NotImplementedError


def test_safe_counter(impl: type) -> None:
    counter = impl()
    assert counter.value == 0, f"a new counter should be 0, got {counter.value}"
    counter.increment()
    counter.increment(5)
    assert counter.value == 6, f"after +1 and +5 expected 6, got {counter.value}"
    lock_types = (type(threading.Lock()), type(threading.RLock()))
    assert any(isinstance(v, lock_types) for v in vars(counter).values()), (
        "store a threading.Lock() on the instance, e.g. self._lock"
    )

    def hammer() -> None:
        for _ in range(2000):
            counter.increment()

    threads = [threading.Thread(target=hammer) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    expected = 6 + 8 * 2000
    assert counter.value == expected, f"expected {expected}, got {counter.value}"


def check_safe_counter() -> None:
    report("2. SafeCounter", test_safe_counter, SafeCounter)


# --- Exercise 3 -------------------------------------------------------------

def run_all(funcs: list[Callable[[], Any]]) -> tuple[list[Any], list[str]]:
    """Call every function in a thread pool; collect results and errors.

    Submit each func to a ThreadPoolExecutor and keep the futures in a list.
    Then go through the futures in submission order: future.result() returns
    the value, or re-raises the exception the function raised. Return
    (results, errors), where errors holds "TypeName: message" strings,
    e.g. "ValueError: bad input". One failure must not stop the others.
    """
    raise NotImplementedError


def test_run_all(impl: Callable[[list[Callable[[], Any]]], Any]) -> None:
    def make(value: Any, delay: float) -> Callable[[], Any]:
        def func() -> Any:
            time.sleep(delay)
            if isinstance(value, Exception):
                raise value
            return value
        return func

    funcs = [make(1, 0.03), make(ValueError("bad input"), 0.0), make(2, 0.0),
             make(KeyError("k"), 0.01), make(3, 0.02)]
    results, errors = impl(funcs)
    assert results == [1, 2, 3], f"results should be [1, 2, 3], got {results}"
    expected = ["ValueError: bad input", "KeyError: 'k'"]
    assert errors == expected, f"errors should be {expected}, got {errors}"
    assert impl([]) == ([], []), "no functions should give ([], [])"


def check_run_all() -> None:
    report("3. run_all", test_run_all, run_all)


# --- Exercise 4 -------------------------------------------------------------

def fastest(tasks: dict[str, Callable[[], Any]]) -> str:
    """Run every task at once and return the name of the first to finish.

    Give the pool one worker per task, submit them all, and keep a dict
    from each future to its name. concurrent.futures.as_completed(futures)
    yields futures in the order they finish, so the first one it yields is
    the winner. (Leaving the with block still waits for the others; that is
    fine here.)
    """
    raise NotImplementedError


def test_fastest(impl: Callable[[dict[str, Callable[[], Any]]], str]) -> None:
    def sleeper(seconds: float) -> Callable[[], float]:
        def func() -> float:
            time.sleep(seconds)
            return seconds
        return func

    tasks = {"tortoise": sleeper(0.2), "hare": sleeper(0.0), "dog": sleeper(0.1)}
    got = impl(tasks)
    assert got == "hare", f"'hare' finishes first, got {got!r}"
    got = impl({"a": sleeper(0.1), "b": sleeper(0.25)})
    assert got == "a", f"'a' finishes first, got {got!r}"
    assert impl({"only": sleeper(0.0)}) == "only", "a single task wins"


def check_fastest() -> None:
    report("4. fastest", test_fastest, fastest)


# --- Exercise 5 -------------------------------------------------------------

def process_queue(
    func: Callable[[int], int], items: list[int], workers: int
) -> list[int]:
    """Process items with `workers` threads that share a queue.Queue.

    This is the classic producer/consumer pattern, built by hand:
      1. Start `workers` threading.Thread objects. Each loops: take an item
         with queue.get(); stop when it gets None; otherwise append
         func(item) to a shared results list (guard it with a Lock, or use
         a second Queue).
      2. Put every item on the queue, then one None per worker so each
         worker knows when to stop.
      3. join() every thread, then return the results sorted.
    """
    raise NotImplementedError


def test_process_queue(impl: Callable[..., list[int]]) -> None:
    lock = threading.Lock()
    thread_names: set[str] = set()

    def slow_triple(n: int) -> int:
        with lock:
            thread_names.add(threading.current_thread().name)
        time.sleep(0.005)
        return n * 3

    threads_before = threading.active_count()
    got = impl(slow_triple, [5, 1, 4, 2, 3, 0, 9, 8, 7, 6, 11, 10], 3)
    assert got == [n * 3 for n in range(12)], f"got {got}"
    assert threading.main_thread().name not in thread_names, (
        "func should run in the worker threads, not in the main thread"
    )
    assert 1 < len(thread_names) <= 3, (
        f"2 or 3 workers should share the items, saw {len(thread_names)}"
    )
    assert threading.active_count() == threads_before, (
        "every worker should have stopped: send one None per worker and join()"
    )
    assert impl(slow_triple, [], 2) == [], "no items should give []"
    assert threading.active_count() == threads_before, "workers should stop"


def check_process_queue() -> None:
    report("5. process_queue", test_process_queue, process_queue)


def main() -> None:
    check_parallel_map()
    check_safe_counter()
    check_run_all()
    check_fastest()
    check_process_queue()


if __name__ == "__main__":
    main()
