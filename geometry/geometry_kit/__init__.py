"""geometry_kit: 2-D points as tuples, polygons as lists of points.

    >>> from geometry.geometry_kit import convex_hull, signed_area, intersection_point
    >>> square = convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])
    >>> square, signed_area(square)
    ([(0, 0), (2, 0), (2, 2), (0, 2)], 4.0)
    >>> intersection_point((0, 0), (4, 4), (0, 4), (4, 0))
    (2.0, 2.0)
"""

from .shapes import centroid, closest_pair, contains, convex_hull, diameter, perimeter, signed_area
from .vectors import (
    Point,
    cross,
    dist,
    dot,
    intersection_point,
    on_segment,
    orientation,
    segments_intersect,
    sub,
)

__all__ = [
    "Point",
    "sub",
    "dot",
    "cross",
    "dist",
    "orientation",
    "on_segment",
    "segments_intersect",
    "intersection_point",
    "signed_area",
    "perimeter",
    "centroid",
    "contains",
    "convex_hull",
    "closest_pair",
    "diameter",
]
