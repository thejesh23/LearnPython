"""Point in a convex polygon in O(log n) by binary search on a fan.

For a general polygon, deciding whether a point is inside costs O(n) by ray
casting. Convexity buys a logarithmic test. Fix a vertex of the convex polygon
as an anchor and imagine fanning triangles from it to every edge; the anchor
splits the polygon into wedges whose bounding rays sweep monotonically in angle.
Binary searching those rays finds the single wedge that could contain the query
in O(log n), after which one orientation test against that wedge's far edge
settles it.

Concretely, with vertices in counter-clockwise order and anchor v0, the query p
must lie left of ray v0->v1 and right of ray v0->v[n-1] to be in any wedge; a
binary search on the cross product of v0->p against v0->v[i] locates the wedge
i, and p is inside iff it is left of edge v[i]->v[i+1]. Points exactly on an
edge count as inside here.

This file contrasts the O(log n) test with a straightforward O(n) ray cast and
asserts they agree on random queries.

Complexity: O(log n) per query after an O(n) convexity assumption.
"""

import random

Point = tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_convex(poly: list[Point], p: Point) -> bool:
    """Fast test: poly must be convex and counter-clockwise, no 3 collinear.

    Returns True for interior and boundary points."""
    n = len(poly)
    if n < 3:
        return False
    v0 = poly[0]
    # Must be within the extreme fan rays to stand a chance.
    if _cross(v0, poly[1], p) < 0 or _cross(v0, poly[n - 1], p) > 0:
        return False
    # Binary search for wedge i such that p is between rays v0->v[i], v0->v[i+1].
    lo, hi = 1, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _cross(v0, poly[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    # p is inside iff it is on the interior side of edge v[lo] -> v[lo+1].
    return _cross(poly[lo], poly[lo + 1], p) >= 0


def point_in_polygon_raycast(poly: list[Point], p: Point) -> bool:
    """Reference O(n) even-odd ray cast; boundary points count as inside."""
    n = len(poly)
    x, y = p
    inside = False
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        # Boundary: p exactly on this edge.
        if _cross((ax, ay), (bx, by), p) == 0 and \
                min(ax, bx) <= x <= max(ax, bx) and \
                min(ay, by) <= y <= max(ay, by):
            return True
        if (ay > y) != (by > y):
            x_cross = ax + (y - ay) / (by - ay) * (bx - ax)
            if x < x_cross:
                inside = not inside
    return inside


def main() -> None:
    # Counter-clockwise convex hexagon.
    poly: list[Point] = [(0.0, 0.0), (4.0, 0.0), (6.0, 3.0),
                         (4.0, 6.0), (0.0, 6.0), (-2.0, 3.0)]
    tests = [(2.0, 3.0), (0.0, 0.0), (3.0, 0.0), (10.0, 10.0),
             (-1.0, 3.0), (5.0, 3.0)]
    for q in tests:
        fast = point_in_convex(poly, q)
        slow = point_in_polygon_raycast(poly, q)
        print(f"{q}: log-n {fast}, ray-cast {slow}")
        assert fast == slow, q

    random.seed(4)
    for _ in range(5000):
        q = (random.uniform(-4, 8), random.uniform(-2, 8))
        # Skip queries landing exactly on a vertex fan ray tie edge case is
        # already handled; both methods must still agree everywhere.
        assert point_in_convex(poly, q) == point_in_polygon_raycast(poly, q), q
    print("random cross-checks: O(log n) == O(n) ray cast (5000 queries)")

    print("\nedge cases:")
    tri: list[Point] = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0)]
    print("  triangle, centroid inside:", point_in_convex(tri, (1.0, 1.0)))
    print("  triangle, vertex on boundary:", point_in_convex(tri, (0.0, 0.0)))
    print("  triangle, far outside:", point_in_convex(tri, (9.0, 9.0)))
    print("  degenerate (2 pts):", point_in_convex([(0.0, 0.0), (1.0, 1.0)],
                                                    (0.5, 0.5)))


if __name__ == "__main__":
    main()
