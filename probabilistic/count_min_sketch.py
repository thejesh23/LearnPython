"""Count-min sketch: frequency estimates in space that does not grow with the data.

Keep a table of d rows and w counters. Each row has its own hash function. To
record an item, increment one counter per row, at the column that row's hash
picks. To query, read those same d counters and return the smallest.

Collisions can only ever add to a counter, never subtract from it, so every
counter holding your item is at least its true count. Taking the minimum keeps
the least-contaminated estimate. The answer is therefore one-sided: never an
underestimate, sometimes an overestimate.

The guarantee is that with w = ceil(e/epsilon) and d = ceil(ln(1/delta)), the
error is at most epsilon * N with probability at least 1 - delta, where N is the
total number of increments. Widening the table shrinks the error; deepening it
shrinks the chance of exceeding the error. Both updates and queries are O(d),
independent of how many distinct items have been seen, in O(w * d) space.
"""

import math
import random
from collections import Counter
from typing import Hashable, Iterable


FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
MASK64 = (1 << 64) - 1


def fnv1a(data: bytes, seed: int = FNV_OFFSET) -> int:
    """A small, deterministic, seedable 64-bit hash — stable across processes."""
    h = seed
    for byte in data:
        h = ((h ^ byte) * FNV_PRIME) & MASK64
    # FNV alone leaves the high bits poorly mixed, and taking h % width would
    # then map two keys to the same column in every row at once. This final
    # avalanche step spreads every bit's influence across the whole word.
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & MASK64
    h ^= h >> 29
    return h


class CountMinSketch:
    def __init__(self, width: int, depth: int, seed: int = 0) -> None:
        if width <= 0 or depth <= 0:
            raise ValueError("width and depth must be positive")
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.total = 0
        rng = random.Random(seed)
        # One random salt per row makes the rows behave as independent hashes.
        self.salts = [rng.getrandbits(64) for _ in range(depth)]

    @classmethod
    def with_error(cls, epsilon: float, delta: float,
                   seed: int = 0) -> "CountMinSketch":
        """Size the table from the desired error bound rather than by hand."""
        width = math.ceil(math.e / epsilon)
        depth = math.ceil(math.log(1 / delta))
        return cls(width, depth, seed)

    def _columns(self, item: Hashable) -> list[int]:
        # Python's built-in hash() of a string is salted per process, so a
        # sketch built with it would give different answers on every run.
        data = repr(item).encode()
        return [fnv1a(data, salt) % self.width for salt in self.salts]

    def add(self, item: Hashable, count: int = 1) -> None:
        if count < 0:
            raise ValueError("count-min cannot handle negative counts")
        self.total += count
        for row, col in enumerate(self._columns(item)):
            self.table[row][col] += count

    def update(self, items: Iterable[Hashable]) -> None:
        for item in items:
            self.add(item)

    def estimate(self, item: Hashable) -> int:
        return min(self.table[row][col]
                   for row, col in enumerate(self._columns(item)))

    def error_bound(self) -> float:
        """The epsilon * N term: expected worst-case overestimate."""
        return math.e / self.width * self.total

    def heavy_hitters(self, candidates: Iterable[Hashable],
                      fraction: float) -> list[tuple[Hashable, int]]:
        """Candidates whose estimate exceeds fraction * N, largest first."""
        cut = fraction * self.total
        hits = [(c, self.estimate(c)) for c in candidates]
        return sorted((h for h in hits if h[1] >= cut),
                      key=lambda kv: -kv[1])


def zipf_stream(n: int, vocabulary: int, seed: int) -> list[str]:
    """A skewed stream: a few words very common, a long tail of rare ones."""
    rng = random.Random(seed)
    weights = [1 / (i + 1) for i in range(vocabulary)]
    total = sum(weights)
    cumulative = []
    running = 0.0
    for w in weights:
        running += w / total
        cumulative.append(running)
    out = []
    for _ in range(n):
        r = rng.random()
        lo, hi = 0, vocabulary - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cumulative[mid] < r:
                lo = mid + 1
            else:
                hi = mid
        out.append(f"w{lo:04d}")
    return out


def main() -> None:
    stream = zipf_stream(100_000, 5_000, seed=17)
    exact = Counter(stream)

    sketch = CountMinSketch(width=2000, depth=5, seed=99)
    sketch.update(stream)

    print(f"stream length {sketch.total}, distinct items {len(exact)}")
    print(f"table {sketch.depth} x {sketch.width} = "
          f"{sketch.depth * sketch.width} counters "
          f"(exact counting would need {len(exact)})")
    print(f"error bound e/w * N = {sketch.error_bound():.1f}")

    print("\ntop ten by true count")
    print("  item     exact  estimate   error")
    for item, count in exact.most_common(10):
        est = sketch.estimate(item)
        print(f"  {item}  {count:>7}  {est:>8}  {est - count:>6}")

    print("\nten rare items (where relative error hurts most)")
    rare = sorted(exact.items(), key=lambda kv: (kv[1], kv[0]))[:10]
    for item, count in rare:
        est = sketch.estimate(item)
        print(f"  {item}  {count:>7}  {est:>8}  {est - count:>6}")

    errors = [sketch.estimate(item) - count for item, count in exact.items()]
    print(f"\nnever underestimates: {min(errors) >= 0}")
    print(f"max overestimate:  {max(errors)}")
    print(f"mean overestimate: {sum(errors) / len(errors):.2f}")
    print(f"exact for {sum(1 for e in errors if e == 0)} of {len(errors)} items")

    print("\nwidth versus accuracy at depth 5")
    for width in (200, 500, 2000, 8000):
        s = CountMinSketch(width, 5, seed=99)
        s.update(stream)
        errs = [s.estimate(i) - c for i, c in exact.items()]
        print(f"  width {width:>6}: max error {max(errs):>6}, "
              f"mean {sum(errs) / len(errs):>8.2f}, "
              f"bound {s.error_bound():>9.1f}")

    print("\ndepth versus accuracy at width 500")
    for depth in (1, 2, 5, 10):
        s = CountMinSketch(500, depth, seed=99)
        s.update(stream)
        errs = [s.estimate(i) - c for i, c in exact.items()]
        print(f"  depth {depth:>2}: max error {max(errs):>6}, "
              f"mean {sum(errs) / len(errs):>8.2f}")

    sized = CountMinSketch.with_error(epsilon=0.001, delta=0.01, seed=5)
    print(f"\nwith_error(eps=0.001, delta=0.01) -> "
          f"{sized.depth} x {sized.width}")

    print("\nheavy hitters above 1% of the stream")
    for item, est in sketch.heavy_hitters(exact, 0.01):
        print(f"  {item}: estimate {est}, exact {exact[item]}")

    print("\nedge cases")
    tiny = CountMinSketch(4, 2, seed=1)
    print(f"  unseen item: {tiny.estimate('never-added')}")
    tiny.add("x", 10)
    print(f"  bulk add of 10: {tiny.estimate('x')}")
    tiny.add("x")
    print(f"  one more: {tiny.estimate('x')}")
    tiny.add(42)
    tiny.add((1, 2))
    print(f"  non-string keys: int {tiny.estimate(42)}, "
          f"tuple {tiny.estimate((1, 2))}")
    try:
        tiny.add("x", -1)
    except ValueError as exc:
        print(f"  negative count: ValueError({exc})")
    try:
        CountMinSketch(0, 3)
    except ValueError as exc:
        print(f"  zero width: ValueError({exc})")


if __name__ == "__main__":
    main()
