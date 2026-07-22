"""Convex hull by Andrew's monotone chain: the smallest enclosing polygon.

The convex hull of a point set is the shape a rubber band would take if
stretched around every point. Monotone chain is the easiest correct way to find
it: sort the points left to right (ties broken bottom to top), then sweep once
building the lower hull and once more, in reverse, building the upper hull.

The sweep keeps a stack. Before pushing a new point, pop while the last two
stack entries and the new point make a non-left turn, because such a middle
point lies inside the hull being formed. Since every point is pushed and popped
at most once, the sweep is O(n) and the sort dominates at O(n log n).

Collinear points are the classic trap. Popping on cross <= 0 discards points
lying flat on a hull edge and keeps only the corners; popping on cross < 0
keeps them. This file exposes both through a flag. Degenerate inputs — zero,
one, two, or all-identical points — return the deduplicated points unchanged.
"""

Point = tuple[float, float]


def cross(o: Point, a: Point, b: Point) -> float:
    """Signed turn at o going to a then b: >0 left, <0 right, 0 straight."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[Point], include_collinear: bool = False) -> list[Point]:
    """Hull in counter-clockwise order, starting at the lowest-leftmost point."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def build(sequence: list[Point]) -> list[Point]:
        stack: list[Point] = []
        for p in sequence:
            while len(stack) >= 2:
                turn = cross(stack[-2], stack[-1], p)
                if turn < 0 or (turn == 0 and not include_collinear):
                    stack.pop()
                else:
                    break
            stack.append(p)
        return stack

    lower = build(pts)
    upper = build(pts[::-1])
    # Each chain repeats the other's endpoint, so drop the last of both.
    return lower[:-1] + upper[:-1]


def hull_perimeter(hull: list[Point]) -> float:
    if len(hull) < 2:
        return 0.0
    total = 0.0
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        total += ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    return total


def main() -> None:
    square_with_interior: list[Point] = [
        (0.0, 0.0), (0.0, 4.0), (4.0, 4.0), (4.0, 0.0),
        (2.0, 2.0), (1.0, 3.0), (3.0, 1.0),
    ]
    print(f"hull: {convex_hull(square_with_interior)}")
    print(f"perimeter: {hull_perimeter(convex_hull(square_with_interior))}")

    # A point sitting exactly on an edge: kept or dropped, by flag.
    on_edge: list[Point] = [(0.0, 0.0), (2.0, 0.0), (4.0, 0.0), (4.0, 4.0),
                            (0.0, 4.0)]
    print(f"corners only:      {convex_hull(on_edge)}")
    print(f"with collinear:    {convex_hull(on_edge, include_collinear=True)}")

    print(f"empty:     {convex_hull([])}")
    print(f"single:    {convex_hull([(1.0, 1.0)])}")
    print(f"duplicates:{convex_hull([(1.0, 1.0)] * 5)}")
    print(f"two points:{convex_hull([(1.0, 1.0), (3.0, 3.0)])}")

    # Every point collinear: the hull degenerates to the two extremes.
    line: list[Point] = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
    print(f"all collinear: {convex_hull(line)}")


if __name__ == "__main__":
    main()
