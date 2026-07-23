"""Closest pair of points by divide and conquer in O(n log n).

Given n points in the plane, find the two whose Euclidean distance is smallest.
Checking all pairs is O(n**2); the classic speedup splits the work. Sort points
by x, cut the set into a left and right half, solve each recursively, and let d
be the smaller of the two returned distances. A closer pair, if any, must
straddle the cut, so only points within a vertical strip of width d around the
dividing line can matter.

The strip's magic is that, sorted by y, each point needs to be compared with
only a handful of following points (at most seven) before their y-gap exceeds d
and no closer pair is possible. That bounded scan is what keeps the merge linear,
giving O(n log n) overall. Keeping the points sorted by y as the recursion
returns avoids re-sorting at every level.

This file returns the distance and the achieving pair, and cross-checks the
result against the brute-force all-pairs minimum on random inputs.

Complexity: O(n log n) time and O(n) space.
"""

import math
import random

Point = tuple[float, float]


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def closest_pair(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    """Return (distance, (p, q)) for the closest pair; needs >= 2 points."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    by_x = sorted(points)

    def rec(px: list[Point]) -> tuple[float, tuple[Point, Point]]:
        n = len(px)
        if n <= 3:  # base case: brute force, also produces the y-sorted return
            best = (math.inf, (px[0], px[0]))
            for i in range(n):
                for j in range(i + 1, n):
                    d = _dist(px[i], px[j])
                    if d < best[0]:
                        best = (d, (px[i], px[j]))
            px.sort(key=lambda p: p[1])
            return best

        mid = n // 2
        midx = px[mid][0]
        left, right = px[:mid], px[mid:]
        dl = rec(left)
        dr = rec(right)
        best = dl if dl[0] <= dr[0] else dr
        # px halves are now each sorted by y; merge them into px sorted by y.
        px[:] = _merge_by_y(left, right)

        strip = [p for p in px if abs(p[0] - midx) < best[0]]
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < best[0]:
                d = _dist(strip[i], strip[j])
                if d < best[0]:
                    best = (d, (strip[i], strip[j]))
                j += 1
        return best

    return rec(by_x)


def _merge_by_y(a: list[Point], b: list[Point]) -> list[Point]:
    out: list[Point] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i][1] <= b[j][1]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def brute_force(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    best = (math.inf, (points[0], points[0]))
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = _dist(points[i], points[j])
            if d < best[0]:
                best = (d, (points[i], points[j]))
    return best


def main() -> None:
    pts: list[Point] = [(2.0, 3.0), (12.0, 30.0), (40.0, 50.0),
                        (5.0, 1.0), (12.0, 10.0), (3.0, 4.0)]
    d, (p, q) = closest_pair(pts)
    print(f"closest distance {d:.4f} between {p} and {q}")
    bf = brute_force(pts)
    print(f"brute force: {bf[0]:.4f} between {bf[1][0]} and {bf[1][1]}")
    assert abs(d - bf[0]) < 1e-9

    random.seed(11)
    for _ in range(300):
        n = random.randint(2, 60)
        rng = [(random.uniform(0, 100), random.uniform(0, 100))
               for _ in range(n)]
        assert abs(closest_pair(rng)[0] - brute_force(rng)[0]) < 1e-9
    print("random cross-checks: divide-and-conquer == brute force (300 runs)")

    print("\nedge cases:")
    print("  two points:", closest_pair([(0.0, 0.0), (3.0, 4.0)])[0])
    dup = [(1.0, 1.0), (1.0, 1.0), (9.0, 9.0)]
    print("  duplicate points give distance:", closest_pair(dup)[0])


if __name__ == "__main__":
    main()
