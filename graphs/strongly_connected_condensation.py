"""Condensation DAG of SCCs, plus longest path on the resulting DAG.

Collapse every strongly connected component of a directed graph to a single
super-node and you get the condensation: a graph with the same reachability but
no cycles, a DAG. This is useful because many problems that are hard on a general
directed graph become easy once cycles are gone. Here we compute the longest path
(counted in super-node hops) through the condensation.

Longest path is NP-hard on general graphs but linear on a DAG. Process the
super-nodes in topological order and relax dp[v] = max(dp[v], dp[u] + 1) along
each edge u -> v; every node is finalized before its successors are touched, so
one pass suffices. Because Tarjan already emits components in reverse topological
order, we get the ordering almost for free. The whole thing is O(V + E): one
SCC pass to build the condensation, one DP pass over it.
"""


def tarjan_scc(n: int, graph: list[list[int]]) -> list[list[int]]:
    """Iterative Tarjan; returns components in reverse topological order."""
    index_of = [-1] * n
    lowlink = [0] * n
    on_stack = [False] * n
    stack: list[int] = []
    sccs: list[list[int]] = []
    counter = 0

    for start in range(n):
        if index_of[start] != -1:
            continue
        work: list[tuple[int, int]] = [(start, 0)]
        while work:
            node, pi = work[-1]
            if pi == 0:
                index_of[node] = lowlink[node] = counter
                counter += 1
                stack.append(node)
                on_stack[node] = True
            recursed = False
            while pi < len(graph[node]):
                nxt = graph[node][pi]
                if index_of[nxt] == -1:
                    work[-1] = (node, pi + 1)
                    work.append((nxt, 0))
                    recursed = True
                    break
                if on_stack[nxt]:
                    lowlink[node] = min(lowlink[node], index_of[nxt])
                pi += 1
            if recursed:
                continue
            if lowlink[node] == index_of[node]:
                comp: list[int] = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    comp.append(w)
                    if w == node:
                        break
                sccs.append(comp)
            work.pop()
            if work:
                parent = work[-1][0]
                lowlink[parent] = min(lowlink[parent], lowlink[node])
    return sccs


def condense(n: int, graph: list[list[int]],
             sccs: list[list[int]]) -> tuple[list[int], list[list[int]]]:
    """Return (comp_id per node, DAG adjacency between components)."""
    comp_id = [-1] * n
    for cid, comp in enumerate(sccs):
        for node in comp:
            comp_id[node] = cid
    dag: list[set[int]] = [set() for _ in range(len(sccs))]
    for u in range(n):
        for v in graph[u]:
            if comp_id[u] != comp_id[v]:
                dag[comp_id[u]].add(comp_id[v])
    return comp_id, [sorted(s) for s in dag]


def dag_longest_path(dag: list[list[int]]) -> int:
    """Longest path in edges over a DAG. Tarjan order is reverse-topological."""
    m = len(dag)
    # sccs came out reverse-topo, so component ids increase against topo order;
    # process ids from high to low for a valid topological sweep.
    dp = [0] * m
    best = 0
    for u in range(m - 1, -1, -1):
        for v in dag[u]:
            if dp[u] + 1 > dp[v]:
                dp[v] = dp[u] + 1
            best = max(best, dp[v])
    return best


def _reachable(n: int, graph: list[list[int]], src: int) -> set[int]:
    seen = {src}
    stack = [src]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def main() -> None:
    #  0 -> 1 -> 2 -> 0  (SCC)   2 -> 3   3 -> 4 -> 5 -> 3 (SCC)   5 -> 6
    n = 7
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4),
                 (4, 5), (5, 3), (5, 6)]:
        graph[u].append(v)

    sccs = tarjan_scc(n, graph)
    print("SCCs (reverse topological order):")
    for comp in sccs:
        print(f"  {sorted(comp)}")

    comp_id, dag = condense(n, graph, sccs)
    print("condensation DAG (component -> components):")
    for cid, outs in enumerate(dag):
        print(f"  {cid} {sorted(sccs[cid])} -> {outs}")

    longest = dag_longest_path(dag)
    # Chain of super-nodes: {0,1,2} -> {3,4,5} -> {6}, so 2 edges.
    print(f"DAG longest path (edges): {longest} (expect 2)")
    assert longest == 2

    # Cross-check: reachability is preserved by the condensation. Every node
    # reachable from 0 in the original must share or descend its component.
    reach0 = _reachable(n, graph, 0)
    comp_reach = {comp_id[v] for v in reach0}
    # From node 0's component we should reach every component in the DAG.
    dag_reach = {comp_id[0]}
    stack = [comp_id[0]]
    while stack:
        c = stack.pop()
        for nxt in dag[c]:
            if nxt not in dag_reach:
                dag_reach.add(nxt)
                stack.append(nxt)
    print(f"components reachable from node 0: {sorted(dag_reach)}")
    assert comp_reach == dag_reach, "condensation must preserve reachability"

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
