"""puzzle_kit: one BFS solver for state-space puzzles, plus rule-driven FizzBuzz and Life.

    >>> from puzzles.puzzle_kit import solve_jugs, fizzbuzz
    >>> solve_jugs(4, 3, 2)
    [(0, 0), (0, 3), (3, 0), (3, 3), (4, 2)]
    >>> [fizzbuzz(n, rules=((3, "Fizz"), (5, "Buzz"), (7, "Bazz"))) for n in (7, 15, 21)]
    ['Bazz', 'FizzBuzz', 'FizzBazz']
"""

from .rules import (
    FIZZBUZZ,
    fizzbuzz,
    fizzbuzz_stream,
    from_picture,
    life_run,
    life_step,
    parse_rule,
    period,
    render,
)
from .search import (
    bfs_solve,
    jug_moves,
    missionaries_moves,
    sliding_moves,
    solve_jugs,
    solve_missionaries,
    solve_sliding,
)

__all__ = [
    "bfs_solve", "jug_moves", "solve_jugs", "missionaries_moves", "solve_missionaries",
    "sliding_moves", "solve_sliding", "FIZZBUZZ", "fizzbuzz", "fizzbuzz_stream", "parse_rule",
    "life_step", "life_run", "from_picture", "render", "period",
]
