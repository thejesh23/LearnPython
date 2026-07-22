"""HyperLogLog: counting distinct items in kilobytes instead of gigabytes.

Hash each item to a uniform bit string. In a uniform stream about half the hashes
start with a 1, a quarter start with 01, an eighth with 001, and so on. So if the
longest run of leading zeros you have ever seen is r, you have probably seen
around 2^(r+1) distinct values. One such estimate is hopelessly noisy, so the
hash's first p bits pick one of m = 2^p registers and each register keeps its own
maximum, turning one wild guess into m averaged ones.

Averaging is done harmonically, which suppresses the influence of a register that
happened to see a freak run of zeros, and the result is multiplied by a constant
alpha that corrects the bias this estimator would otherwise have. The standard
error is about 1.04/sqrt(m): 16384 registers, one byte each, give roughly 0.8%
error while counting billions.

The raw estimator misbehaves when the sketch is nearly empty, so below 2.5m it is
replaced by linear counting over the registers still at zero. Because we hash to
64 bits, the large-range correction needed by the original 32-bit paper never
applies. Adding an item is O(1); merging two sketches is a register-wise maximum,
which is what makes the structure so useful across distributed counters.
"""

import math


FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
MASK64 = (1 << 64) - 1


def hash64(data: bytes) -> int:
    """Deterministic 64-bit hash: FNV-1a plus a murmur-style finaliser.

    The finaliser matters. Plain FNV-1a barely mixes its high bits, and this
    algorithm reads the register index straight off the top of the word.
    """
    h = FNV_OFFSET
    for byte in data:
        h = ((h ^ byte) * FNV_PRIME) & MASK64
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & MASK64
    h ^= h >> 33
    h = (h * 0xC4CEB9FE1A85EC53) & MASK64
    h ^= h >> 33
    return h


def alpha_for(m: int) -> float:
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    return 0.7213 / (1 + 1.079 / m)


class HyperLogLog:
    def __init__(self, precision: int = 14) -> None:
        if not 4 <= precision <= 18:
            raise ValueError("precision must be between 4 and 18")
        self.p = precision
        self.m = 1 << precision
        self.registers = [0] * self.m
        self.alpha = alpha_for(self.m)

    def add(self, item: object) -> None:
        h = hash64(repr(item).encode())
        index = h >> (64 - self.p)  # top p bits choose the register
        rest = (h << self.p) & MASK64  # remaining bits, left aligned
        # Leading zeros of the remainder, plus one; a zero remainder means the
        # whole 64-p bit tail was zero, the rarest case we can represent.
        rank = 64 - rest.bit_length() + 1 if rest else 64 - self.p + 1
        if rank > self.registers[index]:
            self.registers[index] = rank

    def update(self, items) -> None:
        for item in items:
            self.add(item)

    def count(self) -> float:
        harmonic = sum(2.0 ** -r for r in self.registers)
        raw = self.alpha * self.m * self.m / harmonic
        zeros = self.registers.count(0)
        if raw <= 2.5 * self.m and zeros:
            # Nearly empty: linear counting is far more accurate here.
            return self.m * math.log(self.m / zeros)
        return raw

    def merge(self, other: "HyperLogLog") -> "HyperLogLog":
        if self.p != other.p:
            raise ValueError("cannot merge sketches of different precision")
        out = HyperLogLog(self.p)
        out.registers = [max(a, b) for a, b in zip(self.registers, other.registers)]
        return out

    def standard_error(self) -> float:
        return 1.04 / math.sqrt(self.m)

    def bytes_used(self) -> int:
        """One byte per register is enough: ranks never exceed 64."""
        return self.m


def report(label: str, estimate: float, truth: int) -> None:
    error = (estimate - truth) / truth * 100 if truth else 0.0
    print(f"  {label:<28} truth {truth:>8}  estimate {estimate:>12.1f}  "
          f"{error:+7.3f}%")


def main() -> None:
    hll = HyperLogLog(precision=14)
    print(f"precision 14 -> {hll.m} registers, {hll.bytes_used()} bytes, "
          f"expected error {hll.standard_error() * 100:.2f}%")

    print("\naccuracy as distinct items accumulate")
    seen = 0
    for target in (100, 1_000, 10_000, 50_000, 100_000):
        while seen < target:
            hll.add(f"item-{seen}")
            seen += 1
        report(f"{target} distinct", hll.count(), target)

    print(f"\nstoring 100000 exact strings would need roughly "
          f"{100_000 * 60 // 1024} KB; the sketch used "
          f"{hll.bytes_used() // 1024} KB")

    print("\nduplicates do not move the estimate")
    before = hll.count()
    for _ in range(3):
        for i in range(0, 100_000, 1000):
            hll.add(f"item-{i}")
    print(f"  before {before:.1f}, after 300 re-adds {hll.count():.1f}")

    print("\nprecision versus error at 100000 distinct items")
    for p in (8, 10, 12, 14, 16):
        h = HyperLogLog(p)
        h.update(f"item-{i}" for i in range(100_000))
        err = (h.count() - 100_000) / 100_000 * 100
        print(f"  p={p:>2}: {h.m:>6} registers, {h.bytes_used() // 1024:>3} KB, "
              f"estimate {h.count():>10.1f}  {err:+7.3f}%  "
              f"(expected +-{h.standard_error() * 100:.2f}%)")

    print("\nsmall ranges rely on linear counting")
    for n in (1, 5, 50, 500, 2000):
        h = HyperLogLog(10)
        h.update(range(n))
        report(f"n = {n} at p=10", h.count(), n)

    print("\nmerging is a register-wise maximum")
    a, b = HyperLogLog(12), HyperLogLog(12)
    a.update(f"u{i}" for i in range(30_000))
    b.update(f"u{i}" for i in range(20_000, 60_000))  # 10000 shared
    merged = a.merge(b)
    report("A (30000)", a.count(), 30_000)
    report("B (40000)", b.count(), 40_000)
    report("A union B (60000)", merged.count(), 60_000)
    # Inclusion-exclusion on sketches is noisy but shows the intersection idea.
    print(f"  inferred intersection: "
          f"{a.count() + b.count() - merged.count():.1f} (true 10000)")

    print("\nedge cases")
    empty = HyperLogLog(10)
    print(f"  empty sketch counts {empty.count():.1f}")
    one = HyperLogLog(10)
    one.add("solo")
    one.add("solo")
    print(f"  one distinct item added twice: {one.count():.4f}")
    mixed = HyperLogLog(10)
    mixed.update([1, "1", (1,), 1.0])
    print(f"  int 1, str '1', tuple, float distinguished: {mixed.count():.4f}")
    try:
        HyperLogLog(3)
    except ValueError as exc:
        print(f"  precision 3: ValueError({exc})")
    try:
        HyperLogLog(10).merge(HyperLogLog(11))
    except ValueError as exc:
        print(f"  mismatched merge: ValueError({exc})")


if __name__ == "__main__":
    main()
