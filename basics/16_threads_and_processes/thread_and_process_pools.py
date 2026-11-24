"""`concurrent.futures` — pools of threads or processes that run your functions.

Creating, starting and joining threads by hand gets repetitive. A *pool* keeps
a few workers ready and hands them calls to make:

    ThreadPoolExecutor(max_workers=4)    workers are threads (good for waiting)
    ProcessPoolExecutor(max_workers=2)   workers are separate Python processes
                                         (good for heavy computation)
    pool.map(f, items)                   like map(), results in input order
    pool.submit(f, x)                    start one call, get a Future back
    as_completed(futures)                yield futures as they finish

A *Future* is a placeholder for a result that is not ready yet. Ask it with
`.result()`, which waits if needed and re-raises any exception the call raised.

Both pools have the same interface, so switching is a one-word change. The
catch with processes: functions and arguments are sent to the workers by
pickling, so the functions must be defined at the top level of a module, and
the script must start its work under `if __name__ == "__main__":`.
"""

import time
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def fetch_page(url: str) -> str:
    time.sleep(0.1)  # pretend to wait for a web server
    return f"<html of {url}>"


def map_demo() -> None:
    urls = [f"site{n}.example" for n in range(4)]
    start = time.perf_counter()
    # The with block waits for all work to finish and shuts the pool down.
    with ThreadPoolExecutor(max_workers=4) as pool:
        pages = list(pool.map(fetch_page, urls))
    elapsed = time.perf_counter() - start

    for page in pages:  # same order as urls, whatever order they finished in
        print(f"  {page}")
    print(f"4 fetches of 0.1s overlapped (took < 0.2s): {elapsed < 0.2}")


def slow_square(n: int, seconds: float) -> int:
    time.sleep(seconds)
    return n * n


def submit_demo() -> None:
    jobs = {1: 0.15, 2: 0.05, 3: 0.10}  # number -> how long it takes
    with ThreadPoolExecutor(max_workers=3) as pool:
        # submit() returns a Future at once. Keeping a dict from future to
        # input lets us tell which result belongs to which job later.
        futures: dict[Future[int], int] = {
            pool.submit(slow_square, n, seconds): n for n, seconds in jobs.items()
        }
        # as_completed yields each future the moment it finishes, so fast
        # jobs are handled first instead of waiting behind slow ones.
        for future in as_completed(futures):
            n = futures[future]
            print(f"  {n} squared is {future.result()} (took {jobs[n]}s)")


def main() -> None:
    map_demo()
    print()
    submit_demo()


if __name__ == "__main__":
    main()
