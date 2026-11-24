"""matrix_kit: an immutable Matrix with @, ** and rotations, plus grid walks.

    >>> from matrix.matrix_kit import Matrix
    >>> fib = Matrix([[1, 1], [1, 0]]) ** 10
    >>> fib.rows[0][1]
    55
"""

from .grid import rotate_in_place, set_zeroes, spiral
from .matrix import Matrix

__all__ = ["Matrix", "spiral", "rotate_in_place", "set_zeroes"]
