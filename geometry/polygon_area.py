"""Shoelace formula: the area of any simple polygon from its vertices alone.

Walk the vertices in order and sum the cross product of each consecutive pair,
x_i * y_(i+1) - x_(i+1) * y_i, wrapping the last vertex back to the first. Half
that sum is the area. The name comes from the criss-cross pattern the products
make when the coordinates are written in two columns.

Each term is twice the signed area of the triangle formed by the origin and one
edge. Triangles on the far side of the origin come out negative and cancel the
overcount exactly, so the origin's position does not matter and the polygon need
not be convex — only simple, meaning its edges do not cross each other.

The sign of the result is free information: positive means the vertices are
listed counter-clockwise, negative means clockwise. The same sum, weighted by
the midpoint of each edge, gives the centroid of the enclosed area, which is not
the same as the average of the vertices. Both are O(n) time and O(1) space.
"""

Point = tuple[float, float]


def signed_area(polygon: list[Point]) -> float:
    """Positive if the vertices run counter-clockwise, negative if clockwise."""
    if len(polygon) < 3:
        return 0.0
    total = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        total += x1 * y2 - x2 * y1
    return total / 2.0


def area(polygon: list[Point]) -> float:
    return abs(signed_area(polygon))


def is_counter_clockwise(polygon: list[Point]) -> bool:
    return signed_area(polygon) > 0


def perimeter(polygon: list[Point]) -> float:
    total = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        total += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return total


def centroid(polygon: list[Point]) -> Point | None:
    """Centroid of the enclosed area. None when the area is zero (degenerate)."""
    a = signed_area(polygon)
    if a == 0:
        return None
    cx = cy = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        term = x1 * y2 - x2 * y1
        cx += (x1 + x2) * term
        cy += (y1 + y2) * term
    return (cx / (6.0 * a), cy / (6.0 * a))


def main() -> None:
    square: list[Point] = [(0.0, 0.0), (4.0, 0.0), (4.0, 4.0), (0.0, 4.0)]
    print(f"square area:      {area(square)}")
    print(f"square signed:    {signed_area(square)}")
    print(f"square ccw:       {is_counter_clockwise(square)}")
    print(f"square perimeter: {perimeter(square)}")
    print(f"square centroid:  {centroid(square)}")

    # Reversing the vertex order flips the sign but not the magnitude.
    print(f"reversed signed:  {signed_area(square[::-1])}")
    print(f"reversed ccw:     {is_counter_clockwise(square[::-1])}")

    triangle: list[Point] = [(0.0, 0.0), (5.0, 0.0), (0.0, 3.0)]
    print(f"triangle area:     {area(triangle)}")
    print(f"triangle centroid: {centroid(triangle)}")

    # Non-convex but simple: an L shape. The formula does not care.
    ell: list[Point] = [(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (2.0, 2.0),
                        (2.0, 4.0), (0.0, 4.0)]
    print(f"L-shape area:     {area(ell)}")
    print(f"L-shape centroid: {centroid(ell)}")
    # The vertex average differs from the true area centroid.
    avg = (sum(p[0] for p in ell) / len(ell), sum(p[1] for p in ell) / len(ell))
    print(f"L-shape vertex average: {avg}")

    print(f"two points:      {area([(0.0, 0.0), (1.0, 1.0)])}")
    print(f"empty:           {area([])}")
    print(f"collinear three: {area([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])}")
    print(f"collinear centroid: {centroid([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])}")


if __name__ == "__main__":
    main()
