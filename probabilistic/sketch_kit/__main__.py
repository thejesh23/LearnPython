"""Examples and self-check: python3 -m probabilistic.sketch_kit"""

import math
import random
import sys
from collections import Counter

from . import (
    CountMinSketch,
    HyperLogLog,
    MinHash,
    estimate_pi,
    jaccard,
    mc_integrate,
    reservoir_sample,
    shingles,
    stratified_integrate,
)


def zipf_words(n: int, vocabulary: int, rng: random.Random) -> list[str]:
    """A skewed stream: word i appears with weight 1/(i+1)."""
    weights = [1 / (i + 1) for i in range(vocabulary)]
    return [f"w{i}" for i in rng.choices(range(vocabulary), weights, k=n)]


def examples() -> None:
    rng = random.Random(1)
    stream = zipf_words(20_000, 2000, rng)
    truth = Counter(stream)
    cms = CountMinSketch.with_error(epsilon=0.001, delta=0.01)
    for word in stream:
        cms.add(word)
    top = [(w, truth[w], cms.estimate(w)) for w, _ in truth.most_common(3)]
    print("1. count-min (word, true, estimate):", top)

    hll = HyperLogLog(precision=12)
    for i in range(30_000):
        hll.add(f"user-{i}")
    print(f"2. HyperLogLog: 30000 distinct users -> {hll.count():.0f} using {hll.m} registers")

    a, b = HyperLogLog(12), HyperLogLog(12)
    for i in range(10_000):
        a.add(i)
        b.add(i + 5_000)
    print(f"3. merged HyperLogLog of two overlapping sets (truth 15000): {a.merge(b).count():.0f}")

    docs = ["the quick brown fox jumps over the lazy dog near the river bank",
            "the quick brown fox leaps over the lazy dog near the river bank",
            "grammars of programming languages describe the syntax of valid code"]
    sets = [shingles(d) for d in docs]
    mh = MinHash(num_hashes=256)
    sigs = [mh.signature(s) for s in sets]
    print(f"4. MinHash vs exact Jaccard: near-duplicates {mh.similarity(sigs[0], sigs[1]):.2f}"
          f" vs {jaccard(sets[0], sets[1]):.2f}, unrelated {mh.similarity(sigs[0], sigs[2]):.2f}")

    print("5. reservoir sample of 5 from a million:", reservoir_sample(range(1_000_000), 5, rng))
    print("6. pi from 50000 darts:", estimate_pi(50_000, random.Random(2)))
    plain, err = mc_integrate(math.sin, 0, math.pi, 2000, random.Random(3))
    strat = stratified_integrate(math.sin, 0, math.pi, 2000, random.Random(3))
    print(f"7. integral of sin over [0, pi] (exact 2): plain {plain:.4f} +/- {err:.4f},"
          f" stratified {strat:.6f}")


def self_check() -> None:
    rng = random.Random(42)
    stream = zipf_words(10_000, 500, rng)
    cms = CountMinSketch(width=200, depth=4, seed=7)
    for word in stream:
        cms.add(word)
    truth = Counter(stream)
    bound = math.e / 200 * len(stream)
    over = [cms.estimate(w) - truth[w] for w in truth]
    assert min(over) >= 0, "count-min undercounted"
    assert sum(o > bound for o in over) <= 0.05 * len(over)  # delta = e^-4 < 2%

    for n in (0, 10, 1000, 20_000):
        hll = HyperLogLog(12)
        for i in range(n):
            hll.add(rng.random())
        if n:
            assert abs(hll.count() - n) / n < 0.06, (n, hll.count())  # ~3.5 sigma
        else:
            assert hll.count() == 0
    try:
        HyperLogLog(10).merge(HyperLogLog(11))
    except ValueError:
        pass
    else:
        raise AssertionError("merged different precisions")

    universe = list(range(400))
    mh = MinHash(num_hashes=200, seed=3)
    for _ in range(10):
        a = set(rng.sample(universe, 120))
        b = set(rng.sample(universe, 120))
        estimate = mh.similarity(mh.signature(a), mh.signature(b))
        assert abs(estimate - jaccard(a, b)) < 0.15  # ~4 standard errors
    assert mh.signature(a) == mh.signature(set(a)), "signature must be deterministic"
    assert jaccard(set(), set()) == 1.0 and shingles("") == set()

    counts = Counter()
    for _ in range(4000):
        counts.update(reservoir_sample(range(10), 3, rng))
    assert all(abs(c - 1200) < 150 for c in counts.values()), counts  # ideal 4000 * 3 / 10
    assert reservoir_sample([1, 2], 5, rng) == [1, 2] and reservoir_sample([1], 0, rng) == []

    assert abs(estimate_pi(20_000, rng) - math.pi) < 0.06
    value, err = mc_integrate(lambda x: x * x, 0, 3, 5000, rng)
    assert abs(value - 9) < 4 * err
    assert abs(stratified_integrate(lambda x: x * x, 0, 3, 5000, rng) - 9) < 0.01


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
