"""Tower of Hanoi: move a stack of n discs between three pegs.

Only one disc moves at a time, and a larger disc may never sit on a smaller
one. The recursion mirrors the puzzle exactly: to move n discs from the source
peg to the target peg, first move the top n-1 discs out of the way onto the
spare peg, then move the single largest disc across, then move those n-1 discs
back on top of it. The subproblem is the same puzzle with one fewer disc, which
is why the code is three lines.

The move count satisfies T(n) = 2*T(n-1) + 1 with T(0) = 0, so T(n) = 2^n - 1.
That is optimal: the largest disc must move at least once, and immediately
before it does, every smaller disc has to be stacked on the spare peg. Time is
therefore O(2^n) and the recursion depth is only O(n).
"""


def hanoi(n: int, source: str, target: str, spare: str) -> list[tuple[str, str]]:
    if n == 0:
        return []
    moves = hanoi(n - 1, source, spare, target)
    moves.append((source, target))
    moves.extend(hanoi(n - 1, spare, target, source))
    return moves


def move_count(n: int) -> int:
    return (1 << n) - 1


def simulate(n: int, moves: list[tuple[str, str]]) -> dict[str, list[int]]:
    """Replay the moves to prove no larger disc ever lands on a smaller one."""
    pegs: dict[str, list[int]] = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for src, dst in moves:
        disc = pegs[src].pop()
        if pegs[dst] and pegs[dst][-1] < disc:
            raise ValueError(f"illegal move {disc} onto {pegs[dst][-1]}")
        pegs[dst].append(disc)
    return pegs


def main() -> None:
    for n in range(4):
        moves = hanoi(n, "A", "C", "B")
        print(f"n={n}: {len(moves)} moves (2^n - 1 = {move_count(n)}) {moves}")

    moves = hanoi(4, "A", "C", "B")
    print(f"n=4: {len(moves)} moves, first five {moves[:5]}")
    print(f"n=4 final pegs: {simulate(4, moves)}")

    # Growth is exactly doubling plus one; 64 discs is famously infeasible.
    print(f"moves for 20 discs: {move_count(20)}")
    print(f"moves for 64 discs: {move_count(64)}")


if __name__ == "__main__":
    main()
