"""Lexicographically smallest topological order, and counting all orders.

A topological order lists a DAG's vertices so every edge points forward. Kahn's
algorithm builds one by repeatedly removing a vertex with no remaining incoming
edges (in-degree zero) and decrementing its successors. When several vertices are
ready at once, any of them may go next — so to get the lexicographically smallest
order we always take the smallest-labeled ready vertex. A min-heap over the ready
set makes that choice in O(log V), giving O((V + E) log V) overall.

If the heap empties before all vertices are placed, a cycle remains and no
topological order exists. Counting how many distinct orders a DAG admits is a
separate, harder question — it is #P-hard in general — so here we count by
straightforward backtracking over the ready set, which is fine for the small
DAGs used to teach the idea and lets us cross-check the Kahn result is one of
the enumerated orders.
"""

import heapq


def lexicographic_toposort(n: int,
                           adj: list[list[int]]) -> list[int] | None:
    """Smallest topological order by label, or None if a cycle exists."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    heap = [u for u in range(n) if indeg[u] == 0]
    heapq.heapify(heap)
    order: list[int] = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    return order if len(order) == n else None


def count_topological_orders(n: int, adj: list[list[int]]) -> int:
    """Count distinct topological orders by backtracking over ready vertices."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1

    count = 0

    def backtrack(placed: int) -> None:
        nonlocal count
        if placed == n:
            count += 1
            return
        for u in range(n):
            if indeg[u] == 0:
                indeg[u] = -1  # mark placed
                for v in adj[u]:
                    indeg[v] -= 1
                backtrack(placed + 1)
                for v in adj[u]:
                    indeg[v] += 1
                indeg[u] = 0
    backtrack(0)
    return count


def _all_topological_orders(n: int,
                            adj: list[list[int]]) -> list[tuple[int, ...]]:
    """Enumerate every order (for cross-checking, small n only)."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    orders: list[tuple[int, ...]] = []
    current: list[int] = []

    def backtrack() -> None:
        if len(current) == n:
            orders.append(tuple(current))
            return
        for u in range(n):
            if indeg[u] == 0:
                indeg[u] = -1
                for v in adj[u]:
                    indeg[v] -= 1
                current.append(u)
                backtrack()
                current.pop()
                for v in adj[u]:
                    indeg[v] += 1
                indeg[u] = 0
    backtrack()
    return orders


def _is_valid_topo(order: list[int], n: int, adj: list[list[int]]) -> bool:
    pos = {node: i for i, node in enumerate(order)}
    if len(pos) != n:
        return False
    return all(pos[u] < pos[v] for u in range(n) for v in adj[u])


def main() -> None:
    # Classic dependency DAG (course prerequisites style).
    #   0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4
    n = 5
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]:
        adj[u].append(v)

    order = lexicographic_toposort(n, adj)
    print(f"lexicographically smallest order: {order}")
    assert order is not None and _is_valid_topo(order, n, adj)

    all_orders = sorted(_all_topological_orders(n, adj))
    assert tuple(order) == all_orders[0], "Kahn+heap must give the smallest"
    print(f"smallest of all orders: {all_orders[0]}")

    total = count_topological_orders(n, adj)
    print(f"number of distinct topological orders: {total}")
    assert total == len(all_orders), "backtrack count must match enumeration"

    # Edge case: independent vertices permute freely -> n! orders.
    empty: list[list[int]] = [[], [], []]
    print(f"3 isolated nodes -> {count_topological_orders(3, empty)} orders "
          f"(expect 6)")
    assert count_topological_orders(3, empty) == 6

    # Edge case: a cycle has no topological order.
    cyc: list[list[int]] = [[1], [2], [0]]
    print(f"cyclic graph order -> {lexicographic_toposort(3, cyc)}")
    assert lexicographic_toposort(3, cyc) is None

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
