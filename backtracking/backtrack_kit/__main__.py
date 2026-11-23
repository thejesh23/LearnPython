"""Examples and self-check: python3 -m backtracking.backtrack_kit"""

import itertools
import random
import sys

from . import is_solved, n_queens, permutations_where, solve_sudoku, subset_sums, word_path

PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
HARD = [[int(ch) for ch in row] for row in (
    "800000000", "003600000", "070090200", "050007000", "000045700",
    "000100030", "001000068", "008500010", "090000400",
)]
GRID = ["ABCE", "SFCS", "ADEE"]


def no_neighbours_adjacent(prefix: list[int]) -> bool:
    """Prefix rule: the newest value never differs from the one before it by 1."""
    return len(prefix) < 2 or abs(prefix[-1] - prefix[-2]) != 1


def examples() -> None:
    board = n_queens(6, limit=1)[0]
    print("1. a 6-queens board:", board)
    print("\n".join("   " + " ".join("Q" if c == col else "." for c in range(6)) for col in board))
    print("2. N-queens counts for N=1..8:", [len(n_queens(n)) for n in range(1, 9)])
    print("3. subsets of [3, 34, 4, 12, 5, 2] summing to 9:", subset_sums([3, 34, 4, 12, 5, 2], 9))
    perms = permutations_where([1, 2, 3, 4, 5], no_neighbours_adjacent)
    print(f"4. {len(perms)} of 120 orderings of 1..5 have no adjacent neighbours, e.g. {perms[0]}")
    print("5. word search 'ABCCED':", word_path(GRID, "ABCCED"), "| 'ABCB':", word_path(GRID, "ABCB"))
    solved = solve_sudoku(HARD)
    print("6. hard sudoku solved:", solved is not None and is_solved(solved))
    print("\n".join("   " + " ".join(map(str, row)) for row in solved or []))


def self_check() -> None:
    assert [len(n_queens(n)) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
    for q in n_queens(7):
        assert all(q[i] != q[j] and abs(q[i] - q[j]) != j - i for i, j in itertools.combinations(range(7), 2))
    rng = random.Random(3)
    for _ in range(200):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
        target = rng.randint(0, 25)
        brute = {c for r in range(len(nums) + 1)
                 for c in itertools.combinations(sorted(nums), r) if sum(c) == target}
        got = subset_sums(nums, target)
        assert len(got) == len(brute) and {tuple(s) for s in got} == brute
    items = list(range(6))
    expected = [list(p) for p in itertools.permutations(items)
                if all(abs(a - b) != 1 for a, b in zip(p, p[1:]))]
    assert permutations_where(items, no_neighbours_adjacent) == expected
    for _ in range(100):
        grid = ["".join(rng.choice("AB") for _ in range(4)) for _ in range(3)]
        r, c, walk = rng.randrange(3), rng.randrange(4), []
        while (r, c) not in walk and len(walk) < 6:  # a random self-avoiding walk
            walk.append((r, c))
            dr, dc = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            r, c = min(max(r + dr, 0), 2), min(max(c + dc, 0), 3)
        word = "".join(grid[r][c] for r, c in walk)
        path = word_path(grid, word)
        assert path is not None and len(set(path)) == len(word)
        assert "".join(grid[r][c] for r, c in path) == word
        assert all(abs(r1 - r2) + abs(c1 - c2) == 1 for (r1, c1), (r2, c2) in zip(path, path[1:]))
    assert word_path(GRID, "ABCB") is None and word_path(GRID, "") == []
    for puzzle in (PUZZLE, HARD):
        solved = solve_sudoku(puzzle)
        assert solved and is_solved(solved)
        assert all(puzzle[r][c] in (0, solved[r][c]) for r in range(9) for c in range(9))
    clash = [row[:] for row in PUZZLE]
    clash[0][2] = 5  # a second 5 in the first row
    assert solve_sudoku(clash) is None and PUZZLE[0][2] == 0


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
