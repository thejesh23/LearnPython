"""Convex hull trick: turn an O(n**2) DP with linear transitions into O(n).

Some DP recurrences have the form dp[i] = min over j < i of (m[j] * x[i] + c[j]),
where each earlier state j contributes a line y = m[j] * t + c[j] and the query
is that line evaluated at t = x[i]. Answering "which line is lowest at x[i]?" by
scanning all j is the O(n**2) cost. But the lowest value across a family of lines
traces their lower envelope, a convex piecewise-linear curve, so we only need to
keep the lines that appear on it.

When new lines arrive with monotonically decreasing slopes and queries arrive
with non-decreasing x, both maintenance and lookup become amortised O(1): a deque
holds the envelope, we pop a line from the back when a newcomer makes it
redundant, and a forward-moving pointer answers each query. That is the classic
convex hull trick.

The worked DP here is dp[i] = min over j < i of dp[j] + (x[i] - x[j])**2 on an
increasing x, which expands to lines of slope -2*x[j]; this file solves it both
naively and with CHT and asserts they match.

Complexity: O(n) amortised versus the naive O(n**2).
"""


class Line:
    """A line y = m*t + c on the lower envelope."""

    __slots__ = ("m", "c")

    def __init__(self, m: float, c: float) -> None:
        self.m = m
        self.c = c

    def at(self, t: float) -> float:
        return self.m * t + self.c


def _redundant(a: Line, b: Line, c: Line) -> bool:
    """True if b never wins: a and c cross at or before a and b cross."""
    # Intersection x of two lines is (c2 - c1) / (m1 - m2); compare via
    # cross-multiplication to avoid division and its sign pitfalls.
    return (c.c - a.c) * (a.m - b.m) <= (b.c - a.c) * (a.m - c.m)


class MinEnvelope:
    """Lower envelope for min queries; add lines of decreasing slope,
    query at non-decreasing t."""

    def __init__(self) -> None:
        self._lines: list[Line] = []
        self._ptr = 0

    def add(self, m: float, c: float) -> None:
        line = Line(m, c)
        while len(self._lines) >= 2 and _redundant(
                self._lines[-2], self._lines[-1], line):
            self._lines.pop()
        self._lines.append(line)
        if self._ptr >= len(self._lines):
            self._ptr = len(self._lines) - 1

    def query(self, t: float) -> float:
        while (self._ptr + 1 < len(self._lines)
               and self._lines[self._ptr + 1].at(t)
               <= self._lines[self._ptr].at(t)):
            self._ptr += 1
        return self._lines[self._ptr].at(t)


def solve_cht(x: list[int]) -> list[float]:
    """dp via convex hull trick; dp[0] = 0, dp[i] = min_j dp[j]+(x[i]-x[j])**2."""
    n = len(x)
    dp = [0.0] * n
    env = MinEnvelope()
    env.add(-2 * x[0], dp[0] + x[0] ** 2)  # line for j = 0
    for i in range(1, n):
        dp[i] = env.query(x[i]) + x[i] ** 2
        env.add(-2 * x[i], dp[i] + x[i] ** 2)
    return dp


def solve_naive(x: list[int]) -> list[float]:
    n = len(x)
    dp = [0.0] * n
    for i in range(1, n):
        dp[i] = min(dp[j] + (x[i] - x[j]) ** 2 for j in range(i))
    return dp


def main() -> None:
    x = [0, 2, 3, 7, 8, 15]
    fast = solve_cht(x)
    slow = solve_naive(x)
    print(f"x         = {x}")
    print(f"dp (CHT)  = {fast}")
    print(f"dp (naive)= {slow}")
    assert fast == slow

    import random
    random.seed(3)
    for _ in range(200):
        n = random.randint(1, 40)
        xs = sorted(random.sample(range(0, 300), n))
        f = solve_cht(xs)
        s = solve_naive(xs)
        assert all(abs(a - b) < 1e-6 for a, b in zip(f, s)), (xs, f, s)
    print("random cross-checks: CHT == naive on 200 instances")

    print("\nedge cases:")
    print("  single point:", solve_cht([5]))
    print("  two points:  ", solve_cht([1, 4]))


if __name__ == "__main__":
    main()
