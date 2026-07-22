"""Breadth-first search: explore a graph in rings of increasing distance.

BFS keeps a queue of nodes waiting to be expanded. It pops the oldest one,
looks at its neighbours, and pushes any it has never seen. Because the queue is
first-in-first-out, every node at distance k is dequeued before any node at
distance k+1.

That ordering is the key insight: the first time BFS reaches a node, it has
reached it by a path with the fewest possible edges. So on an unweighted graph
BFS is a shortest-path algorithm, not just a traversal. Recording the node you
came from turns the search into a path you can print by walking parents
backwards from the goal.

Complexity: O(V + E) time and O(V) space, since each node enters the queue once
and each edge is examined once (twice for an undirected graph).
"""

from collections import deque

Graph = dict[str, list[str]]


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Return nodes in the order BFS visits them."""
    seen = {start}
    queue = deque([start])
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, []):
            # Mark on push, not on pop: otherwise a node with two parents in
            # the same ring gets queued twice.
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return order


def bfs_distances(graph: Graph, start: str) -> dict[str, int]:
    """Edge count from start to every reachable node."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph.get(node, []):
            if neighbour not in dist:
                dist[neighbour] = dist[node] + 1
                queue.append(neighbour)
    return dist


def shortest_path(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Fewest-edges path from start to goal, or None if unreachable."""
    if start == goal:
        return [start]
    parent: dict[str, str | None] = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph.get(node, []):
            if neighbour in parent:
                continue
            parent[neighbour] = node
            if neighbour == goal:
                return reconstruct(parent, goal)
            queue.append(neighbour)
    return None


def reconstruct(parent: dict[str, str | None], goal: str) -> list[str]:
    path: list[str] = []
    node: str | None = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def main() -> None:
    #   A --- B --- D
    #   |     |     |
    #   C --- E --- F      G --- H  (a separate component)
    graph: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "E"],
        "D": ["B", "F"],
        "E": ["B", "C", "F"],
        "F": ["D", "E"],
        "G": ["H"],
        "H": ["G"],
    }

    print(f"visit order from A: {bfs_order(graph, 'A')}")
    print(f"distances from A:   {bfs_distances(graph, 'A')}")
    print(f"A -> F: {shortest_path(graph, 'A', 'F')}")
    print(f"A -> A: {shortest_path(graph, 'A', 'A')}")

    # Edge case: the goal sits in another component, so BFS drains the queue
    # and reports failure rather than looping forever.
    print(f"A -> H: {shortest_path(graph, 'A', 'H')}")

    # Edge case: an isolated node has no neighbours at all.
    print(f"visit order from G: {bfs_order(graph, 'G')}")
    print(f"lone node: {bfs_order({'X': []}, 'X')}")


if __name__ == "__main__":
    main()
