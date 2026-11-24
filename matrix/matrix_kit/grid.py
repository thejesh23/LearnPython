"""Functions on plain list-of-lists grids: walks and in-place transforms."""

Grid = list[list[int]]


def spiral(m: Grid) -> list[int]:
    """Clockwise spiral from the top-left, using four shrinking walls."""
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


def rotate_in_place(m: Grid, clockwise: bool = True) -> None:
    """Square grids only: transpose, then reverse rows (or row order)."""
    n = len(m)
    if any(len(row) != n for row in m):
        raise ValueError("in-place rotation needs a square grid")
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    if clockwise:
        for row in m:
            row.reverse()
    else:
        m.reverse()


def set_zeroes(m: Grid) -> None:
    """Clear the row and column of every original zero, in O(1) extra space."""
    if not m or not m[0]:
        return
    rows, cols = len(m), len(m[0])
    first_row = any(v == 0 for v in m[0])
    first_col = any(m[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if m[r][c] == 0:
                m[r][0] = m[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if m[r][0] == 0 or m[0][c] == 0:
                m[r][c] = 0
    if first_row:
        m[0] = [0] * cols
    if first_col:
        for r in range(rows):
            m[r][0] = 0
