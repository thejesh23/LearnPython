"""The Ackermann function: recursion that no loop nest can express.

Defined on non-negative integers by A(0, n) = n + 1, A(m, 0) = A(m - 1, 1),
and A(m, n) = A(m - 1, A(m, n - 1)). The last clause is the interesting one:
the second argument of the outer call is itself an Ackermann call, so the
recursion is not merely nested but self-feeding.

It matters historically because it is total and computable yet not primitive
recursive: it grows faster than any function you can write with a fixed nest of
bounded for-loops. Each increment of m jumps a whole level of the hyperoperation
ladder. A(1, n) is n + 2, A(2, n) is 2n + 3, A(3, n) is 2^(n+3) - 3, and A(4, n)
is a tower of powers of two, so A(4, 2) already has 19729 digits.

Practical consequences: only tiny inputs are computable, memoisation helps a lot
because the same pairs recur, and the recursion depth is enormous, so the limit
has to be raised. Its inverse turns up as the near-constant factor in union-find.
"""

import sys
from functools import cache


@cache
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


def ackermann_closed(m: int, n: int) -> int | None:
    """Known closed forms for small m, used here to check the recursion."""
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return 2 ** (n + 3) - 3
    return None


def main() -> None:
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(20_000)  # A(3, 6) alone nests thousands of frames
    try:
        for m in range(4):
            row = [ackermann(m, n) for n in range(6)]
            print(f"A({m}, n) for n=0..5: {row}")

        checks = [
            (m, n, ackermann(m, n), ackermann_closed(m, n))
            for m in range(4)
            for n in range(5)
        ]
        print(f"matches closed forms: {all(a == b for _, _, a, b in checks)}")

        print(f"A(3, 6) = {ackermann(3, 6)}")
        print(f"A(3, 10) = {ackermann(3, 10)}")
        print(f"cache entries after the above: {ackermann.cache_info().currsize}")

        # A(4, 1) = 65533 is the last value that is even printable; A(4, 2) has
        # 19729 digits and A(4, 3) is beyond any machine.
        print(f"A(4, 0) = {ackermann(4, 0)}")
        # A(4, 1) = 65533, but reaching it needs ~65k nested frames, past any
        # sane recursion limit; A(4, 2) has 19729 digits and A(4, 3) is hopeless.
        try:
            ackermann(4, 1)
        except RecursionError:
            print("A(4, 1) = 65533 in theory; the recursion overflows the stack")
    finally:
        sys.setrecursionlimit(old)


if __name__ == "__main__":
    main()
