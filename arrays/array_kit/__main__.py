"""Examples and self-check: python3 -m arrays.array_kit"""

import itertools
import random
import sys
from collections import Counter

from . import (
    PrefixSums,
    count_subarrays_with_sum,
    majority,
    merge_intervals,
    move_zeroes,
    partition3,
    rotate,
    three_sum,
    two_sum,
    window_max,
)


def examples() -> None:
    print("1. two sum:", two_sum([2, 7, 11, 15], 9), two_sum([1, 2], 100))
    print("2. three sum to 0:", three_sum([-1, 0, 1, 2, -1, -4]))
    print("3. move zeroes:", move_zeroes([0, 1, 0, 3, 12]))
    print("4. Dutch flag:", partition3([2, 0, 2, 1, 1, 0], 1),
          "| around 5:", partition3([9, 3, 5, 1, 7, 5], 5))
    print("5. rotate right 3:", rotate([1, 2, 3, 4, 5, 6, 7], 3), "| left 2:", rotate([1, 2, 3, 4, 5], -2))
    sums = PrefixSums([3, 1, 4, 1, 5, 9, 2])
    print("6. prefix sums:", sums.prefix, "| sum of [2:5]:", sums.range_sum(2, 5))
    print("7. subarrays summing to 5:", count_subarrays_with_sum([1, 2, 3, 0, 5], 5))
    print("8. window max k=3:", window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
    print("9. majority:", majority([2, 2, 1, 1, 1, 2, 2]), majority([1, 2, 3]))
    print("10. merge intervals:", merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]))


def covered(intervals: list[tuple[int, int]]) -> set[int]:
    """Every point of the closed intervals, doubled so (1, 2) and (3, 4) leave a gap."""
    return {x for s, e in intervals for x in range(2 * s, 2 * e + 1)}


def self_check() -> None:
    rng = random.Random(11)
    for _ in range(300):
        a = [rng.randint(-6, 6) for _ in range(rng.randint(0, 12))]
        t = rng.randint(-8, 8)
        pair = two_sum(a, t)
        has_pair = any(a[i] + a[j] == t for i, j in itertools.combinations(range(len(a)), 2))
        assert (pair is not None) == has_pair and (pair is None or a[pair[0]] + a[pair[1]] == t)
        triples = {c for c in itertools.combinations(sorted(a), 3) if sum(c) == t}
        assert sorted(three_sum(a, t)) == sorted(triples)
        assert move_zeroes(a) == [x for x in a if x] + [0] * a.count(0)
        p = partition3(a, t)
        assert sorted(p) == sorted(a)
        assert p == [x for x in p if x < t] + [x for x in p if x == t] + [x for x in p if x > t]
        k = rng.randint(-20, 20)
        cut = len(a) - (k % len(a) if a else 0)
        assert rotate(a, k) == a[cut:] + a[:cut]
        sums = PrefixSums(a)
        lo, hi = sorted(rng.randint(0, len(a)) for _ in range(2))
        assert sums.range_sum(lo, hi) == sum(a[lo:hi])
        brute = sum(sum(a[i:j]) == t for i in range(len(a)) for j in range(i + 1, len(a) + 1))
        assert count_subarrays_with_sum(a, t) == brute
        w = rng.randint(1, 4)
        assert window_max(a, w) == [max(a[i:i + w]) for i in range(len(a) - w + 1)]
        top = Counter(a).most_common(1)
        assert majority(a) == (top[0][0] if top and top[0][1] > len(a) // 2 else None)
        spans = [tuple(sorted((rng.randint(0, 30), rng.randint(0, 30)))) for _ in range(rng.randint(0, 6))]
        merged = merge_intervals(spans)
        assert covered(merged) == covered(spans)
        assert all(a1[1] < b1[0] for a1, b1 in zip(merged, merged[1:]))


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
