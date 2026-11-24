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
import timeit


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


def manual_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


def timeit_demo() -> None:
    n = 10_000
    # Pass a callable (or a string of code). number= is how many times to run
    # it; the result is the TOTAL time for all those runs, in seconds.
    loop_time = timeit.timeit(lambda: manual_sum(n), number=100)
    builtin_time = timeit.timeit(lambda: sum(range(n)), number=100)

    # Compare like with like: both compute exactly the same number.
    print(f"same answer: {manual_sum(n) == sum(range(n))}")
    print(f"sum(range(n)) faster than a manual loop: {builtin_time < loop_time}")
    # sum() runs its loop in C; the manual loop runs bytecode per item.
    print(f"... by more than 1.5x: {loop_time / builtin_time > 1.5}")

    # String form: setup= runs once, and is not included in the timing.
    per_call = timeit.timeit("sorted(data)", setup="data = list(range(1000))[::-1]",
                             number=200) / 200
    print(f"sorting 1000 ints takes under a millisecond: {per_call < 0.001}")


def repeat_demo() -> None:
    # repeat() returns one total per round. The rounds differ because of noise.
    runs = timeit.repeat(lambda: slow_square_sum(5_000), number=50, repeat=5)
    best, worst = min(runs), max(runs)
    print(f"5 rounds measured, best <= worst: {best <= worst}")
    print(f"noise made some round slower than the best: {worst > best}")
    # The per-call cost is the best round divided by number=.
    per_call = best / 50
    print(f"one call of slow_square_sum(5_000) takes under 10 ms: {per_call < 0.01}")

    # Not sure what number= to use? autorange() keeps increasing it until one
    # round takes at least 0.2 seconds, which is long enough to trust.
    timer = timeit.Timer(lambda: slow_square_sum(1_000))
    number, total = timer.autorange()
    # number depends on the machine (1, 2, 5, 10, 20, 50, ...), so it is not
    # printed here; the guarantee is about the round's total time.
    print(f"autorange found a number= whose round takes >= 0.2s: {total >= 0.2}")
    print(f"and it ran more than once: {number > 1}")


def fair_comparison_demo() -> None:
    data = list(range(10_000))
    target = 5_000
    lookup_set = set(data)

    in_list = min(timeit.repeat(lambda: target in data, number=200, repeat=3))
    # UNFAIR: this also times building the set, on every single run.
    unfair = min(timeit.repeat(lambda: target in set(data), number=200, repeat=3))
    # FAIR: the set is built once, outside the timing, like in a real program
    # that builds it once and then looks things up many times.
    fair = min(timeit.repeat(lambda: target in lookup_set, number=200, repeat=3))

    print(f"set lookup faster than list (set rebuilt each time): {unfair < in_list}")
    print(f"set lookup faster than list (set built once)       : {fair < in_list}")
    # Same question, opposite answers: what you include in the timing matters.
    # Checklist for a fair comparison:
    #   same input data for both versions, built outside the timed code
    #   enough runs (number=) and rounds (repeat=); keep the minimum
    #   check both versions return the same answer before timing them
    agree = (target in data) == (target in lookup_set)
    print(f"both versions agree on the answer: {agree}")


def main() -> None:
    perf_counter_demo()
    print()
    timeit_demo()
    print()
    repeat_demo()
    print()
    fair_comparison_demo()


if __name__ == "__main__":
    main()
