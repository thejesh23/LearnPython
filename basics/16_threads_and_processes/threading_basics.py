"""Threads — running several pieces of code at the same time in one program.

A thread is a separate line of execution that shares the program's memory with
every other thread. The `threading` module gives you:

    Thread(target=f, args=(...))   describe the work
    .start()                       begin running it in the background
    .join()                        wait until it finishes
    daemon=True                    do not keep the program alive for this one
    threading.current_thread()     which thread is running this line right now

In CPython, threads are great for work that *waits*: downloads, disk, sleeps,
subprocesses. While one thread waits, another runs. They do not make pure
Python number-crunching faster (see choosing_concurrency.py for why).

Output from several threads can interleave in any order, so the demos below
collect results and print them once the threads have finished.
"""

import threading
import time


def download(name: str, seconds: float, results: list[str]) -> None:
    time.sleep(seconds)  # stands in for waiting on a network or a disk
    # list.append is safe to call from several threads at once.
    results.append(f"{name} done")


def start_join_demo() -> None:
    results: list[str] = []
    threads = [
        threading.Thread(target=download, args=(f"file{i}", 0.1, results))
        for i in range(3)
    ]

    start = time.perf_counter()
    for t in threads:
        t.start()  # returns at once; the thread runs in the background
    for t in threads:
        t.join()  # block until this thread has finished
    elapsed = time.perf_counter() - start

    print(f"results: {sorted(results)}")
    # Three 0.1s waits, one after another, would take 0.3s.
    print(f"three 0.1s downloads overlapped (took < 0.2s): {elapsed < 0.2}")


def report(seen: list[str]) -> None:
    # current_thread() returns the Thread object running this very line, so
    # the same function can tell which of the workers is calling it.
    seen.append(threading.current_thread().name)


def current_thread_demo() -> None:
    print(f"the program starts in: {threading.current_thread().name}")
    print(f"is that the main thread: "
          f"{threading.current_thread() is threading.main_thread()}")

    seen: list[str] = []
    # Naming threads makes logs and tracebacks far easier to read.
    workers = [threading.Thread(target=report, args=(seen,), name=f"worker-{i}")
               for i in range(3)]
    for t in workers:
        t.start()
    for t in workers:
        t.join()
    print(f"threads that ran report(): {sorted(seen)}")
    print(f"still alive after join: {[t.is_alive() for t in workers]}")


def main() -> None:
    start_join_demo()
    print()
    current_thread_demo()


if __name__ == "__main__":
    main()
