"""2-D Fenwick tree: rectangle sums with point updates in O(log^2 n).

The one-dimensional Fenwick tree walks a single index by stripping or adding the
lowest set bit. In two dimensions the same walk runs in both coordinates,
nested — so a point update touches O(log rows * log cols) cells, and a prefix
rectangle sum reads the same number.

A rectangle [r1, r2) x [c1, c2) comes from four prefix sums by
inclusion-exclusion, exactly as a 2-D prefix-sum array does — but here the grid
can be updated cheaply, which a static prefix-sum array cannot.

Build O(rows * cols), each update and each query O(log rows * log cols).
"""


class Fenwick2D:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]  # 1-indexed

    def add(self, r: int, c: int, delta: int) -> None:
        i = r + 1
        while i <= self.rows:
            j = c + 1
            while j <= self.cols:
                self.tree[i][j] += delta
                j += j & -j
            i += i & -i

    def _prefix(self, r: int, c: int) -> int:
        """Sum over the rectangle [0, r) x [0, c)."""
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= j & -j
            i -= i & -i
        return total

    def range_sum(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Sum over [r1, r2) x [c1, c2), by inclusion-exclusion of four corners."""
        return (self._prefix(r2, c2) - self._prefix(r1, c2)
                - self._prefix(r2, c1) + self._prefix(r1, c1))


def main() -> None:
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    rows, cols = len(grid), len(grid[0])
    fen = Fenwick2D(rows, cols)
    for r in range(rows):
        for c in range(cols):
            fen.add(r, c, grid[r][c])

    def brute(r1: int, c1: int, r2: int, c2: int) -> int:
        return sum(grid[r][c] for r in range(r1, r2) for c in range(c1, c2))

    for rect in [(0, 0, 2, 2), (1, 1, 4, 4), (0, 0, 4, 4), (2, 2, 3, 3)]:
        got = fen.range_sum(*rect)
        print(f"  rectangle {rect} -> {got} (check {brute(*rect)})")

    # Point update: bump a cell and re-query.
    fen.add(1, 1, 100)
    grid[1][1] += 100
    print(f"after adding 100 at (1,1): rectangle (0,0,2,2) -> "
          f"{fen.range_sum(0, 0, 2, 2)} (check {brute(0, 0, 2, 2)})")

    # Exhaustive cross-check over every rectangle.
    ok = all(
        fen.range_sum(r1, c1, r2, c2) == brute(r1, c1, r2, c2)
        for r1 in range(rows + 1) for r2 in range(r1, rows + 1)
        for c1 in range(cols + 1) for c2 in range(c1, cols + 1)
    )
    print(f"all rectangles correct: {ok}")


if __name__ == "__main__":
    main()
