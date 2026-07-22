"""Segment tree: range queries *and* point updates, both O(log n).

A prefix-sum array answers range sums in O(1) but costs O(n) per update. A
segment tree gives up a little query speed to make updates logarithmic too —
the right trade whenever the data changes.

Each node stores the aggregate of a range; the leaves are the elements. The
iterative array layout below (size 2n, leaves at n..2n-1) needs no recursion
and no pointers.

Any associative operation works: sum, min, max, gcd. Swap `combine`.
"""


class SegmentTree:
    def __init__(self, values: list[int], combine=lambda a, b: a + b, identity: int = 0) -> None:
        self.n = len(values)
        self.combine = combine
        self.identity = identity
        self.tree = [identity] * (2 * self.n)
        self.tree[self.n:] = values
        for i in range(self.n - 1, 0, -1):  # build parents bottom-up
            self.tree[i] = combine(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index: int, value: int) -> None:
        i = index + self.n
        self.tree[i] = value
        while i > 1:  # walk up, refreshing each ancestor
            i //= 2
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, lo: int, hi: int) -> int:
        """Aggregate over [lo, hi) — half-open, like a slice."""
        result_left = result_right = self.identity
        lo += self.n
        hi += self.n
        while lo < hi:
            if lo & 1:  # lo is a right child: take it and move past
                result_left = self.combine(result_left, self.tree[lo])
                lo += 1
            if hi & 1:  # hi is a right child: step back and take it
                hi -= 1
                result_right = self.combine(self.tree[hi], result_right)
            lo //= 2
            hi //= 2
        return self.combine(result_left, result_right)


def main() -> None:
    values = [1, 3, 5, 7, 9, 11]
    sums = SegmentTree(values)
    print(f"values      = {values}")
    print(f"sum[1:4)    = {sums.query(1, 4)}  (check {sum(values[1:4])})")
    print(f"sum[0:6)    = {sums.query(0, 6)}")

    sums.update(1, 10)  # values[1] = 10
    values[1] = 10
    print(f"after update, sum[1:4) = {sums.query(1, 4)} (check {sum(values[1:4])})")

    mins = SegmentTree(values, combine=min, identity=float("inf"))
    print(f"min[0:6)    = {mins.query(0, 6)}")
    print(f"min[2:5)    = {mins.query(2, 5)}  (check {min(values[2:5])})")

    from math import gcd

    gcds = SegmentTree([12, 18, 24, 30], combine=gcd, identity=0)
    print(f"gcd[0:4)    = {gcds.query(0, 4)}")

    print("prefix sums: O(1) query, O(n) update | segment tree: O(log n) both")


if __name__ == "__main__":
    main()
