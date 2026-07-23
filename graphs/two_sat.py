"""2-SAT: satisfy a conjunction of two-literal clauses via an implication graph.

Each clause (a OR b) is equivalent to two implications: if a is false then b
must be true, and if b is false then a must be true. Encode every variable x as
two nodes, x and NOT x, and add both implication edges for each clause. A truth
assignment exists exactly when no variable and its negation land in the same
strongly connected component — if they did, x would imply NOT x and vice versa,
a contradiction.

When it is satisfiable, the SCCs give the assignment for free. Condense the
graph and process components in reverse topological order (which is the order
Tarjan emits them). A literal is true when its component comes later than the
component of its negation. Everything runs in O(V + E) over the 2n literals.
"""


def _var(i: int) -> int:
    return 2 * i  # node id of literal x_i being true


def _neg(i: int) -> int:
    return 2 * i + 1  # node id of literal x_i being false


def solve_2sat(n: int, clauses: list[tuple[int, int]]) -> list[bool] | None:
    """Clauses use signed 1-based ints: 3 means x2 true, -3 means x2 false.

    Returns a list of n booleans, or None if the instance is unsatisfiable.
    """
    graph: list[list[int]] = [[] for _ in range(2 * n)]

    def node(lit: int) -> int:
        idx = abs(lit) - 1
        return _var(idx) if lit > 0 else _neg(idx)

    for a, b in clauses:
        # (a OR b) == (not a -> b) and (not b -> a).
        na, nb = node(-a), node(-b)
        graph[na].append(node(b))
        graph[nb].append(node(a))

    comp = _tarjan(graph)

    assignment = [False] * n
    for i in range(n):
        if comp[_var(i)] == comp[_neg(i)]:
            return None
        # Tarjan emits components in reverse topological order, so a smaller
        # component id sits later in topological order. Pick the literal whose
        # component is topologically later (the consequence, not the cause).
        assignment[i] = comp[_var(i)] < comp[_neg(i)]
    return assignment


def _tarjan(graph: list[list[int]]) -> list[int]:
    """Iterative Tarjan SCC; returns a component id per node."""
    n = len(graph)
    index_of = [-1] * n
    lowlink = [0] * n
    on_stack = [False] * n
    comp = [-1] * n
    stack: list[int] = []
    counter = 0
    n_comp = 0

    for start in range(n):
        if index_of[start] != -1:
            continue
        # Explicit DFS stack of (node, next-neighbour-index) frames.
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
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    comp[w] = n_comp
                    if w == node:
                        break
                n_comp += 1
            work.pop()
            if work:
                parent = work[-1][0]
                lowlink[parent] = min(lowlink[parent], lowlink[node])
    return comp


def _brute_force(n: int, clauses: list[tuple[int, int]]) -> bool:
    """Try every assignment; return True iff some assignment satisfies all."""
    for mask in range(1 << n):
        vals = [(mask >> i) & 1 == 1 for i in range(n)]

        def holds(lit: int) -> bool:
            return vals[abs(lit) - 1] if lit > 0 else not vals[abs(lit) - 1]

        if all(holds(a) or holds(b) for a, b in clauses):
            return True
    return False


def main() -> None:
    # Satisfiable: (x1 or x2) and (not x1 or x2) and (not x2 or x3).
    sat = [(1, 2), (-1, 2), (-2, 3)]
    result = solve_2sat(3, sat)
    print(f"satisfiable instance -> {result}")
    assert result is not None
    for a, b in sat:
        la = result[abs(a) - 1] if a > 0 else not result[abs(a) - 1]
        lb = result[abs(b) - 1] if b > 0 else not result[abs(b) - 1]
        assert la or lb, "returned assignment must satisfy every clause"
    assert _brute_force(3, sat), "brute force must agree it is satisfiable"

    # Unsatisfiable: forces x1 true and false at once.
    unsat = [(1, 1), (-1, -1)]  # (x1 or x1) and (not x1 or not x1)
    print(f"unsatisfiable instance -> {solve_2sat(1, unsat)}")
    assert solve_2sat(1, unsat) is None
    assert not _brute_force(1, unsat), "brute force must agree it is UNSAT"

    # Edge case: no clauses is trivially satisfiable.
    empty = solve_2sat(2, [])
    print(f"empty clause set -> {empty}")
    assert empty is not None and len(empty) == 2  # any assignment satisfies

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
