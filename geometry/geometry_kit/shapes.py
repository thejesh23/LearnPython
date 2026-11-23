"""Polygons and point sets: area, centroid, containment, hull, closest/farthest pair."""

import heapq
import math

from .vectors import Point, cross, dist, on_segment, sub


def _edges(polygon: list[Point]) -> list[tuple[Point, Point]]:
    return [(polygon[i], polygon[(i + 1) % len(polygon)]) for i in range(len(polygon))]


def signed_area(polygon: list[Point]) -> float:
    """Shoelace formula: positive for counter-clockwise vertices, negative for clockwise."""
    return sum(cross(a, b) for a, b in _edges(polygon)) / 2 if len(polygon) >= 3 else 0.0


def perimeter(polygon: list[Point]) -> float:
    """Total edge length, closing the last vertex back to the first."""
    return sum(dist(a, b) for a, b in _edges(polygon)) if len(polygon) >= 2 else 0.0


def centroid(polygon: list[Point]) -> Point | None:
    """Centre of mass of the enclosed area, or None if the area is zero."""
    area = signed_area(polygon)
    if area == 0:
        return None
    cx = sum((a[0] + b[0]) * cross(a, b) for a, b in _edges(polygon))
    cy = sum((a[1] + b[1]) * cross(a, b) for a, b in _edges(polygon))
    return (cx / (6 * area), cy / (6 * area))


def contains(polygon: list[Point], p: Point) -> bool:
    """Ray casting for any simple polygon; points on the boundary count as inside."""
    inside = False
    for (x1, y1), (x2, y2) in _edges(polygon):
        if on_segment((x1, y1), (x2, y2), p):
            return True
        if (y1 > p[1]) != (y2 > p[1]):  # half-open test counts a shared vertex once
            if p[0] < x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def convex_hull(points: list[Point]) -> list[Point]:
    """Andrew's monotone chain: hull corners counter-clockwise from the lowest-left point."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def chain(seq: list[Point]) -> list[Point]:
        stack: list[Point] = []
        for p in seq:
            while len(stack) >= 2 and cross(sub(stack[-1], stack[-2]), sub(p, stack[-2])) <= 0:
                stack.pop()  # not a left turn, so stack[-1] is inside
            stack.append(p)
        return stack

    return chain(pts)[:-1] + chain(pts[::-1])[:-1]


def closest_pair(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    """Divide and conquer in O(n log n). Returns (distance, (p, q))."""
    if len(points) < 2:
        raise ValueError("need at least two points")

    def rec(px: list[Point]) -> tuple[float, tuple[Point, Point], list[Point]]:
        """Best pair in px (sorted by x), plus px re-sorted by y."""
        if len(px) <= 3:
            best = min(((dist(p, q), (p, q)) for i, p in enumerate(px) for q in px[i + 1:]),
                       default=(math.inf, (px[0], px[0])))
            return best[0], best[1], sorted(px, key=lambda p: p[1])
        mid = len(px) // 2
        mid_x = px[mid][0]
        d1, pair1, left = rec(px[:mid])
        d2, pair2, right = rec(px[mid:])
        d, pair = (d1, pair1) if d1 <= d2 else (d2, pair2)
        by_y = list(heapq.merge(left, right, key=lambda p: p[1]))
        strip = [p for p in by_y if abs(p[0] - mid_x) < d]
        for i, p in enumerate(strip):  # each point has O(1) neighbours to check
            for q in strip[i + 1:]:
                if q[1] - p[1] >= d:
                    break
                if dist(p, q) < d:
                    d, pair = dist(p, q), (p, q)
        return d, pair, by_y

    d, pair, _ = rec(sorted(points))
    return d, pair


def diameter(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    """Farthest pair by rotating calipers over the convex hull. Returns (distance, (p, q))."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    hull = convex_hull(points)
    if len(hull) <= 2:
        return dist(hull[0], hull[-1]), (hull[0], hull[-1])
    m, j = len(hull), 1
    best = (0.0, (hull[0], hull[0]))
    for i in range(m):
        a, b = hull[i], hull[(i + 1) % m]

        def height(k: int) -> float:  # twice the area of triangle a, b, hull[k]
            return abs(cross(sub(b, a), sub(hull[k % m], a)))

        # Advance j while it moves farther from edge ab; it never goes back.
        while height(j + 1) > height(j):
            j = (j + 1) % m
        for v in (hull[j], hull[(j + 1) % m]):
            best = max(best, (dist(a, v), (a, v)), key=lambda t: t[0])
    return best
