"""Topological sort: order a directed graph so every edge points forward.

If tasks depend on other tasks, a topological order is a schedule in which
nothing runs before its prerequisites. Such an order exists exactly when the
graph is acyclic — a cycle is a set of tasks all waiting on each other.

Two standard algorithms, same result. Kahn's works forwards: count how many
incoming edges each node has, repeatedly take a node with zero, and decrement
its neighbours. The DFS variant works backwards: run a depth-first search and
append each node once all its descendants are finished, then reverse. A node
finishing last in DFS is one nothing depends on, so reversal puts sources
first.

Cycle detection falls out of both. Kahn's emits fewer nodes than the graph has
if some never reach in-degree zero. DFS colours nodes white/grey/black and
reports a cycle the moment it meets a grey node — one still on the recursion
stack, meaning it found a path back to an ancestor.

Complexity: O(V + E) time and O(V) space for either version.
"""

from collections import deque

Graph = dict[str, list[str]]


def kahn(graph: Graph) -> list[str] | None:
    """Topological order by repeatedly removing in-degree-zero nodes."""
    indegree = {node: 0 for node in graph}
    for node in graph:
        for target in graph[node]:
            indegree[target] += 1

    # sorted() only makes the output deterministic; any zero node would do.
    ready = deque(sorted(n for n, d in indegree.items() if d == 0))
    order: list[str] = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for target in graph[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)

    return order if len(order) == len(graph) else None


def dfs_topological(graph: Graph) -> list[str] | None:
    """Topological order from reversed DFS finish times."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}
    order: list[str] = []

    def visit(node: str) -> bool:
        colour[node] = GREY
        for target in graph[node]:
            if colour[target] == GREY:
                return False  # back edge to an ancestor: a cycle
            if colour[target] == WHITE and not visit(target):
                return False
        colour[node] = BLACK
        order.append(node)  # appended only after every descendant is done
        return True

    for node in sorted(graph):
        if colour[node] == WHITE and not visit(node):
            return None
    order.reverse()
    return order


def find_cycle(graph: Graph) -> list[str] | None:
    """Return one directed cycle as a node list, or None if the graph is acyclic."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        colour[node] = GREY
        stack.append(node)
        for target in graph[node]:
            if colour[target] == GREY:
                return stack[stack.index(target):] + [target]
            if colour[target] == WHITE:
                found = visit(target)
                if found is not None:
                    return found
        colour[node] = BLACK
        stack.pop()
        return None

    for node in sorted(graph):
        if colour[node] == WHITE:
            found = visit(node)
            if found is not None:
                return found
    return None


def is_valid_order(graph: Graph, order: list[str]) -> bool:
    position = {node: i for i, node in enumerate(order)}
    return all(
        position[node] < position[target]
        for node in graph
        for target in graph[node]
    )


def main() -> None:
    # A tiny build pipeline: parse before compile, compile before link, and so on.
    build: Graph = {
        "fetch": ["parse"],
        "parse": ["compile"],
        "compile": ["link", "test"],
        "lint": ["test"],
        "link": ["package"],
        "test": ["package"],
        "package": [],
    }

    kahn_order = kahn(build)
    dfs_order = dfs_topological(build)
    assert kahn_order is not None and dfs_order is not None
    print(f"kahn: {kahn_order}")
    print(f"dfs:  {dfs_order}")
    print(f"both valid: {is_valid_order(build, kahn_order)} "
          f"{is_valid_order(build, dfs_order)}")
    print(f"cycle: {find_cycle(build)}")

    # Add an edge that closes a loop: package now feeds back into fetch.
    cyclic = {node: list(targets) for node, targets in build.items()}
    cyclic["package"] = ["fetch"]
    print(f"kahn on a cycle: {kahn(cyclic)}")
    print(f"dfs on a cycle:  {dfs_topological(cyclic)}")
    print(f"the cycle: {find_cycle(cyclic)}")

    # Edge cases: no edges at all, and an empty graph.
    print(f"no edges: {kahn({'a': [], 'b': []})}")
    print(f"empty:    {kahn({})}, {dfs_topological({})}")

    # A self-loop is the shortest possible cycle.
    print(f"self loop: {kahn({'a': ['a']})}, {find_cycle({'a': ['a']})}")


if __name__ == "__main__":
    main()
