"""Optimal binary search tree by interval DP over key access frequencies.

Given sorted keys and how often each is searched for, different BST shapes give
different average search costs: a frequently queried key deep in the tree is
expensive because every search for it traverses many nodes. We want the shape
minimising the expected number of comparisons, sum over keys of
frequency * (depth + 1).

The state is cost[i][j], the best expected cost of a tree built from keys i..j.
Whichever key r becomes the root, its two subtrees are the ranges i..r-1 and
r+1..j, each solved optimally, and rooting deepens every key in the range by one
level, which adds the whole range's frequency sum exactly once. So
cost[i][j] = freq_sum(i, j) + min over r of cost[i][r-1] + cost[r+1][j]. This is
interval DP: shorter ranges first, so longer ones read them.

Recording the winning root per range lets us print the resulting tree. (This
uses key frequencies only; unsuccessful-search "gap" weights are a standard
extension omitted for clarity.)

Complexity: O(n**3) time and O(n**2) space.
"""

INF = float("inf")


def optimal_bst(keys: list[str],
                freq: list[float]) -> tuple[float, list[list[int]]]:
    """Return the minimum expected cost and the chosen-root table."""
    n = len(keys)
    if n == 0:
        return 0.0, []
    cost = [[0.0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]
    prefix = [0.0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    def freq_sum(i: int, j: int) -> float:
        return prefix[j + 1] - prefix[i]

    for i in range(n):
        cost[i][i] = freq[i]
        root[i][i] = i
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = INF
            w = freq_sum(i, j)
            for r in range(i, j + 1):
                left = cost[i][r - 1] if r > i else 0.0
                right = cost[r + 1][j] if r < j else 0.0
                trial = left + right + w
                if trial < cost[i][j]:
                    cost[i][j] = trial
                    root[i][j] = r
    return cost[0][n - 1], root


def build_structure(root: list[list[int]], keys: list[str],
                    i: int, j: int) -> str:
    if i > j:
        return "."
    r = root[i][j]
    if i == j:
        return keys[r]
    return f"({build_structure(root, keys, i, r - 1)} " \
           f"{keys[r]} " \
           f"{build_structure(root, keys, r + 1, j)})"


def brute_force(freq: list[float]) -> float:
    """Reference: try every root recursively, no memoisation."""
    prefix = [0.0]
    for f in freq:
        prefix.append(prefix[-1] + f)

    def solve(i: int, j: int) -> float:
        if i > j:
            return 0.0
        w = prefix[j + 1] - prefix[i]
        return w + min(solve(i, r - 1) + solve(r + 1, j)
                       for r in range(i, j + 1))

    return solve(0, len(freq) - 1)


def main() -> None:
    keys = ["A", "B", "C", "D"]
    freq = [0.1, 0.2, 0.4, 0.3]
    best, root = optimal_bst(keys, freq)
    print(f"keys {keys} freq {freq}")
    print(f"  minimum expected cost: {best:.4f}")
    print(f"  tree structure: {build_structure(root, keys, 0, len(keys) - 1)}")
    assert abs(best - brute_force(freq)) < 1e-9

    keys2 = ["10", "20", "30", "40", "50", "60"]
    freq2 = [4, 2, 6, 3, 1, 5]
    best2, root2 = optimal_bst(keys2, freq2)
    print(f"\nkeys {keys2} freq {freq2}")
    print(f"  minimum expected cost: {best2:.4f}")
    print(f"  tree structure: {build_structure(root2, keys2, 0, len(keys2)-1)}")
    assert abs(best2 - brute_force(freq2)) < 1e-9

    print("\nedge cases:")
    print("  empty:", optimal_bst([], []))
    b1, r1 = optimal_bst(["X"], [7])
    print("  single key:", b1, build_structure(r1, ["X"], 0, 0))


if __name__ == "__main__":
    main()
