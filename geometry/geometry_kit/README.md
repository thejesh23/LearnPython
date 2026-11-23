# geometry_kit

2-D computational geometry on plain tuples: vectors, segment crossings, polygon measures, convex hull, closest and farthest pairs.

```bash
python3 -m geometry.geometry_kit     # eight examples plus a randomized self-check
```

```python
from geometry.geometry_kit import convex_hull, signed_area, closest_pair

hull = convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])   # [(0, 0), (2, 0), (2, 2), (0, 2)]
signed_area(hull)                                              # 4.0 (positive: counter-clockwise)
closest_pair([(0, 0), (5, 5), (1, 1)])                         # (1.414..., ((0, 0), (1, 1)))
```

| Function | Module | Teaches |
|---|---|---|
| `sub`, `dot`, `cross`, `dist`, `orientation` | `vectors.py` | vector basics and the left/right turn test |
| `on_segment`, `segments_intersect`, `intersection_point` | `vectors.py` | exact crossing tests from orientations |
| `signed_area`, `perimeter`, `centroid` | `shapes.py` | the shoelace formula and its relatives |
| `contains` | `shapes.py` | ray casting (boundary counts as inside) |
| `convex_hull`, `diameter` | `shapes.py` | monotone chain, then rotating calipers |
| `closest_pair` | `shapes.py` | divide and conquer in O(n log n) |

Standalone versions live next to this folder, e.g. `../polygon_area.py`.
