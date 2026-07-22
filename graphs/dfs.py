"""Depth-first search: follow one branch as far as it goes, then back up.

DFS commits to a neighbour and keeps descending until it hits a dead end or an
already-visited node; only then does it retreat and try the next option. The
recursive form gets that behaviour for free from the call stack. The iterative
form makes the stack explicit, which matters in Python because the default
recursion limit is about 1000 frames and a long path will blow through it.

The two forms visit the same set of nodes but not always in the same order: a
stack reverses the neighbour list, so pushing neighbours in order visits them
last-first. Pushing the reversed list restores the recursive order.

Unlike BFS, the first path DFS finds to a node is not the shortest — so use DFS
for reachability, cycle detection, and topological order, not for distance.

Complexity: O(V + E) time, O(V) space for the visited set plus the stack.
"""

Graph = dict[str, list[str]]


def dfs_recursive(graph: Graph, start: str) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()

    def visit(node: str) -> None:
        seen.add(node)
        order.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in seen:
                visit(neighbour)

    visit(start)
    return order


def dfs_iterative(graph: Graph, start: str) -> list[str]:
    """Same traversal with an explicit stack, so deep graphs cannot overflow."""
    order: list[str] = []
    seen: set[str] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        # A node can be pushed several times before it is popped, so the
        # visited test has to happen here as well as before pushing.
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        # Reversed, so the first neighbour ends up on top of the stack and the
        # order matches the recursive version.
        for neighbour in reversed(graph.get(node, [])):
            if neighbour not in seen:
                stack.append(neighbour)
    return order


def has_path(graph: Graph, start: str, goal: str) -> bool:
    seen: set[str] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node == goal:
            return True
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.get(node, []))
    return False


def find_path(graph: Graph, start: str, goal: str) -> list[str] | None:
    """Some path from start to goal (not necessarily the shortest)."""
    seen: set[str] = set()

    def visit(node: str, path: list[str]) -> list[str] | None:
        if node == goal:
            return path
        seen.add(node)
        for neighbour in graph.get(node, []):
            if neighbour not in seen:
                found = visit(neighbour, path + [neighbour])
                if found is not None:
                    return found
        return None

    return visit(start, [start])


def main() -> None:
    #   A --- B --- D
    #   |     |     |
    #   C --- E --- F      G  (isolated)
    graph: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "E"],
        "D": ["B", "F"],
        "E": ["B", "C", "F"],
        "F": ["D", "E"],
        "G": [],
    }

    print(f"recursive from A: {dfs_recursive(graph, 'A')}")
    print(f"iterative from A: {dfs_iterative(graph, 'A')}")
    print(f"has_path A -> F: {has_path(graph, 'A', 'F')}")
    print(f"has_path A -> G: {has_path(graph, 'A', 'G')}")
    print(f"find_path A -> F: {find_path(graph, 'A', 'F')}")

    # The DFS path is valid but longer than the two-edge BFS answer A-B-E.
    print(f"find_path A -> E: {find_path(graph, 'A', 'E')}")

    # Edge cases: an isolated start, and a self-loop that must not hang.
    print(f"isolated start G:  {dfs_recursive(graph, 'G')}")
    print(f"self loop:         {dfs_iterative({'X': ['X']}, 'X')}")

    # A long chain is exactly where the iterative form earns its keep.
    chain: Graph = {str(i): [str(i + 1)] for i in range(3000)}
    chain["3000"] = []
    print(f"chain of 3001 nodes: {len(dfs_iterative(chain, '0'))} visited")


if __name__ == "__main__":
    main()
