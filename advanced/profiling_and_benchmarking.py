"""Measuring, not guessing: timeit, cProfile, and tracemalloc.

Three tools for three questions:
    timeit       how long does this small snippet take? (many runs, best-of)
    cProfile     which function is the time going into? (per-call breakdown)
    tracemalloc  where is the memory being allocated?

Rules that keep the numbers honest: use `perf_counter`, never `time.time`, for
elapsed time; take the *minimum* of several timeit runs, not the mean, because
noise only ever adds; and profile before optimising — the bottleneck is almost
never where it feels like it is.
"""

import cProfile
import io
import pstats
import timeit
import tracemalloc


def concat_plus(n: int) -> str:
    out = ""
    for i in range(n):
        out += str(i)  # quadratic: builds a new string each time
    return out


def concat_join(n: int) -> str:
    return "".join(str(i) for i in range(n))


def slow_path() -> int:
    return sum(i * i for i in range(200_000))


def fast_path() -> int:
    return sum(range(200_000))


def workload() -> None:
    slow_path()
    fast_path()
    slow_path()


def main() -> None:
    print("timeit — 5 runs of 20 iterations, reporting the best:")
    for label, fn in (("+= in a loop", concat_plus), ("str.join", concat_join)):
        best = min(timeit.repeat(lambda: fn(2000), number=20, repeat=5))
        print(f"  {label:<14} {best * 1000:7.2f} ms")

    print("\ntimeit on a snippet, with setup:")
    t = min(timeit.repeat("d[500]", setup="d = {i: i for i in range(1000)}",
                          number=100_000, repeat=3))
    print(f"  dict lookup x100k: {t * 1000:.2f} ms")
    t = min(timeit.repeat("500 in lst", setup="lst = list(range(1000))",
                          number=10_000, repeat=3))
    print(f"  list scan   x10k:  {t * 1000:.2f} ms")

    print("\ncProfile — where the time goes:")
    buffer = io.StringIO()
    profiler = cProfile.Profile()
    profiler.enable()
    workload()
    profiler.disable()
    stats = pstats.Stats(profiler, stream=buffer).sort_stats("cumulative")
    stats.print_stats(5)
    for line in buffer.getvalue().splitlines()[4:11]:
        print(f"  {line}")

    print("\ntracemalloc — where the memory goes:")
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    big = [str(i) for i in range(100_000)]
    snapshot_after = tracemalloc.take_snapshot()
    top = snapshot_after.compare_to(snapshot_before, "lineno")[:2]
    for stat in top:
        print(f"  {stat}")
    tracemalloc.stop()
    del big


if __name__ == "__main__":
    main()
