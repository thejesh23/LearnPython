"""Examples and self-check: python3 -m greedy.greedy_kit"""

import itertools
import random
import sys
from collections import deque

from . import (
    assign_rooms,
    decode,
    encode,
    fractional_knapsack,
    huffman_codes,
    min_jumps,
    min_rooms,
    select_activities,
)

TALKS = [("a", 1, 4), ("b", 3, 5), ("c", 0, 6), ("d", 5, 7), ("e", 3, 9),
         ("f", 5, 9), ("g", 6, 10), ("h", 8, 11), ("i", 8, 12), ("j", 2, 14)]


def compatible(chosen: list[tuple[str, int, int]]) -> bool:
    """No two intervals overlap (touching endpoints are fine)."""
    ordered = sorted(chosen, key=lambda a: a[1])
    return all(a[2] <= b[1] for a, b in zip(ordered, ordered[1:]))


def bfs_jumps(nums: list[int]) -> int | None:
    """Reference answer: plain BFS over indices."""
    dist = {0: 0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(i + 1, min(i + nums[i], len(nums) - 1) + 1):
            if j not in dist:
                dist[j] = dist[i] + 1
                queue.append(j)
    return dist.get(len(nums) - 1)


def examples() -> None:
    print("1. activities:", [a[0] for a in select_activities(TALKS)])
    rooms = assign_rooms(TALKS)
    print("2. rooms needed:", min_rooms(TALKS), {r: [m[0] for m in ms] for r, ms in rooms.items()})
    print("3. fewest jumps:", min_jumps([2, 3, 1, 1, 4]), "| stuck:", min_jumps([3, 2, 1, 0, 4]))
    value, taken = fractional_knapsack([("a", 60, 10), ("b", 100, 20), ("c", 120, 30)], 50)
    print("4. fractional knapsack:", value, [(n, round(f, 3)) for n, f in taken])
    text = "abracadabra"
    codes = huffman_codes(text)
    bits = encode(text, codes)
    print("5. Huffman codes:", dict(sorted(codes.items())))
    print(f"6. {text!r} -> {bits} ({len(bits)} bits vs {8 * len(text)} as bytes) -> {decode(bits, codes)!r}")


def self_check() -> None:
    rng = random.Random(8)
    for _ in range(200):
        starts = [rng.randint(0, 15) for _ in range(rng.randint(0, 8))]
        spans = [(str(i), s, s + rng.randint(1, 6)) for i, s in enumerate(starts)]
        chosen = select_activities(spans)
        best = max(r for r in range(len(spans) + 1)
                   if any(compatible(list(c)) for c in itertools.combinations(spans, r)))
        assert compatible(chosen) and len(chosen) == best
        peak = max((sum(s <= t < e for _, s, e in spans) for t in range(25)), default=0)
        rooms = assign_rooms(spans)
        assert min_rooms(spans) == peak and all(compatible(ms) for ms in rooms.values())
        assert sorted(m for ms in rooms.values() for m in ms) == sorted(spans)
        nums = [rng.randint(0, 3) for _ in range(rng.randint(1, 12))]
        assert min_jumps(nums) == bfs_jumps(nums), nums
        items = [(str(i), rng.randint(1, 30), rng.randint(1, 8)) for i in range(rng.randint(1, 6))]
        cap = rng.randint(0, 30)
        # Brute force: split every item into unit-weight pieces, take the best `cap` of them.
        pieces = sorted((v / w for _, v, w in items for _ in range(w)), reverse=True)
        value, taken = fractional_knapsack(items, cap)
        assert abs(value - sum(pieces[:cap])) < 1e-9
        weight = {name: w for name, _, w in items}
        assert sum(f * weight[name] for name, f in taken) <= cap + 1e-9
        assert all(0 < f <= 1 for _, f in taken)
        text = "".join(rng.choice("aaaabbbccd") for _ in range(rng.randint(1, 40)))
        codes = huffman_codes(text)
        assert decode(encode(text, codes), codes) == text
        assert not any(a != b and b.startswith(a) for a, b in itertools.permutations(codes.values(), 2))
        if len(codes) > 1:  # a full binary tree: Kraft sum is exactly 1
            assert sum(2.0 ** -len(c) for c in codes.values()) == 1.0
    assert len(encode("abracadabra", huffman_codes("abracadabra"))) == 23
    assert huffman_codes("") == {} and min_jumps([0]) == 0


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
