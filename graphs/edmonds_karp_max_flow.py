"""Edmonds-Karp: maximum flow by always augmenting along the shortest path.

Max flow asks how much can be pushed from a source to a sink when every edge
has a capacity. Ford-Fulkerson repeatedly finds a path with spare capacity (an
augmenting path) in the residual graph and pushes flow along it, adding a
reverse edge each time so later paths can cancel earlier choices. Edmonds-Karp
pins down the path choice: use BFS, so each augmenting path has the fewest
edges.

That single decision bounds the running time. Because the shortest source-sink
distance in the residual graph never decreases and each edge can become the
bottleneck only O(V) times, the number of augmentations is O(VE), giving an
O(VE^2) algorithm independent of the capacity values.

When no augmenting path remains, the flow is maximum. The nodes still reachable
from the source in the final residual graph form one side of a minimum cut;
every original edge crossing from that side to the rest is saturated, and their
capacities sum to the max flow — the max-flow min-cut theorem in action.
"""

from collections import deque

Capacity = dict[str, dict[str, int]]


def edmonds_karp(capacity: Capacity, source: str, sink: str) -> tuple[int, Capacity]:
    """Return (max flow value, residual capacities after saturation)."""
    # Deep-copy into a residual graph, adding a 0-capacity reverse slot per edge.
    residual: Capacity = {u: {} for u in capacity}
    for u in capacity:
        for v, cap in capacity[u].items():
            residual.setdefault(v, {})
            residual[u][v] = residual[u].get(v, 0) + cap
            residual[v].setdefault(u, residual[v].get(u, 0))

    max_flow = 0
    while True:
        # BFS for a shortest augmenting path, remembering parents.
        parent: dict[str, str] = {source: source}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, cap in residual[u].items():
                if cap > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break

        # Bottleneck = smallest residual capacity along the found path.
        bottleneck = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u
        max_flow += int(bottleneck)

    return max_flow, residual


def min_cut_edges(
    capacity: Capacity, residual: Capacity, source: str
) -> list[tuple[str, str]]:
    """Edges from the source side to the sink side; all are saturated."""
    reachable: set[str] = set()
    queue = deque([source])
    while queue:
        u = queue.popleft()
        if u in reachable:
            continue
        reachable.add(u)
        for v, cap in residual[u].items():
            if cap > 0 and v not in reachable:
                queue.append(v)

    cut: list[tuple[str, str]] = []
    for u in capacity:
        for v in capacity[u]:
            if u in reachable and v not in reachable:
                cut.append((u, v))
    return cut


def main() -> None:
    #        S
    #      /   \
    #   10/     \10
    #    A --1--- B
    #   9|        |10
    #    C --6--- D
    #      \     /
    #    10 \   /10
    #         T
    capacity: Capacity = {
        "S": {"A": 10, "B": 10},
        "A": {"B": 1, "C": 9},
        "B": {"D": 10},
        "C": {"D": 6, "T": 10},
        "D": {"C": 0, "T": 10},
        "T": {},
    }

    flow, residual = edmonds_karp(capacity, "S", "T")
    print(f"max flow S -> T: {flow}")

    cut = min_cut_edges(capacity, residual, "S")
    cut_value = sum(capacity[u][v] for u, v in cut)
    print(f"min cut edges: {sorted(cut)}")
    print(f"min cut capacity: {cut_value}")
    assert cut_value == flow, "max-flow min-cut theorem must hold"

    # Edge case: a single bottleneck edge caps the whole flow.
    narrow: Capacity = {"S": {"M": 3}, "M": {"T": 100}, "T": {}}
    f2, _ = edmonds_karp(narrow, "S", "T")
    print(f"bottleneck flow: {f2} (expect 3)")

    # Edge case: no path at all yields zero flow.
    cut_off: Capacity = {"S": {}, "T": {}}
    f3, _ = edmonds_karp(cut_off, "S", "T")
    print(f"disconnected flow: {f3} (expect 0)")


if __name__ == "__main__":
    main()
