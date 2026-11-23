"""Small summaries of big streams: count-min, HyperLogLog and MinHash.

All three hash with ``hash64``, which is seedable and identical in every
process (Python's built-in ``hash`` of a str is salted per run).
"""

import math
import random
from collections.abc import Hashable, Iterable

MASK64 = (1 << 64) - 1


def hash64(item: object, seed: int = 0xCBF29CE484222325) -> int:
    """FNV-1a over ``repr(item)`` plus a murmur-style finaliser to mix the high bits."""
    h = seed & MASK64
    for byte in repr(item).encode():
        h = ((h ^ byte) * 0x100000001B3) & MASK64
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & MASK64
    h ^= h >> 33
    h = (h * 0xC4CEB9FE1A85EC53) & MASK64
    return h ^ (h >> 33)


class CountMinSketch:
    """Frequency estimates that never undercount; error <= e/width * N, usually."""

    def __init__(self, width: int = 272, depth: int = 5, seed: int = 0) -> None:
        if width <= 0 or depth <= 0:
            raise ValueError("width and depth must be positive")
        self.width, self.total = width, 0
        self.table = [[0] * width for _ in range(depth)]
        rng = random.Random(seed)
        self.salts = [rng.getrandbits(64) for _ in range(depth)]  # one hash per row

    @classmethod
    def with_error(cls, epsilon: float, delta: float, seed: int = 0) -> "CountMinSketch":
        """Size the table so error <= epsilon * N with probability 1 - delta."""
        return cls(math.ceil(math.e / epsilon), math.ceil(math.log(1 / delta)), seed)

    def add(self, item: Hashable, count: int = 1) -> None:
        if count < 0:
            raise ValueError("count-min cannot handle negative counts")
        self.total += count
        for row, salt in zip(self.table, self.salts):
            row[hash64(item, salt) % self.width] += count

    def estimate(self, item: Hashable) -> int:
        """The least-contaminated counter: always >= the true count."""
        return min(row[hash64(item, salt) % self.width]
                   for row, salt in zip(self.table, self.salts))


class HyperLogLog:
    """Distinct-count estimate in 2**precision bytes; standard error 1.04/sqrt(m)."""

    def __init__(self, precision: int = 12) -> None:
        if not 4 <= precision <= 18:
            raise ValueError("precision must be between 4 and 18")
        self.p, self.m = precision, 1 << precision
        self.registers = [0] * self.m

    def add(self, item: object) -> None:
        h = hash64(item)
        index, rest = h >> (64 - self.p), (h << self.p) & MASK64
        rank = 64 - rest.bit_length() + 1 if rest else 64 - self.p + 1  # leading zeros + 1
        self.registers[index] = max(self.registers[index], rank)

    def count(self) -> float:
        """Harmonic mean of 2**register, with linear counting for small sets."""
        alpha = {16: 0.673, 32: 0.697, 64: 0.709}.get(self.m, 0.7213 / (1 + 1.079 / self.m))
        raw = alpha * self.m * self.m / sum(2.0 ** -r for r in self.registers)
        zeros = self.registers.count(0)
        if raw <= 2.5 * self.m and zeros:
            return self.m * math.log(self.m / zeros)
        return raw

    def merge(self, other: "HyperLogLog") -> "HyperLogLog":
        """Register-wise max: the sketch of the union of both streams."""
        if self.p != other.p:
            raise ValueError("cannot merge sketches of different precision")
        out = HyperLogLog(self.p)
        out.registers = [max(a, b) for a, b in zip(self.registers, other.registers)]
        return out


def shingles(text: str, n: int = 3) -> set[str]:
    """Word n-grams, so documents that share phrasing share elements."""
    words = text.lower().split()
    if not words:
        return set()
    return {" ".join(words[i:i + n]) for i in range(max(1, len(words) - n + 1))}


def jaccard(a: set, b: set) -> float:
    """|A & B| / |A | B|, defined as 1.0 for two empty sets."""
    return len(a & b) / len(a | b) if a or b else 1.0


class MinHash:
    """Signatures whose agreement rate estimates Jaccard similarity (+/- 1/sqrt(k))."""

    def __init__(self, num_hashes: int = 128, seed: int = 1) -> None:
        if num_hashes <= 0:
            raise ValueError("num_hashes must be positive")
        rng = random.Random(seed)
        self.seeds = [rng.getrandbits(64) for _ in range(num_hashes)]  # one "permutation" each

    def signature(self, items: Iterable[Hashable]) -> list[int]:
        """The minimum hash of the set under each seed."""
        items = list(items)
        return [min((hash64(x, s) for x in items), default=MASK64) for s in self.seeds]

    @staticmethod
    def similarity(sig_a: list[int], sig_b: list[int]) -> float:
        return sum(x == y for x, y in zip(sig_a, sig_b)) / len(sig_a)
