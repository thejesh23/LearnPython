"""0/1 knapsack: pick a subset of items maximising value within a weight limit.

Each item may be taken at most once, which is what the 0/1 in the name means.
The state is best[i][w]: the most value obtainable from the first i items with
capacity w. For item i there are exactly two choices, so

    best[i][w] = max(best[i-1][w], value[i] + best[i-1][w - weight[i]])

with the second option only available when the item fits. Because every read
comes from row i-1, one row is enough if it is updated in place — but only if
the capacity loop runs downward. Going upward would let best[w - weight[i]]
already contain the current item, silently turning the problem into unbounded
knapsack where items may be reused.

Complexity: O(n * capacity) time; O(n * capacity) space for the table version
and O(capacity) for the rolling one. Note this is pseudo-polynomial: the cost
grows with the numeric capacity, not with the number of bits used to write it.
"""


def knapsack_table(weights: list[int], values: list[int],
                   capacity: int) -> tuple[int, list[int]]:
    """Return the best value and the indices of the items achieving it."""
    n = len(weights)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]
            if wi <= w:
                best[i][w] = max(best[i][w], vi + best[i - 1][w - wi])

    chosen: list[int] = []
    w = capacity
    for i in range(n, 0, -1):
        if best[i][w] != best[i - 1][w]:  # value changed, so item i was taken
            chosen.append(i - 1)
            w -= weights[i - 1]
    chosen.reverse()
    return best[n][capacity], chosen


def knapsack_rolling(weights: list[int], values: list[int], capacity: int) -> int:
    """One row, updated right to left so each item is considered only once."""
    best = [0] * (capacity + 1)
    for wi, vi in zip(weights, values):
        for w in range(capacity, wi - 1, -1):
            best[w] = max(best[w], vi + best[w - wi])
    return best[capacity]


def unbounded_knapsack(weights: list[int], values: list[int],
                       capacity: int) -> int:
    """The same loop running forward: items become reusable, for contrast."""
    best = [0] * (capacity + 1)
    for wi, vi in zip(weights, values):
        for w in range(wi, capacity + 1):
            best[w] = max(best[w], vi + best[w - wi])
    return best[capacity]


def main() -> None:
    weights = [3, 4, 5, 9, 4]
    values = [3, 5, 8, 10, 6]
    capacity = 13

    value, chosen = knapsack_table(weights, values, capacity)
    print(f"capacity {capacity}, best value {value}")
    for i in chosen:
        print(f"  item {i}: weight {weights[i]}, value {values[i]}")
    print("  total weight:", sum(weights[i] for i in chosen))

    print("rolling array agrees:", knapsack_rolling(weights, values, capacity))
    assert knapsack_rolling(weights, values, capacity) == value

    print("\nwhy the loop runs backwards — one item, weight 2, value 3,"
          " capacity 6:")
    print("  backward (0/1, item used once):     ",
          knapsack_rolling([2], [3], 6))
    print("  forward  (unbounded, used 3 times): ",
          unbounded_knapsack([2], [3], 6))

    print("\nedge cases:")
    print("  no items:      ", knapsack_table([], [], 10))
    print("  zero capacity: ", knapsack_table(weights, values, 0))
    print("  nothing fits:  ", knapsack_table([7, 8], [9, 9], 5))
    print("  everything fits:", knapsack_table(weights, values, 100))


if __name__ == "__main__":
    main()
