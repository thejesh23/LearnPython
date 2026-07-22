"""Dijkstra's algorithm: shortest paths when every edge weight is non-negative.

BFS works on unweighted graphs because the queue orders nodes by hop count.
With weights the cheapest node is no longer the oldest one, so Dijkstra swaps
the queue for a min-heap keyed on distance-so-far. Each round it pops the
closest unfinalised node, declares its distance final, and relaxes its outgoing
edges — that is, checks whether going through it beats the best known distance
to each neighbour.

Declaring a distance final on pop is only sound because no edge is negative:
any other route to that node would have to leave through something already at
least as far away, and adding non-negative weight cannot make it cheaper. A
single negative edge destroys that argument, and Dijkstra can then finalise a
node too early and return a wrong answer; use Bellman-Ford instead.

Python's heapq has no decrease-key, so the standard trick is to push a new
entry on every improvement and skip stale pops.

Complexity: O((V + E) log V) time, O(V + E) space.
"""

import heapq

Graph = dict[str, list[tuple[str, float]]]


def dijkstra(graph: Graph, start: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """Shortest distances from start, plus the parent map for path rebuilding."""
    dist: dict[str, float] = {start: 0.0}
    parent: dict[str, str | None] = {start: None}
    done: set[str] = set()
    heap: list[tuple[float, str]] = [(0.0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        # Stale entry: this node was already finalised via a cheaper push.
        if node in done:
            continue
        done.add(node)
        for neighbour, weight in graph.get(node, []):
            candidate = d + weight
            if candidate < dist.get(neighbour, float("inf")):
                dist[neighbour] = candidate
                parent[neighbour] = node
                heapq.heappush(heap, (candidate, neighbour))
    return dist, parent


def shortest_path(
    graph: Graph, start: str, goal: str
) -> tuple[list[str], float] | None:
    dist, parent = dijkstra(graph, start)
    if goal not in dist:
        return None
    path: list[str] = []
    node: str | None = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, dist[goal]


def main() -> None:
    #        7        9
    #    A ----- B ------- C
    #     \      |       / |
    #    9 \   10|    11/  |6
    #       \    |     /   |
    #        F --+--- D ---+
    #         14      15
    graph: Graph = {
        "A": [("B", 7), ("C", 9), ("F", 14)],
        "B": [("A", 7), ("C", 10), ("D", 15)],
        "C": [("A", 9), ("B", 10), ("D", 11), ("F", 2)],
        "D": [("B", 15), ("C", 11), ("E", 6)],
        "E": [("D", 6), ("F", 9)],
        "F": [("A", 14), ("C", 2), ("E", 9)],
        "G": [],  # unreachable from A
    }

    dist, _ = dijkstra(graph, "A")
    for node in sorted(dist):
        print(f"A -> {node}: cost {dist[node]:g}")

    print(f"path A -> E: {shortest_path(graph, 'A', 'E')}")
    print(f"path A -> A: {shortest_path(graph, 'A', 'A')}")
    print(f"path A -> G: {shortest_path(graph, 'A', 'G')}")

    # The greedy route A-F (14) loses to A-C-F (11): relaxation fixes an
    # early guess as soon as a cheaper way to reach F shows up.
    print(f"path A -> F: {shortest_path(graph, 'A', 'F')}")

    # Why negative edges break it: Y is popped and finalised at cost 1, so W is
    # computed from that stale value. The later -5 edge does lower Y, but Y is
    # already done, so the correction never reaches W.
    broken: Graph = {
        "X": [("Y", 1), ("Z", 2)],
        "Z": [("Y", -5)],
        "Y": [("W", 1)],
        "W": [],
    }
    print(f"with a negative edge: {dijkstra(broken, 'X')[0]}")
    print("true answers: Y = -3, W = -2")


if __name__ == "__main__":
    main()
