"""Climbing stairs: how many distinct ways to reach step n taking 1 or 2 steps?

This is the smallest honest dynamic programming problem. The state is a single
number: ways[i] is the number of distinct ways to stand on step i. The last
move onto step i was either a single step from i-1 or a double step from i-2,
and those two sets of paths are disjoint, so ways[i] = ways[i-1] + ways[i-2].

That is Fibonacci shifted by one: ways[n] equals fib(n+1). The lesson is that
recognising the recurrence matters more than the story wrapped around it.
Generalising the allowed step sizes keeps the same shape — sum over every step
size s of ways[i - s] — which is how the coin change counting problem appears.

Complexity: O(n) time and O(1) space for the two-step version, O(n * len(steps))
time for the general one.
"""


def climb_stairs(n: int) -> int:
    if n < 0:
        return 0
    prev, curr = 1, 1  # ways to reach step 0, and step 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


def climb_stairs_table(n: int) -> int:
    """The explicit table, which is easier to read off and to debug."""
    if n < 0:
        return 0
    ways = [0] * (n + 1)
    ways[0] = 1  # exactly one way to stand where you already are
    for i in range(1, n + 1):
        ways[i] = ways[i - 1] + (ways[i - 2] if i >= 2 else 0)
    return ways[n]


def climb_stairs_steps(n: int, steps: list[int]) -> int:
    """Same recurrence with an arbitrary set of allowed step sizes."""
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in steps if s <= i)
    return ways[n]


def fib(n: int) -> int:
    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


def main() -> None:
    for n in range(9):
        print(f"n = {n}: {climb_stairs(n)} ways")

    print("\nedge cases:")
    print("n = 0 (already at the top):", climb_stairs(0))
    print("n = -3 (nonsense input):   ", climb_stairs(-3))

    assert all(climb_stairs(n) == climb_stairs_table(n) for n in range(30))
    print("\ntable and rolling versions agree for n < 30")

    print("Fibonacci in disguise: ways(n) == fib(n + 1)")
    print(" n :", [n for n in range(10)])
    print("ways:", [climb_stairs(n) for n in range(10)])
    print("fib :", [fib(n + 1) for n in range(10)])
    assert all(climb_stairs(n) == fib(n + 1) for n in range(40))

    print("\nsteps of 1, 2 or 3, n = 10:", climb_stairs_steps(10, [1, 2, 3]))
    print("only steps of 2, n = 7:     ", climb_stairs_steps(7, [2]))
    print("only steps of 2, n = 8:     ", climb_stairs_steps(8, [2]))


if __name__ == "__main__":
    main()
