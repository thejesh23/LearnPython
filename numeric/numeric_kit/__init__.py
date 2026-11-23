"""numeric_kit: roots, derivatives, integrals, ODEs and small linear systems.

    >>> import math
    >>> from numeric.numeric_kit import bisect_root, integrate, solve
    >>> round(bisect_root(lambda x: x * x - 2, 0, 2), 9), round(integrate(math.sin, 0, math.pi), 9)
    (1.414213562, 2.0)
    >>> [round(x, 9) for x in solve([[2, 1], [1, 3]], [3, 5])]
    [0.8, 1.4]
"""

from .calculus import bisect_root, derivative, integrate, newton_root, rk4
from .linalg import determinant, dominant_eigen, mat_vec, solve

__all__ = [
    "derivative",
    "bisect_root",
    "newton_root",
    "integrate",
    "rk4",
    "mat_vec",
    "solve",
    "determinant",
    "dominant_eigen",
]
