"""Set matrix zeroes: wherever a cell is 0, clear its whole row and column.

The trap is clearing while scanning: a freshly written zero looks like an
original one and wipes out rows it should not. The simple fix records which
rows and columns to clear in two sets first (O(rows + cols) extra space), then
clears in a second pass.

The O(1)-space version reuses the first row and first column as those marker
sets. Since they are also real data, remember up front whether each of them
held a zero, mark into them while scanning the rest, clear the inner cells
from the markers, and only then clear the first row and column themselves.
The order of those last steps is the whole difficulty.
"""

import random

Matrix = list[list[int]]


def set_zeroes_with_sets(m: Matrix) -> None:
    rows = {r for r, row in enumerate(m) for v in row if v == 0}
    cols = {c for row in m for c, v in enumerate(row) if v == 0}
    for r, row in enumerate(m):
        for c in range(len(row)):
            if r in rows or c in cols:
                row[c] = 0


def set_zeroes_constant_space(m: Matrix) -> None:
    if not m or not m[0]:
        return
    rows, cols = len(m), len(m[0])
    first_row_zero = any(v == 0 for v in m[0])
    first_col_zero = any(m[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if m[r][c] == 0:
                m[r][0] = m[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if m[r][0] == 0 or m[0][c] == 0:
                m[r][c] = 0
    if first_row_zero:
        m[0] = [0] * cols
    if first_col_zero:
        for r in range(rows):
            m[r][0] = 0


def set_zeroes_buggy(m: Matrix) -> None:
    """Clears while scanning, so new zeros cascade."""
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v == 0:
                m[r] = [0] * len(row)
                for rr in range(len(m)):
                    m[rr][c] = 0


def show(label: str, m: Matrix) -> None:
    print(label)
    for row in m:
        print("  " + " ".join(str(v) for v in row))


def main() -> None:
    grid = [[1, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 0], [1, 1, 1, 1]]
    show("input:", grid)

    a = [row[:] for row in grid]
    set_zeroes_constant_space(a)
    show("constant space:", a)

    b = [row[:] for row in grid]
    set_zeroes_buggy(b)
    show("clearing while scanning (wrong):", b)

    corner = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    set_zeroes_constant_space(corner)
    show("zero in the corner:", corner)

    rng = random.Random(7)
    ok = True
    for _ in range(500):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        m = [[rng.choice([0, 1, 1, 1, 2]) for _ in range(cols)] for _ in range(rows)]
        x, y = [r[:] for r in m], [r[:] for r in m]
        set_zeroes_with_sets(x)
        set_zeroes_constant_space(y)
        ok &= x == y
    print(f"\nconstant space matches the set version on 500 random grids: {ok}")


if __name__ == "__main__":
    main()
