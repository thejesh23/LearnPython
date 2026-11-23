"""Rules as data: FizzBuzz from a table of (divisor, word) pairs, and Life-like
cellular automata from a rule string such as "B3/S23". New rules need no new code."""

from collections import Counter
from collections.abc import Iterator
from itertools import count

Cell = tuple[int, int]
FIZZBUZZ = ((3, "Fizz"), (5, "Buzz"))


def fizzbuzz(n: int, rules: tuple[tuple[int, str], ...] = FIZZBUZZ) -> str:
    """Join the words whose divisor divides n, or fall back to the number."""
    return "".join(word for divisor, word in rules if n % divisor == 0) or str(n)


def fizzbuzz_stream(
    limit: int | None = None, rules: tuple[tuple[int, str], ...] = FIZZBUZZ
) -> Iterator[str]:
    """Lazy FizzBuzz from 1; ``limit=None`` runs forever."""
    numbers = count(1) if limit is None else range(1, limit + 1)
    return (fizzbuzz(n, rules) for n in numbers)


def parse_rule(rule: str) -> tuple[frozenset[int], frozenset[int]]:
    """'B36/S23' -> neighbour counts that give birth, and counts that survive."""
    born, survive = rule.upper().split("/")
    return frozenset(map(int, born[1:])), frozenset(map(int, survive[1:]))


def life_step(live: set[Cell], rule: str = "B3/S23") -> set[Cell]:
    """One generation on an unbounded board; only cells next to a live one can change."""
    born, survive = parse_rule(rule)
    counts = Counter(
        (r + dr, c + dc) for r, c in live for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc
    )
    return {cell for cell, n in counts.items() if n in (survive if cell in live else born)}


def life_run(live: set[Cell], generations: int, rule: str = "B3/S23") -> set[Cell]:
    """Advance ``generations`` steps."""
    for _ in range(generations):
        live = life_step(live, rule)
    return live


def from_picture(picture: str) -> set[Cell]:
    """Read '#' (live) and '.' (dead) rows into a set of (row, col) cells."""
    rows = picture.strip().splitlines()
    return {(r, c) for r, row in enumerate(rows) for c, ch in enumerate(row.strip()) if ch == "#"}


def render(live: set[Cell], rows: int, cols: int) -> str:
    """Draw the window rows x cols anchored at (0, 0)."""
    return "\n".join("".join("#" if (r, c) in live else "." for c in range(cols)) for r in range(rows))


def _normalise(live: set[Cell]) -> tuple[frozenset[Cell], Cell]:
    top = min((r for r, _ in live), default=0)
    left = min((c for _, c in live), default=0)
    return frozenset((r - top, c - left) for r, c in live), (top, left)


def period(live: set[Cell], limit: int = 100, rule: str = "B3/S23") -> tuple[int, Cell] | None:
    """(period, displacement) of a pattern that repeats its shape, or None within ``limit``.

    Still lifes give (1, (0, 0)), oscillators (p, (0, 0)) and spaceships a non-zero shift.
    """
    shape, origin = _normalise(live)
    state = live
    for step in range(1, limit + 1):
        state = life_step(state, rule)
        new_shape, new_origin = _normalise(state)
        if new_shape == shape:
            return step, (new_origin[0] - origin[0], new_origin[1] - origin[1])
    return None
