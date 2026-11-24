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

import sys


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


def main() -> None:
    getsizeof_demo()


if __name__ == "__main__":
    main()
