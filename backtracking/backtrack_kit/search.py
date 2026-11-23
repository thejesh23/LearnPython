"""Backtracking searches: choose, recurse, undo — and prune as early as possible.

Each search keeps one mutable partial solution, extends it by one choice,
recurses, then undoes the choice. Pruning means rejecting a partial solution
before its whole subtree is explored.
"""

from collections.abc import Callable, Sequence
from itertools import accumulate
from typing import Any


def n_queens(n: int, limit: int | None = None) -> list[list[int]]:
    """Every placement of n non-attacking queens, as a column per row.

    Diagonals are indexed by row - col and row + col, so each conflict test is
    a set lookup. Stops after ``limit`` solutions when given.
    """
    solutions: list[list[int]] = []
    cols: list[int] = []
    used_cols: set[int] = set()
    diag: set[int] = set()  # row - col is constant along a diagonal
    anti: set[int] = set()  # row + col is constant along an anti-diagonal

    def place(row: int) -> None:
        if limit is not None and len(solutions) >= limit:
            return
        if row == n:
            solutions.append(list(cols))
            return
        for col in range(n):
            if col in used_cols or row - col in diag or row + col in anti:
                continue
            cols.append(col)
            used_cols.add(col)
            diag.add(row - col)
            anti.add(row + col)
            place(row + 1)
            cols.pop()
            used_cols.discard(col)
            diag.discard(row - col)
            anti.discard(row + col)

    place(0)
    return solutions


def subset_sums(numbers: Sequence[int], target: int) -> list[list[int]]:
    """Every distinct subset (as a sorted list) of non-negative numbers summing to target.

    Sorted input lets the loop stop at the first number that is too big, and a
    suffix sum stops branches that cannot reach the target even taking the rest.
    """
    if any(x < 0 for x in numbers):
        raise ValueError("pruning assumes non-negative numbers")
    nums = sorted(numbers)
    suffix = list(accumulate(reversed(nums)))[::-1] + [0]
    found: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int, need: int) -> None:
        if need == 0:
            found.append(list(chosen))  # no return: zeros could still extend it
        for i in range(start, len(nums)):
            if nums[i] > need or suffix[i] < need:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue  # same value at the same depth gives the same subsets
            chosen.append(nums[i])
            extend(i + 1, need - nums[i])
            chosen.pop()

    extend(0, target)
    return found


def permutations_where(items: Sequence[Any], prefix_ok: Callable[[list[Any]], bool]) -> list[list[Any]]:
    """Orderings of items whose every prefix passes ``prefix_ok``.

    The rule is checked on each partial ordering, so one bad prefix cuts off
    all (n - k)! of its completions instead of filtering them one by one.
    """
    out: list[list[Any]] = []
    used = [False] * len(items)
    prefix: list[Any] = []

    def extend() -> None:
        if len(prefix) == len(items):
            out.append(list(prefix))
            return
        for i, x in enumerate(items):
            if used[i]:
                continue
            prefix.append(x)
            if prefix_ok(prefix):
                used[i] = True
                extend()
                used[i] = False
            prefix.pop()

    extend()
    return out


def word_path(grid: Sequence[str], word: str) -> list[tuple[int, int]] | None:
    """Cells spelling ``word`` through up/down/left/right steps, each cell used once."""
    rows, cols = len(grid), len(grid[0]) if grid else 0
    path: list[tuple[int, int]] = []

    def walk(r: int, c: int, k: int) -> bool:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != word[k] or (r, c) in path:
            return False
        path.append((r, c))
        if k == len(word) - 1 or any(
            walk(r + dr, c + dc, k + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ):
            return True
        path.pop()  # undo: this cell is free again for other routes
        return False

    if not word:
        return []
    for r in range(rows):
        for c in range(cols):
            if walk(r, c, 0):
                return path
    return None
