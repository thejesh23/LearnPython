"""Reading a matrix in spiral order, and writing one back.

Keep four walls: top, bottom, left and right. Walk the top row left to right
and move the top wall down; walk the right column downward and move the right
wall in; then the bottom row backward and the left column upward. Repeat until
the walls cross. Every cell is visited once, so the cost is O(rows * cols).

The only trap is a single leftover row or column in the middle of a
non-square matrix: after the first two legs, the bottom and left legs must
check the walls again or they will revisit cells. The direction-turning
version avoids wall bookkeeping by turning right whenever the next cell is out
of bounds or already seen, at the cost of a visited grid.
"""

Matrix = list[list[int]]


def spiral(m: Matrix) -> list[int]:
    out: list[int] = []
    if not m or not m[0]:
        return out
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bottom and left <= right:
        out.extend(m[top][c] for c in range(left, right + 1))
        top += 1
        out.extend(m[r][right] for r in range(top, bottom + 1))
        right -= 1
        if top <= bottom:
            out.extend(m[bottom][c] for c in range(right, left - 1, -1))
            bottom -= 1
        if left <= right:
            out.extend(m[r][left] for r in range(bottom, top - 1, -1))
            left += 1
    return out


def spiral_by_turning(m: Matrix) -> list[int]:
    if not m or not m[0]:
        return []
    rows, cols = len(m), len(m[0])
    seen = [[False] * cols for _ in range(rows)]
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = d = 0
    out: list[int] = []
    for _ in range(rows * cols):
        out.append(m[r][c])
        seen[r][c] = True
        nr, nc = r + moves[d][0], c + moves[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols) or seen[nr][nc]:
            d = (d + 1) % 4
            nr, nc = r + moves[d][0], c + moves[d][1]
        r, c = nr, nc
    return out


def fill_spiral(n: int) -> Matrix:
    """The inverse: write 1..n*n into an n x n grid in spiral order."""
    grid = [[0] * n for _ in range(n)]
    cells = [(r, c) for r in range(n) for c in range(n)]
    index = [[r * n + c for c in range(n)] for r in range(n)]
    for value, flat in enumerate(spiral(index), start=1):
        r, c = cells[flat]
        grid[r][c] = value
    return grid


def main() -> None:
    m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    print(f"3x4:      {spiral(m)}")
    print(f"column:   {spiral([[1], [2], [3]])}")
    print(f"row:      {spiral([[1, 2, 3]])}")
    print(f"empty:    {spiral([])}")

    print("\nfill_spiral(4):")
    for row in fill_spiral(4):
        print("  " + " ".join(f"{v:2}" for v in row))

    shapes = [(r, c) for r in range(1, 8) for c in range(1, 8)]
    agree = all(
        spiral(g) == spiral_by_turning(g)
        for r, c in shapes
        for g in [[[i * c + j for j in range(c)] for i in range(r)]]
    )
    print(f"\nwalls and turning agree on every shape up to 7x7: {agree}")


if __name__ == "__main__":
    main()
