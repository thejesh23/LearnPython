"""Sudoku by backtracking over bitmask candidates, most-constrained cell first.

Rows, columns and boxes each keep a 9-bit mask of the digits they already
hold, so a cell's candidates are ``ALL & ~(row | col | box)``. Branching on the
empty cell with the fewest candidates fails fast and, when a cell has a single
candidate, behaves exactly like constraint propagation.
"""

from collections.abc import Sequence

Grid = list[list[int]]
ALL = 0b1111111110  # bits 1..9, so digit d is bit d


def solve_sudoku(grid: Sequence[Sequence[int]]) -> Grid | None:
    """A solved copy of a 9x9 grid (0 = empty), or None if it has no solution."""
    board = [list(row) for row in grid]
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for r in range(9):
        for c in range(9):
            if d := board[r][c]:
                bit, b = 1 << d, r // 3 * 3 + c // 3
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return None  # the givens already clash
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit

    def candidates(r: int, c: int) -> int:
        return ALL & ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3])

    def most_constrained() -> tuple[int, int, int] | None:
        best: tuple[int, int, int] | None = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    mask = candidates(r, c)
                    if best is None or mask.bit_count() < best[2].bit_count():
                        best = (r, c, mask)
                        if mask.bit_count() <= 1:
                            return best  # forced or dead: no need to look further
        return best

    def fill() -> bool:
        cell = most_constrained()
        if cell is None:
            return True  # no empty cells left
        r, c, best_mask = cell
        b = r // 3 * 3 + c // 3
        for d in range(1, 10):
            bit = 1 << d
            if best_mask & bit:
                board[r][c] = d
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
                if fill():
                    return True
                rows[r] ^= bit
                cols[c] ^= bit
                boxes[b] ^= bit
        board[r][c] = 0
        return False

    return board if fill() else None


def is_solved(grid: Sequence[Sequence[int]]) -> bool:
    """True if every row, column and 3x3 box holds exactly the digits 1-9."""
    digits = set(range(1, 10))
    units = [list(row) for row in grid]
    units += [[grid[r][c] for r in range(9)] for c in range(9)]
    units += [[grid[br + r][bc + c] for r in range(3) for c in range(3)]
              for br in (0, 3, 6) for bc in (0, 3, 6)]
    return len(grid) == 9 and all(set(u) == digits and len(u) == 9 for u in units)
