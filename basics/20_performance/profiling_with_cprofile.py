"""Profiling with `cProfile` and `pstats`: find out *where* the time goes.

`timeit` answers "how fast is this snippet?". A profiler answers the more
useful question for a whole program: "which function is it spending its time
in?". The answer is very often not the function you would have guessed.

`cProfile` records every function call while your code runs. `pstats` turns
the record into a table. The columns that matter:

    ncalls    how many times the function was called
    tottime   time spent in the function's OWN code (not counting the
              functions it called) -- a big tottime is a hotspot
    cumtime   time in the function INCLUDING everything it called -- big for
              any top-level function, since it contains all the work

The workflow: profile, find the row with the biggest tottime, fix that one
thing, check the result is unchanged, profile again.
"""

import cProfile
import io
import pstats
import random
import timeit


def make_words(count: int, seed: int = 7) -> list[str]:
    rng = random.Random(seed)  # seeded, so every run sees the same words
    return [f" Word{rng.randrange(count)} " for _ in range(count)]


def normalize(word: str) -> str:
    return word.strip().lower()


def is_new(word: str, seen: list[str]) -> bool:
    return word not in seen  # scans the whole list: O(len(seen)) per call


def unique_words_slow(words: list[str]) -> list[str]:
    seen: list[str] = []
    for word in words:
        clean = normalize(word)
        if is_new(clean, seen):
            seen.append(clean)
    return seen


def profile_rows(profile: cProfile.Profile) -> list[tuple[str, int, float, float]]:
    """(name, ncalls, tottime share, cumtime share) for this file's functions."""
    stats = pstats.Stats(profile).get_stats_profile()
    total = stats.total_tt or 1.0
    rows = []
    for name, info in stats.func_profiles.items():
        if info.file_name == __file__:  # skip built-ins like list.append
            ncalls = int(info.ncalls.split("/")[0])  # "a/b" for recursion
            rows.append((name, ncalls, info.tottime / total, info.cumtime / total))
    return rows


def print_table(rows: list[tuple[str, int, float, float]]) -> None:
    # Timings differ per run, so the table shows call counts (exact) and
    # marks a row "HOT" when it holds over three quarters of all own time.
    print(f"  {'ncalls':>7}  {'function':<18} own time")
    for name, ncalls, own, _cum in sorted(rows, key=lambda r: (-r[1], r[0])):
        print(f"  {ncalls:>7}  {name:<18} {'HOT' if own > 0.75 else '-'}")


WORDS = make_words(4_000)


def profile_demo() -> None:
    with cProfile.Profile() as profile:
        result = unique_words_slow(WORDS)
    print(f"{len(WORDS)} words, {len(result)} unique")
    print_table(profile_rows(profile))


def tottime_vs_cumtime_demo() -> None:
    with cProfile.Profile() as profile:
        unique_words_slow(WORDS)
    rows = profile_rows(profile)
    by_own = max(rows, key=lambda r: r[2])[0]
    by_cumulative = max(rows, key=lambda r: r[3])[0]
    # The top-level function "contains" all the time, so it tops cumtime but
    # tells you nothing. The hotspot is the row with the largest tottime.
    print(f"largest cumtime: {by_cumulative}  (the caller of everything)")
    print(f"largest tottime: {by_own}  (the real hotspot)")

    # The real pstats report. sort_stats picks the column to sort by,
    # strip_dirs() shortens file paths, print_stats(n) shows the top n rows.
    report = io.StringIO()
    stats = pstats.Stats(profile, stream=report)
    stats.strip_dirs().sort_stats("tottime").print_stats(1)
    lines = report.getvalue().splitlines()
    header = next(line for line in lines if line.lstrip().startswith("ncalls"))
    top_row = lines[lines.index(header) + 1].split()
    # Print the header and the top row, minus the timings that vary per run.
    print(header)
    print(f"{top_row[0]:>9}  {'(four timing columns)':<35}{top_row[-1]}")


def unique_words_fast(words: list[str]) -> list[str]:
    # A set answers "have I seen this?" in O(1); the list keeps the order.
    seen: set[str] = set()
    ordered: list[str] = []
    for word in words:
        clean = normalize(word)
        if clean not in seen:
            seen.add(clean)
            ordered.append(clean)
    return ordered


def fix_hotspot_demo() -> None:
    # Step 1: a faster wrong answer is worthless, so check correctness first.
    print(f"same result: {unique_words_fast(WORDS) == unique_words_slow(WORDS)}")

    # Step 2: profile again. is_new is gone; nothing is HOT any more.
    with cProfile.Profile() as profile:
        unique_words_fast(WORDS)
    print_table(profile_rows(profile))

    # Step 3: confirm the win with a plain timing, outside the profiler
    # (profiling itself slows every call down).
    slow = min(timeit.repeat(lambda: unique_words_slow(WORDS), number=1, repeat=3))
    fast = min(timeit.repeat(lambda: unique_words_fast(WORDS), number=1, repeat=3))
    print(f"fast version is faster: {fast < slow}")
    print(f"... by more than 10x: {slow / fast > 10}")


def main() -> None:
    profile_demo()
    print()
    tottime_vs_cumtime_demo()
    print()
    fix_hotspot_demo()


if __name__ == "__main__":
    main()
