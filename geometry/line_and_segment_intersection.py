"""Do two segments cross, and is a point inside a polygon?

Segment intersection needs no division and no line equations. For segments AB
and CD, compute four orientations: how C and D sit relative to AB, and how A and
B sit relative to CD. If C and D lie on opposite sides of AB and A and B lie on
opposite sides of CD, the segments must cross. That is the general case, and it
is exact for integer coordinates because only multiplication and subtraction are
involved.

The special case is collinearity, where an orientation comes out zero. Then the
segments lie on the same line and touch only if their projections overlap, so a
bounding-box containment check settles it. Missing this case is the usual bug.

Point-in-polygon uses ray casting: shoot a ray from the point in a fixed
direction and count edge crossings. An odd count means inside, an even count
means outside, because each crossing toggles between inside and outside. The
half-open comparison on the y interval, one endpoint counted and the other not,
is what stops a vertex from being counted twice. Both routines are O(1) and O(n)
respectively; a point exactly on the boundary is reported separately since ray
casting alone gives no reliable answer there.
"""

Point = tuple[float, float]


def orientation(a: Point, b: Point, c: Point) -> int:
    """+1 counter-clockwise, -1 clockwise, 0 collinear."""
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def on_segment(a: Point, b: Point, p: Point) -> bool:
    """True when p lies on segment ab. Assumes a, b, p are already collinear."""
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    if o1 != o2 and o3 != o4:
        return True  # proper crossing, each segment straddles the other

    # Collinear touching or overlapping: any endpoint inside the other segment.
    if o1 == 0 and on_segment(a, b, c):
        return True
    if o2 == 0 and on_segment(a, b, d):
        return True
    if o3 == 0 and on_segment(c, d, a):
        return True
    if o4 == 0 and on_segment(c, d, b):
        return True
    return False


def intersection_point(a: Point, b: Point, c: Point, d: Point) -> Point | None:
    """The single crossing point, or None if parallel, collinear, or disjoint."""
    r = (b[0] - a[0], b[1] - a[1])
    s = (d[0] - c[0], d[1] - c[1])
    denom = r[0] * s[1] - r[1] * s[0]
    if denom == 0:
        return None  # parallel or collinear: no unique point
    diff = (c[0] - a[0], c[1] - a[1])
    t = (diff[0] * s[1] - diff[1] * s[0]) / denom
    u = (diff[0] * r[1] - diff[1] * r[0]) / denom
    if not (0 <= t <= 1 and 0 <= u <= 1):
        return None  # the infinite lines meet, but outside both segments
    return (a[0] + t * r[0], a[1] + t * r[1])


def point_on_polygon_boundary(polygon: list[Point], p: Point) -> bool:
    for i in range(len(polygon)):
        a, b = polygon[i], polygon[(i + 1) % len(polygon)]
        if orientation(a, b, p) == 0 and on_segment(a, b, p):
            return True
    return False


def point_in_polygon(polygon: list[Point], p: Point) -> bool:
    """Strictly inside, by ray casting. Boundary points are reported False."""
    if len(polygon) < 3 or point_on_polygon_boundary(polygon, p):
        return False
    x, y = p
    inside = False
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        # Half-open y test: counts an edge once even when the ray hits a vertex.
        if (y1 > y) != (y2 > y):
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > x:
                inside = not inside
    return inside


def main() -> None:
    print("segment intersection")
    cases: list[tuple[str, Point, Point, Point, Point]] = [
        ("proper cross", (0.0, 0.0), (4.0, 4.0), (0.0, 4.0), (4.0, 0.0)),
        ("disjoint", (0.0, 0.0), (1.0, 1.0), (3.0, 3.0), (4.0, 4.0)),
        ("touch at endpoint", (0.0, 0.0), (2.0, 2.0), (2.0, 2.0), (4.0, 0.0)),
        ("collinear overlap", (0.0, 0.0), (4.0, 0.0), (2.0, 0.0), (6.0, 0.0)),
        ("collinear apart", (0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)),
        ("parallel", (0.0, 0.0), (4.0, 0.0), (0.0, 1.0), (4.0, 1.0)),
        ("T junction", (0.0, 0.0), (4.0, 0.0), (2.0, 0.0), (2.0, 3.0)),
    ]
    for name, a, b, c, d in cases:
        hit = segments_intersect(a, b, c, d)
        pt = intersection_point(a, b, c, d)
        print(f"  {name:<18} intersects={hit!s:<5} point={pt}")

    print("point in polygon")
    square: list[Point] = [(0.0, 0.0), (4.0, 0.0), (4.0, 4.0), (0.0, 4.0)]
    for p in [(2.0, 2.0), (5.0, 2.0), (0.0, 0.0), (2.0, 0.0), (4.0, 4.0)]:
        print(f"  square  {p}: inside={point_in_polygon(square, p)} "
              f"boundary={point_on_polygon_boundary(square, p)}")

    # Concave polygon: the notch must read as outside.
    ell: list[Point] = [(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (2.0, 2.0),
                        (2.0, 4.0), (0.0, 4.0)]
    for p in [(1.0, 1.0), (3.0, 3.0), (1.0, 3.0), (3.0, 1.0)]:
        print(f"  L-shape {p}: inside={point_in_polygon(ell, p)}")

    # A ray passing exactly through a vertex is still counted once.
    diamond: list[Point] = [(0.0, 0.0), (2.0, 2.0), (4.0, 0.0), (2.0, -2.0)]
    print(f"  diamond (2.0, 0.0): inside={point_in_polygon(diamond, (2.0, 0.0))}")
    print(f"  degenerate polygon: {point_in_polygon([(0.0, 0.0)], (0.0, 0.0))}")


if __name__ == "__main__":
    main()
