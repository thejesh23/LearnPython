"""Min-cost max-flow: push maximum flow, and among all such flows the cheapest.

Every unit of flow now carries a per-unit cost as well as a capacity. We still
want the maximum flow from source to sink, but of all the ways to achieve it we
want the one whose total cost is least. The workhorse is successive shortest
paths: repeatedly send flow along the cheapest source-sink path in the residual
graph. Choosing the cheapest path each time keeps the running flow cost-optimal
for its value, so when no augmenting path remains we have min cost at max flow.

Residual (reverse) edges carry negative cost, so a plain Dijkstra will not do.
We keep a potential per node — a valid shortest-distance estimate — and search
on reduced costs cost + pot[u] - pot[v], which stay non-negative, letting each
round use Dijkstra. The potentials are refreshed from each round's distances.
The first round's potentials come from one Bellman-Ford/SPFA pass. Complexity is
about O(F * E log V) for F augmenting rounds.
"""

import heapq


class MinCostMaxFlow:
    def __init__(self, n: int) -> None:
        self.n = n
        self.adj: list[list[int]] = [[] for _ in range(n)]
        # each edge: [to, capacity, cost]
        self.edges: list[list[int]] = []

    def add_edge(self, u: int, v: int, cap: int, cost: int) -> None:
        self.adj[u].append(len(self.edges))
        self.edges.append([v, cap, cost])
        self.adj[v].append(len(self.edges))
        self.edges.append([u, 0, -cost])  # residual: no cap, negated cost

    def _spfa_potentials(self, s: int) -> list[int]:
        """Initial potentials via Bellman-Ford/SPFA (handles negative costs)."""
        INF = float("inf")
        dist = [INF] * self.n
        dist[s] = 0
        in_queue = [False] * self.n
        queue = [s]
        in_queue[s] = True
        while queue:
            u = queue.pop()
            in_queue[u] = False
            for eid in self.adj[u]:
                v, cap, cost = self.edges[eid]
                if cap > 0 and dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
        return [0 if d == INF else d for d in dist]

    def flow(self, s: int, t: int) -> tuple[int, int]:
        """Return (max_flow, min_cost)."""
        INF = float("inf")
        pot = self._spfa_potentials(s)
        total_flow = 0
        total_cost = 0

        while True:
            dist = [INF] * self.n
            dist[s] = 0
            prev_edge = [-1] * self.n
            pq: list[tuple[int, int]] = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                for eid in self.adj[u]:
                    v, cap, cost = self.edges[eid]
                    if cap <= 0:
                        continue
                    # Reduced cost stays non-negative given valid potentials.
                    nd = d + cost + pot[u] - pot[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        prev_edge[v] = eid
                        heapq.heappush(pq, (nd, v))
            if dist[t] == INF:
                break  # sink unreachable: max flow reached

            for i in range(self.n):
                if dist[i] < INF:
                    pot[i] += dist[i]

            # Bottleneck along the found path, then augment.
            push = INF
            v = t
            while v != s:
                eid = prev_edge[v]
                push = min(push, self.edges[eid][1])
                v = self.edges[eid ^ 1][0]
            v = t
            while v != s:
                eid = prev_edge[v]
                self.edges[eid][1] -= push
                self.edges[eid ^ 1][1] += push
                v = self.edges[eid ^ 1][0]
            total_flow += push
            total_cost += push * (pot[t] - pot[s])
        return total_flow, total_cost


def _plain_max_flow(n: int, arcs: list[tuple[int, int, int, int]], s: int,
                    t: int) -> int:
    """Ignore costs; BFS-augmenting max flow for cross-checking the value."""
    from collections import deque

    adj: list[list[int]] = [[] for _ in range(n)]
    edges: list[list[int]] = []
    for u, v, cap, _cost in arcs:
        adj[u].append(len(edges))
        edges.append([v, cap])
        adj[v].append(len(edges))
        edges.append([u, 0])

    flow = 0
    while True:
        prev = [-1] * n
        prev[s] = -2
        q = deque([s])
        while q:
            u = q.popleft()
            for eid in adj[u]:
                v, cap = edges[eid]
                if cap > 0 and prev[v] == -1:
                    prev[v] = eid
                    q.append(v)
        if prev[t] == -1:
            break
        push = float("inf")
        v = t
        while v != s:
            eid = prev[v]
            push = min(push, edges[eid][1])
            v = edges[eid ^ 1][0]
        v = t
        while v != s:
            eid = prev[v]
            edges[eid][1] -= push
            edges[eid ^ 1][1] += push
            v = edges[eid ^ 1][0]
        flow += push
    return flow


def main() -> None:
    # 4 nodes, two routes to the sink: one cheap-narrow, one pricey-wide.
    #   0 -> 1 cap 3 cost 1,  1 -> 3 cap 2 cost 1
    #   0 -> 2 cap 2 cost 4,  2 -> 3 cap 3 cost 1
    #   1 -> 2 cap 2 cost 1
    arcs = [
        (0, 1, 3, 1), (1, 3, 2, 1), (0, 2, 2, 4),
        (2, 3, 3, 1), (1, 2, 2, 1),
    ]
    mcmf = MinCostMaxFlow(4)
    for u, v, cap, cost in arcs:
        mcmf.add_edge(u, v, cap, cost)
    f, c = mcmf.flow(0, 3)
    print(f"max flow 0 -> 3: {f}, min cost: {c}")

    expected = _plain_max_flow(4, arcs, 0, 3)
    print(f"plain max flow cross-check: {expected}")
    assert f == expected, "MCMF flow value must equal plain max flow"

    # Edge case: a single edge carries its whole capacity at its own cost.
    single = MinCostMaxFlow(2)
    single.add_edge(0, 1, 5, 7)
    single_result = single.flow(0, 1)  # flow() mutates residuals; call once
    print(f"single edge -> {single_result} (expect (5, 35))")
    assert single_result == (5, 35)

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
