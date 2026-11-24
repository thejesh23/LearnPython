"""Measuring memory: `sys.getsizeof` versus `tracemalloc`.

`sys.getsizeof(obj)` sounds like "how much memory does this use?", but it
only counts the object itself, not the objects it refers to. A list is an
array of *references*; the strings or numbers it holds live elsewhere and are
not included. So getsizeof of a list of a million long strings is a few
megabytes, while the real total may be ten times that.

`tracemalloc` (in the standard library) watches every allocation Python makes
and can tell you how much is in use, the peak, and which *line of your code*
allocated it. It is the tool for "where did my memory go?".

    tracemalloc.start()                  begin tracing (it costs some speed)
    tracemalloc.get_traced_memory()      (current bytes, peak bytes)
    tracemalloc.take_snapshot()          a picture you can compare later
    snapshot.compare_to(old, "lineno")   what grew, grouped by source line

Byte counts differ a little between Python versions, so the demos round them
or compare them.
"""

import linecache
import sys
import tracemalloc
from collections.abc import Callable


def deep_size(items: list[str]) -> int:
    """The list itself plus every string it refers to (no sharing here)."""
    return sys.getsizeof(items) + sum(sys.getsizeof(s) for s in items)


def getsizeof_demo() -> None:
    short = ["x" * 10 for _ in range(1_000)]
    long = ["x" * 1_000 for _ in range(1_000)]

    # Same number of references, so the same getsizeof...
    print(f"getsizeof(short list) == getsizeof(long list): "
          f"{sys.getsizeof(short) == sys.getsizeof(long)}")
    # ...but very different real memory.
    print(f"deep size, short strings: ~{deep_size(short) // 1024} KB")
    print(f"deep size, long strings : ~{deep_size(long) // 1024} KB")

    # Even a "small" object has overhead: an int is not 8 bytes in Python.
    print(f"getsizeof(1) = {sys.getsizeof(1)} bytes, "
          f"getsizeof('') = {sys.getsizeof('')} bytes")


def build_index(count: int) -> dict[int, str]:
    return {n: f"record number {n:06d}" for n in range(count)}  # the big one


def snapshot_demo() -> None:
    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    index = build_index(50_000)
    after = tracemalloc.take_snapshot()
    current, _peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{len(index):,} records, traced memory now ~{current // 2**20} MB")
    # compare_to groups the difference by source line, biggest first.
    top = after.compare_to(before, "lineno")[0]
    frame = top.traceback[0]
    print(f"biggest growth: line {frame.lineno} of {frame.filename.split('/')[-1]}")
    print(f"  that line allocated over 1 MB: {top.size_diff > 2**20}")
    print(f"  source: {linecache.getline(frame.filename, frame.lineno).strip()}")


def peak_bytes_of(func: Callable[[], object]) -> int:
    """Run func and return the peak memory it needed, in bytes."""
    tracemalloc.start()
    tracemalloc.reset_peak()
    func()
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def list_vs_generator_demo() -> None:
    n = 200_000
    # The list comprehension builds all n squares before sum() sees any.
    list_peak = peak_bytes_of(lambda: sum([x * x for x in range(n)]))
    # The generator hands sum() one square at a time; each is freed at once.
    gen_peak = peak_bytes_of(lambda: sum(x * x for x in range(n)))

    print(f"list version peak  : ~{list_peak // 2**20} MB")
    print(f"generator peak     : under 10 KB: {gen_peak < 10 * 1024}")
    print(f"list needed over 100x more: {list_peak > 100 * gen_peak}")
    # The lesson: if you only loop over the values once, do not build a list.


def main() -> None:
    getsizeof_demo()
    print()
    snapshot_demo()
    print()
    list_vs_generator_demo()


if __name__ == "__main__":
    main()
