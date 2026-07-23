"""Square-root decomposition: block the array so both query and update are O(sqrt n).

Split n elements into blocks of size about sqrt(n) and keep a per-block
aggregate (here, a sum). A range query touches at most two partial blocks
element by element and every fully covered block once, so it visits O(sqrt n)
things. A point update fixes one element and one block aggregate in O(1).

It sits between a prefix-sum array (O(1) query, O(n) update) and a segment tree
(O(log n) both). What it lacks in asymptotics it makes up in simplicity, and it
generalises to queries a segment tree cannot easily do — which is the whole
idea behind Mo's algorithm, sketched at the end.

Choosing the block size as sqrt(n) balances the two O(sqrt n) halves of a query.
"""

import math


class SqrtDecomposition:
    def __init__(self, values: list[int]) -> None:
        self.a = list(values)
        self.n = len(values)
        self.block = max(1, int(math.isqrt(self.n)))
        self.block_sum = [0] * ((self.n + self.block - 1) // self.block)
        for i, v in enumerate(self.a):
            self.block_sum[i // self.block] += v

    def update(self, index: int, value: int) -> None:
        block = index // self.block
        self.block_sum[block] += value - self.a[index]
        self.a[index] = value

    def range_sum(self, lo: int, hi: int) -> int:
        """Sum over [lo, hi) — half-open, like a slice."""
        total = 0
        i = lo
        while i < hi and i % self.block != 0:  # leading partial block
            total += self.a[i]
            i += 1
        while i + self.block <= hi:  # whole blocks
            total += self.block_sum[i // self.block]
            i += self.block
        while i < hi:  # trailing partial block
            total += self.a[i]
            i += 1
        return total


def mo_algorithm(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Answer offline range queries by ordering them to move the window cheaply.

    Sorting queries by (block of lo, hi) bounds the total pointer movement to
    O((n + q) sqrt n). Here the query is "count of distinct values in [lo, hi)".
    """
    block = max(1, int(math.isqrt(len(values))))
    order = sorted(
        range(len(queries)),
        key=lambda q: (queries[q][0] // block, queries[q][1]),
    )
    answers = [0] * len(queries)
    counts: dict[int, int] = {}
    distinct = 0
    cur_lo = cur_hi = 0

    def add(i: int) -> None:
        nonlocal distinct
        counts[values[i]] = counts.get(values[i], 0) + 1
        if counts[values[i]] == 1:
            distinct += 1

    def remove(i: int) -> None:
        nonlocal distinct
        counts[values[i]] -= 1
        if counts[values[i]] == 0:
            distinct -= 1

    for q in order:
        lo, hi = queries[q]
        while cur_hi < hi:
            add(cur_hi)
            cur_hi += 1
        while cur_lo > lo:
            cur_lo -= 1
            add(cur_lo)
        while cur_hi > hi:
            cur_hi -= 1
            remove(cur_hi)
        while cur_lo < lo:
            remove(cur_lo)
            cur_lo += 1
        answers[q] = distinct
    return answers


def main() -> None:
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    sd = SqrtDecomposition(values)
    print(f"block size: {sd.block}")
    print(f"sum[2:7)  = {sd.range_sum(2, 7)}  (check {sum(values[2:7])})")
    print(f"sum[0:11) = {sd.range_sum(0, 11)}  (check {sum(values)})")

    sd.update(4, 100)
    values[4] = 100
    print(f"after update index 4 to 100: sum[2:7) = {sd.range_sum(2, 7)} "
          f"(check {sum(values[2:7])})")

    # Cross-check every possible range against a direct sum.
    ok = all(
        sd.range_sum(lo, hi) == sum(values[lo:hi])
        for lo in range(12)
        for hi in range(lo, 12)
    )
    print(f"all ranges correct: {ok}")

    print("Mo's algorithm — distinct values per range, answered offline:")
    data = [1, 1, 2, 1, 3, 2, 4, 2]
    queries = [(0, 4), (2, 6), (0, 8), (4, 8)]
    answers = mo_algorithm(data, queries)
    for (lo, hi), got in zip(queries, answers):
        print(f"  [{lo}, {hi}) -> {got} distinct (check {len(set(data[lo:hi]))})")


if __name__ == "__main__":
    main()
