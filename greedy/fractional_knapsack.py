"""Fractional knapsack: greedy is optimal exactly because items can be split.

Given items with a value and a weight and a bag of fixed capacity, take items
in decreasing order of value density (value divided by weight), and when the
next item no longer fits whole, take the fraction that does. The bag ends up
exactly full unless everything fit.

The exchange argument is short. Suppose an optimal packing puts less of some
high-density item than the greedy solution does; then it must contain some
lower-density material instead. Swapping a unit of weight from the lower to the
higher density item keeps the weight identical and does not decrease the value,
so greedy is at least as good. The step is only legal because material can be
moved in arbitrarily small amounts — that is the whole hinge.

Take away divisibility and the argument collapses. In 0/1 knapsack the same
density rule can be strictly worse than optimal, and the file shows a three-item
instance where it is. That case needs dynamic programming, O(n * capacity).

Cost here is O(n log n), dominated by the sort.
"""

Item = tuple[str, float, float]  # name, value, weight


def by_density(items: list[Item]) -> list[Item]:
    return sorted(items, key=lambda it: it[1] / it[2], reverse=True)


def fractional_knapsack(
    items: list[Item], capacity: float
) -> tuple[float, list[tuple[str, float]]]:
    """Returns the best value and the fraction taken of each item used."""
    taken: list[tuple[str, float]] = []
    total = 0.0
    remaining = capacity
    for name, value, weight in by_density(items):
        if remaining <= 0:
            break
        if weight <= remaining:
            taken.append((name, 1.0))
            total += value
            remaining -= weight
        else:
            fraction = remaining / weight
            taken.append((name, fraction))
            total += value * fraction
            remaining = 0.0
    return total, taken


def knapsack_01_greedy(items: list[Item], capacity: float) -> tuple[float, list[str]]:
    """The same density rule, but items must be taken whole. Not optimal."""
    total = 0.0
    remaining = capacity
    chosen: list[str] = []
    for name, value, weight in by_density(items):
        if weight <= remaining:
            chosen.append(name)
            total += value
            remaining -= weight
    return total, chosen


def knapsack_01_exact(items: list[Item], capacity: int) -> tuple[float, list[str]]:
    """Dynamic programming over integer capacities; O(n * capacity)."""
    best = [0.0] * (capacity + 1)
    pick: list[list[str]] = [[] for _ in range(capacity + 1)]
    for name, value, weight in items:
        w = int(weight)
        for cap in range(capacity, w - 1, -1):  # descending: each item used once
            candidate = best[cap - w] + value
            if candidate > best[cap]:
                best[cap] = candidate
                pick[cap] = pick[cap - w] + [name]
    return best[capacity], pick[capacity]


def main() -> None:
    items: list[Item] = [("gold", 60, 10), ("silver", 100, 20), ("bronze", 120, 30)]
    value, taken = fractional_knapsack(items, 50)
    print(f"fractional, capacity 50: value {value:.2f}")
    for name, frac in taken:
        print(f"  {name}: {frac:.2%}")

    print(f"\ncapacity 0:   {fractional_knapsack(items, 0)}")
    print(f"capacity 100: {fractional_knapsack(items, 100)}")
    print(f"no items:     {fractional_knapsack([], 50)}")

    # Where greedy breaks for 0/1: the densest item crowds out a better pair.
    trap: list[Item] = [("dense", 60, 10), ("big1", 100, 20), ("big2", 100, 20)]
    g_value, g_items = knapsack_01_greedy(trap, 40)
    e_value, e_items = knapsack_01_exact(trap, 40)
    print(f"\n0/1 greedy:  value {g_value:.0f} taking {g_items}")
    print(f"0/1 optimal: value {e_value:.0f} taking {e_items}")
    print(f"greedy loses {e_value - g_value:.0f} of value")

    # With splitting allowed, the same instance has no such gap.
    f_value, _ = fractional_knapsack(trap, 40)
    print(f"fractional on the same instance: {f_value:.0f} (>= the 0/1 optimum)")


if __name__ == "__main__":
    main()
