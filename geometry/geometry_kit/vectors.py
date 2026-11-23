"""2-D points as tuples: vector arithmetic, orientation and segment crossings.

Everything here uses only + - * on coordinates (no trig, no division) except
``dist`` and ``intersection_point``, so integer inputs give exact answers.
"""

import math

Point = tuple[float, float]


def sub(a: Point, b: Point) -> Point:
    """The vector from b to a."""
    return (a[0] - b[0], a[1] - b[1])


def dot(a: Point, b: Point) -> float:
    """Alignment: positive same way, zero perpendicular, negative opposed."""
    return a[0] * b[0] + a[1] * b[1]


def cross(a: Point, b: Point) -> float:
    """Signed area of the parallelogram on a and b (positive if b is left of a)."""
    return a[0] * b[1] - a[1] * b[0]


def dist(a: Point, b: Point) -> float:
    """Euclidean distance between two points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def orientation(a: Point, b: Point, c: Point) -> int:
    """+1 if a -> b -> c turns left (counter-clockwise), -1 right, 0 straight."""
    v = cross(sub(b, a), sub(c, a))
    return (v > 0) - (v < 0)


def on_segment(a: Point, b: Point, p: Point) -> bool:
    """True if p lies on the closed segment ab."""
    return (orientation(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Do segments ab and cd share at least one point (touching counts)?"""
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    if o1 != o2 and o3 != o4:
        return True  # each segment straddles the other's line
    return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)


def intersection_point(a: Point, b: Point, c: Point, d: Point) -> Point | None:
    """The single crossing point of ab and cd, or None (parallel or disjoint)."""
    r, s = sub(b, a), sub(d, c)
    denom = cross(r, s)
    if denom == 0:
        return None
    t = cross(sub(c, a), s) / denom
    u = cross(sub(c, a), r) / denom
    if not (0 <= t <= 1 and 0 <= u <= 1):
        return None  # the lines meet, but outside the segments
    return (a[0] + t * r[0], a[1] + t * r[1])
