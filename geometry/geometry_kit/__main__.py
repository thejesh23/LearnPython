"""Examples and self-check: python3 -m geometry.geometry_kit"""

import itertools
import math
import random
import sys

from . import (
    centroid,
    closest_pair,
    contains,
    convex_hull,
    diameter,
    dist,
    dot,
    intersection_point,
    orientation,
    perimeter,
    segments_intersect,
    signed_area,
)


def examples() -> None:
    print("1. dot of perpendicular vectors:", dot((1, 2), (-2, 1)),
          "| turn (0,0)->(1,0)->(1,1):", orientation((0, 0), (1, 0), (1, 1)))
    print("2. segments cross:", segments_intersect((0, 0), (4, 4), (0, 4), (4, 0)),
          "at", intersection_point((0, 0), (4, 4), (0, 4), (4, 0)))
    house = [(0, 0), (4, 0), (4, 3), (2, 5), (0, 3)]
    print("3. house area", signed_area(house), "| perimeter", round(perimeter(house), 3),
          "| centroid", tuple(round(c, 3) for c in centroid(house)))
    print("4. clockwise order flips the sign:", signed_area(house[::-1]))
    print("5. (2, 4) inside:", contains(house, (2, 4)), "| (4, 4) inside:", contains(house, (4, 4)))
    cloud = [(0, 0), (3, 1), (1, 1), (2, 3), (4, 4), (1, 3), (0, 4), (2, 2)]
    print("6. hull of 8 points:", convex_hull(cloud))
    d, pair = closest_pair(cloud)
    print("7. closest pair:", pair, "at", round(d, 3))
    d, pair = diameter(cloud)
    print("8. farthest pair:", pair, "at", round(d, 3))


def self_check() -> None:
    rect = [(0, 0), (5, 0), (5, 3), (0, 3)]
    assert signed_area(rect) == 15 and perimeter(rect) == 16 and centroid(rect) == (2.5, 1.5)
    assert centroid([(0, 0), (1, 1), (2, 2)]) is None
    assert not segments_intersect((0, 0), (1, 0), (2, 0), (3, 0))
    assert segments_intersect((0, 0), (2, 0), (2, 0), (3, 5))  # touching endpoint counts
    rng = random.Random(11)
    for _ in range(200):
        pts = [(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(rng.randint(2, 40))]
        pairs = list(itertools.combinations(pts, 2))
        assert math.isclose(closest_pair(pts)[0], min(dist(p, q) for p, q in pairs))
        assert math.isclose(diameter(pts)[0], max(dist(p, q) for p, q in pairs))
        hull = convex_hull(pts)
        if len(hull) >= 3:
            assert signed_area(hull) > 0, "hull must be counter-clockwise"
            assert all(contains(hull, p) for p in pts), "hull must enclose every point"
        a, b, c, d = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(4)]
        hit = intersection_point(a, b, c, d)
        if hit is not None:
            assert segments_intersect(a, b, c, d)
            assert math.isclose(dist(a, hit) + dist(hit, b), dist(a, b))


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
