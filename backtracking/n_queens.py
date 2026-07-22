"""N queens: place N queens on an N x N board so that none attacks another.

Backtracking works row by row. Each row holds exactly one queen, so the only
choice is which column, and a partial placement is extended only if the new
queen conflicts with nothing already placed. When no column works, the search
returns and the previous row tries its next column.

The trick that makes conflict checking O(1) is indexing the two diagonals
arithmetically. Cells on the same anti-diagonal share row + col; cells on the
same main diagonal share row - col. Keeping three sets — used columns, used
row+col, used row-col — turns the test into three membership checks, and undoing
a placement is three discards.

The search is still exponential in the worst case, but pruning is aggressive
enough that N=8 finishes instantly. Solution counts grow irregularly: 1, 0, 0,
2, 10, 4, 40, 92 for N=1..8.
"""


def solve_n_queens(n: int, limit: int | None = None) -> list[list[int]]:
    """Return placements as column-per-row lists; stop after `limit` if given."""
    solutions: list[list[int]] = []
    placement: list[int] = []
    cols: set[int] = set()
    diag: set[int] = set()       # row - col
    anti: set[int] = set()       # row + col

    def recurse(row: int) -> None:
        if limit is not None and len(solutions) >= limit:
            return
        if row == n:
            solutions.append(list(placement))
            return
        for col in range(n):
            if col in cols or row - col in diag or row + col in anti:
                continue
            cols.add(col)
            diag.add(row - col)
            anti.add(row + col)
            placement.append(col)
            recurse(row + 1)
            placement.pop()
            cols.discard(col)
            diag.discard(row - col)
            anti.discard(row + col)

    recurse(0)
    return solutions


def count_solutions(n: int) -> int:
    return len(solve_n_queens(n))


def render(placement: list[int]) -> str:
    n = len(placement)
    return "\n".join(
        "".join("Q" if placement[r] == c else "." for c in range(n))
        for r in range(n)
    )


def is_valid(placement: list[int]) -> bool:
    n = len(placement)
    return all(
        placement[r] != placement[s] and abs(placement[r] - placement[s]) != s - r
        for r in range(n)
        for s in range(r + 1, n)
    )


def main() -> None:
    for n in range(1, 9):
        print(f"N={n}: {count_solutions(n)} solutions")

    first = solve_n_queens(8, limit=1)[0]
    print(f"\nfirst 8-queens solution, columns by row: {first}")
    print(render(first))
    print(f"valid: {is_valid(first)}")

    # N=2 and N=3 are the classic impossible cases.
    print(f"\nN=2 solutions: {solve_n_queens(2)}")
    print(f"N=3 solutions: {solve_n_queens(3)}")
    print(f"N=4 solutions: {solve_n_queens(4)}")
    print(f"all 92 N=8 solutions valid: {all(is_valid(p) for p in solve_n_queens(8))}")


if __name__ == "__main__":
    main()
