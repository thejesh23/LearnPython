"""Puzzles as graph search: a start state, a moves function and a goal test are
the whole interface, and breadth-first search returns a shortest solution."""

from collections import deque
from collections.abc import Callable, Hashable, Iterable

Jugs = tuple[int, int]
Bank = tuple[int, int, int]  # missionaries, cannibals, boat (1 = on the start bank)
Board = tuple[int, ...]  # tiles row by row, 0 is the blank


def bfs_solve[S: Hashable](
    start: S, is_goal: Callable[[S], bool], moves: Callable[[S], Iterable[S]]
) -> list[S] | None:
    """Shortest sequence of states from ``start`` to a goal, or None if unreachable."""
    parent: dict[S, S | None] = {start: None}  # doubles as the visited set
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if is_goal(state):
            path = [state]
            while (prev := parent[path[-1]]) is not None:
                path.append(prev)
            return path[::-1]
        for nxt in moves(state):
            if nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)
    return None


def jug_moves(cap_a: int, cap_b: int) -> Callable[[Jugs], list[Jugs]]:
    """Fill, empty or pour between two jugs with the given capacities."""

    def moves(state: Jugs) -> list[Jugs]:
        a, b = state
        ab, ba = min(a, cap_b - b), min(b, cap_a - a)
        return [(cap_a, b), (a, cap_b), (0, b), (a, 0), (a - ab, b + ab), (a + ba, b - ba)]

    return moves


def solve_jugs(cap_a: int, cap_b: int, target: int) -> list[Jugs] | None:
    """Fewest steps until either jug holds exactly ``target`` litres."""
    return bfs_solve((0, 0), lambda s: target in s, jug_moves(cap_a, cap_b))


def missionaries_moves(state: Bank) -> list[Bank]:
    """Boat carries one or two; missionaries are never outnumbered on either bank."""
    m, c, boat = state
    sign = -1 if boat else 1  # the boat takes people away from its own bank
    out = []
    for dm, dc in ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1)):
        nm, nc = m + sign * dm, c + sign * dc
        # Safe on both banks means: all missionaries on one side, or equal numbers.
        if 0 <= nm <= 3 and 0 <= nc <= 3 and nm in (0, 3, nc):
            out.append((nm, nc, 1 - boat))
    return out


def solve_missionaries() -> list[Bank] | None:
    """Three missionaries and three cannibals cross with a two-seat boat."""
    return bfs_solve((3, 3, 1), lambda s: s == (0, 0, 0), missionaries_moves)


def sliding_moves(cols: int) -> Callable[[Board], list[Board]]:
    """Slide a tile into the blank on a board ``cols`` wide."""

    def moves(board: Board) -> list[Board]:
        blank, rows = board.index(0), len(board) // cols
        r, c = divmod(blank, cols)
        out = []
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                tiles = list(board)
                tiles[blank], tiles[nr * cols + nc] = tiles[nr * cols + nc], 0
                out.append(tuple(tiles))
        return out

    return moves


def solve_sliding(board: Board, cols: int) -> list[Board] | None:
    """Shortest slide sequence to 1, 2, ..., n-1 followed by the blank."""
    goal = tuple(range(1, len(board))) + (0,)
    return bfs_solve(board, goal.__eq__, sliding_moves(cols))
