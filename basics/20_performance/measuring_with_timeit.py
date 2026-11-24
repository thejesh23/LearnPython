"""Measuring speed: `time.perf_counter` and the `timeit` module.

"Which version is faster?" is a question for a measurement, not a hunch. But
measuring is easy to get wrong: one run is noisy, the first run is often slow,
and it is easy to time the wrong thing.

    time.perf_counter()   a high-resolution clock for "how long did this take"
    timeit.timeit         run a snippet many times, return the total seconds
    timeit.repeat         do that several times; keep the *minimum*

Why the minimum? Other programs, the OS and the garbage collector can only
ever make a run *slower*, never faster, so the best run is the closest to the
code's true cost.

Exact timings change from machine to machine and run to run, so this file
prints comparisons ("faster: True") instead of raw numbers. That is also the
habit to keep: a timing means something only next to another timing.
"""

import time


def slow_square_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def perf_counter_demo() -> None:
    # perf_counter is monotonic: it never jumps backwards when the system
    # clock is adjusted, which time.time() can do.
    info = time.get_clock_info("perf_counter")
    print(f"perf_counter monotonic: {info.monotonic}, adjustable: {info.adjustable}")

    start = time.perf_counter()
    slow_square_sum(200_000)
    small = time.perf_counter() - start

    start = time.perf_counter()
    slow_square_sum(2_000_000)
    large = time.perf_counter() - start

    # The absolute values differ per machine; the relationship does not.
    print(f"10x the work took longer: {large > small}")
    print(f"roughly 10x longer (between 3x and 30x): {3 < large / small < 30}")


def main() -> None:
    perf_counter_demo()


if __name__ == "__main__":
    main()
