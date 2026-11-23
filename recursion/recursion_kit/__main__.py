"""Examples and self-check: python3 -m recursion.recursion_kit"""

import itertools
import random
import sys

from . import ackermann, combinations, depth, flatten, hanoi, permutations, power_set, recursion_limit


def replay(n: int, moves: list[tuple[str, str]]) -> dict[str, list[int]]:
    """Play the moves on real pegs, failing if a disc lands on a smaller one."""
    pegs: dict[str, list[int]] = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for src, dst in moves:
        disc = pegs[src].pop()
        assert not pegs[dst] or pegs[dst][-1] > disc, f"disc {disc} onto {pegs[dst][-1]}"
        pegs[dst].append(disc)
    return pegs


def examples() -> None:
    print("1. permutations of [1, 2, 3]:", permutations([1, 2, 3]))
    print("2. unique permutations of [1, 1, 2]:", permutations([1, 1, 2], unique=True))
    print("3. 2-combinations of abcd:", ["".join(c) for c in combinations("abcd", 2)])
    print("4. power set of [1, 2, 3]:", power_set([1, 2, 3]))
    nested = [1, [2, [3, [4, []]], 5], [[6]]]
    print("5. flatten", nested, "->", flatten(nested), "| depth", depth(nested))
    moves = hanoi(3)
    print("6. Hanoi, 3 discs:", len(moves), "moves:", " ".join(f"{a}{b}" for a, b in moves))
    with recursion_limit(10_000):
        print("7. Ackermann A(2, 3) =", ackermann(2, 3), "| A(3, 3) =", ackermann(3, 3))
    print("   recursion limit back to", sys.getrecursionlimit())


def self_check() -> None:
    rng = random.Random(4)
    for _ in range(60):
        items = [rng.randint(0, 3) for _ in range(rng.randint(0, 6))]
        assert sorted(permutations(items)) == sorted(map(list, itertools.permutations(items)))
        unique = permutations(items, unique=True)
        assert len(unique) == len({tuple(p) for p in unique}) == len(set(itertools.permutations(items)))
        k = rng.randint(-1, 7)
        expected = [list(c) for c in itertools.combinations(items, k)] if k >= 0 else []
        assert combinations(items, k) == expected
        every = [list(c) for r in range(len(items) + 1) for c in itertools.combinations(items, r)]
        assert sorted(power_set(items)) == sorted(every)
    leaves = list(range(30))
    nested: list = []
    for x in leaves:  # build a random nested shape around the leaves
        nested = [nested, x] if rng.random() < 0.3 else nested + [x]
    assert flatten(nested) == leaves and flatten([]) == [] and depth([[[]]]) == 3
    for n in range(8):
        moves = hanoi(n)
        assert len(moves) == 2**n - 1 and replay(n, moves)["C"] == list(range(n, 0, -1))
    with recursion_limit(10_000):
        for n in range(6):  # known closed forms for m = 0..3
            assert [ackermann(m, n) for m in range(4)] == [n + 1, n + 2, 2 * n + 3, 2 ** (n + 3) - 3]


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
