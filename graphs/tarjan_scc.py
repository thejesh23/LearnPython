"""Tarjan's algorithm: strongly connected components in a single DFS pass.

A strongly connected component (SCC) is a maximal set of vertices where every
vertex can reach every other along directed edges. Tarjan finds them all in one
depth-first traversal by giving each node two numbers: an index (the order it
was first visited) and a lowlink (the smallest index reachable from it through
its DFS subtree plus one back-edge). Nodes still being explored sit on a stack.

The key insight: a node whose lowlink equals its own index is the root of an
SCC, because nothing in its subtree reached anything older. When that happens,
everything above it on the stack down to and including it forms one component.
Lowlink only ever propagates from nodes still on the stack, which keeps already-
finished components from bleeding into later ones.

The components come out in reverse topological order of the condensation — the
DAG you get by collapsing each SCC to a point. Complexity: O(V + E).
"""

Graph = dict[str, list[str]]


def tarjan_scc(graph: Graph) -> list[list[str]]:
    """Return the SCCs; each inner list is one component."""
    index_of: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    sccs: list[list[str]] = []
    counter = 0

    def strong_connect(node: str) -> None:
        nonlocal counter
        index_of[node] = lowlink[node] = counter
        counter += 1
        stack.append(node)
        on_stack.add(node)

        for nxt in graph.get(node, []):
            if nxt not in index_of:
                strong_connect(nxt)
                lowlink[node] = min(lowlink[node], lowlink[nxt])
            elif nxt in on_stack:
                # Back-edge to a node still open: use its index, not its
                # lowlink, so finished SCCs never merge into this one.
                lowlink[node] = min(lowlink[node], index_of[nxt])

        if lowlink[node] == index_of[node]:
            component: list[str] = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                component.append(w)
                if w == node:
                    break
            sccs.append(component)

    for node in graph:
        if node not in index_of:
            strong_connect(node)
    return sccs


def condensation(graph: Graph, sccs: list[list[str]]) -> dict[int, set[int]]:
    """Collapse each SCC to an id; return the DAG of edges between components."""
    comp_id: dict[str, int] = {}
    for i, comp in enumerate(sccs):
        for node in comp:
            comp_id[node] = i
    dag: dict[int, set[int]] = {i: set() for i in range(len(sccs))}
    for node, neighbours in graph.items():
        for nxt in neighbours:
            if comp_id[node] != comp_id[nxt]:
                dag[comp_id[node]].add(comp_id[nxt])
    return dag


def main() -> None:
    #  A -> B -> C -> A   (one cycle)      D -> C, D -> E
    #  E -> F -> E        (another cycle)  G alone
    graph: Graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
        "D": ["C", "E"],
        "E": ["F"],
        "F": ["E"],
        "G": [],
    }

    sccs = tarjan_scc(graph)
    for comp in sccs:
        print(f"SCC: {sorted(comp)}")

    # Cross-check: the SCCs must partition every vertex exactly once.
    flat = [node for comp in sccs for node in comp]
    assert sorted(flat) == sorted(graph), "SCCs must cover all vertices once"

    dag = condensation(graph, sccs)
    print("condensation (component -> components):")
    for cid in sorted(dag):
        members = sorted(sccs[cid])
        print(f"  {cid} {members} -> {sorted(dag[cid])}")

    # Edge case: a single node with a self-loop is its own SCC.
    loop: Graph = {"X": ["X"]}
    print(f"self-loop SCCs: {tarjan_scc(loop)}")

    # Edge case: a pure DAG makes every node its own singleton SCC.
    line: Graph = {"P": ["Q"], "Q": ["R"], "R": []}
    print(f"DAG SCC count: {len(tarjan_scc(line))} (expect 3)")


if __name__ == "__main__":
    main()
