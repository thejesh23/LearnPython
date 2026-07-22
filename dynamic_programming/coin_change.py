"""Coin change: fewest coins summing to an amount, with unlimited coins of each
denomination.

The greedy "take the biggest coin that fits" rule is wrong for general coin
systems — with coins 1, 3, 4 and amount 6 it yields 4+1+1 while the optimum is
3+3. So the whole space of choices has to be searched, and dynamic programming
does it without repetition.

The state is best[a], the fewest coins that make amount a exactly, or infinity
if a is unreachable. The recurrence is best[a] = 1 + min(best[a - c]) over all
coins c that fit. This is the unbounded knapsack shape: a coin may be reused,
so the inner loop scans amounts upward and immediately sees its own results.

Recording which coin achieved each minimum lets the actual multiset be walked
back afterwards. Complexity: O(amount * len(coins)) time, O(amount) space.
"""

from collections import Counter

INF = float("inf")


def min_coins(coins: list[int], amount: int) -> int:
    """Fewest coins for the amount, or -1 if no combination reaches it."""
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else int(best[amount])


def min_coins_with_choice(coins: list[int], amount: int) -> list[int] | None:
    """Return one optimal multiset of coins, or None if the amount is impossible."""
    best = [0] + [INF] * amount
    pick: list[int | None] = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
                pick[a] = c  # the coin used last to reach amount a
    if best[amount] == INF:
        return None
    out: list[int] = []
    a = amount
    while a > 0:
        c = pick[a]
        assert c is not None
        out.append(c)
        a -= c
    return sorted(out, reverse=True)


def count_ways(coins: list[int], amount: int) -> int:
    """Number of distinct combinations (order ignored) that make the amount.

    Coins are the outer loop so each combination is counted in one fixed coin
    order; swapping the loops would count permutations instead.
    """
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


def main() -> None:
    coins = [1, 5, 6, 9]
    for amount in (0, 4, 11, 13, 30):
        picked = min_coins_with_choice(coins, amount)
        print(f"amount {amount:>3}: {min_coins(coins, amount):>2} coins  {picked}")

    print("\ngreedy fails where DP does not, coins 1, 3, 4 and amount 6:")
    print("  optimal:", min_coins_with_choice([1, 3, 4], 6))

    print("\nedge cases:")
    print("  amount 0:", min_coins([1, 2], 0), min_coins_with_choice([1, 2], 0))
    print("  unreachable amount 7 with coins [2, 4]:", min_coins([2, 4], 7))
    print("  no coins at all, amount 5:", min_coins([], 5))

    print("\ncombinations making 11 from", coins, ":", count_ways(coins, 11))
    print("classic: ways to make 100 from [1, 5, 10, 25]:",
          count_ways([1, 5, 10, 25], 100))

    picked = min_coins_with_choice([1, 5, 6, 9], 30)
    assert picked is not None and sum(picked) == 30
    print("\nreconstruction check, 30 =", dict(Counter(picked)), "sums to",
          sum(picked))


if __name__ == "__main__":
    main()
