"""Examples and self-check: python3 -m puzzles.puzzle_kit"""

import math
import random
import sys
from collections.abc import Callable, Hashable, Iterable

from . import (
    fizzbuzz,
    fizzbuzz_stream,
    from_picture,
    jug_moves,
    life_run,
    life_step,
    missionaries_moves,
    parse_rule,
    period,
    render,
    sliding_moves,
    solve_jugs,
    solve_missionaries,
    solve_sliding,
)

GLIDER = from_picture("""
    .#.
    ..#
    ###
""")


def examples() -> None:
    print("1. FizzBuzz 1-15:", " ".join(fizzbuzz_stream(15)))
    bazz = ((3, "Fizz"), (5, "Buzz"), (7, "Bazz"))
    print("   add a rule, not a branch:", [fizzbuzz(n, bazz) for n in (21, 35, 105)])
    print("2. jugs 4 and 3, measure 2:", solve_jugs(4, 3, 2), "| 3 from 4 and 6:", solve_jugs(4, 6, 3))
    crossings = solve_missionaries()
    print("3. missionaries and cannibals:", len(crossings) - 1, "crossings:", crossings)
    path = solve_sliding((4, 1, 3, 7, 2, 6, 0, 5, 8), 3)
    print("4. 8-puzzle solved in", len(path) - 1, "slides; blank moves through", [b.index(0) for b in path])
    print("   two tiles swapped on a 2x3 board is unsolvable:", solve_sliding((2, 1, 3, 4, 5, 0), 3))
    print("5. glider after 4 generations:")
    print("\n".join("   " + line for line in render(life_run(GLIDER, 4), 5, 5).splitlines()))
    blinker = {(1, 0), (1, 1), (1, 2)}
    print("6. (period, shift): glider", period(GLIDER), "| blinker", period(blinker))
    print("7. rules are data: 'B36/S23' (HighLife) ->", parse_rule("B36/S23"))


def min_moves[S: Hashable](
    start: S, is_goal: Callable[[S], bool], moves: Callable[[S], Iterable[S]]
) -> int | None:
    """Independent check on BFS: grow the set reachable within k moves until a goal appears."""
    reach, k = {start}, 0
    while not any(is_goal(s) for s in reach):
        bigger = reach | {nxt for s in reach for nxt in moves(s)}
        if bigger == reach:
            return None
        reach, k = bigger, k + 1
    return k


def assert_valid_path(path: list, moves: Callable) -> None:
    assert all(b in moves(a) for a, b in zip(path, path[1:])), path


def brute_life(live: set, born: frozenset, survive: frozenset) -> set:
    rows, cols = [r for r, _ in live] or [0], [c for _, c in live] or [0]
    nxt = set()
    for r in range(min(rows) - 1, max(rows) + 2):
        for c in range(min(cols) - 1, max(cols) + 2):
            n = sum((r + dr, c + dc) in live for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc)
            if n in (survive if (r, c) in live else born):
                nxt.add((r, c))
    return nxt


def self_check() -> None:
    for n in range(1, 301):
        want = "FizzBuzz" if n % 15 == 0 else "Fizz" if n % 3 == 0 else "Buzz" if n % 5 == 0 else str(n)
        assert fizzbuzz(n) == want
    for a in range(1, 8):  # jugs: solvable exactly when gcd divides target and it fits
        for b in range(1, 8):
            for target in range(max(a, b) + 2):
                path = solve_jugs(a, b, target)
                assert (path is not None) == (target <= max(a, b) and target % math.gcd(a, b) == 0)
                if path:
                    assert_valid_path(path, jug_moves(a, b))
                    assert len(path) - 1 == min_moves((0, 0), lambda s: target in s, jug_moves(a, b))
    crossings = solve_missionaries()
    assert_valid_path(crossings, missionaries_moves)
    assert len(crossings) - 1 == 11
    rng = random.Random(3)
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    for _ in range(15):  # scramble with random slides, BFS must find a shortest way back
        board = goal
        for _ in range(rng.randint(0, 12)):
            board = rng.choice(sliding_moves(3)(board))
        path = solve_sliding(board, 3)
        assert path[0] == board and path[-1] == goal
        assert_valid_path(path, sliding_moves(3))
        assert len(path) - 1 == min_moves(board, goal.__eq__, sliding_moves(3))
    assert solve_sliding((2, 1, 3, 4, 5, 0), 3) is None  # odd permutation
    for rule in ("B3/S23", "B36/S23", "B2/S"):
        born, survive = parse_rule(rule)
        for _ in range(60):
            soup = {(rng.randrange(8), rng.randrange(8)) for _ in range(rng.randint(0, 30))}
            assert life_step(soup, rule) == brute_life(soup, born, survive), (rule, soup)
    assert period(GLIDER) == (4, (1, 1)) and period({(0, 0), (0, 1), (1, 0), (1, 1)}) == (1, (0, 0))


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
