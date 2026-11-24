"""An immutable Matrix value with operators, shape checks and properties."""

from __future__ import annotations

from collections.abc import Iterable

from .grid import spiral


class Matrix:
    __slots__ = ("rows",)

    def __init__(self, rows: Iterable[Iterable[int]]) -> None:
        data = tuple(tuple(row) for row in rows)
        if data and any(len(row) != len(data[0]) for row in data):
            raise ValueError("all rows must have the same length")
        self.rows = data

    @classmethod
    def identity(cls, n: int) -> Matrix:
        return cls([[int(i == j) for j in range(n)] for i in range(n)])

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0]) if self.rows else 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Matrix) and self.rows == other.rows

    def __hash__(self) -> int:
        return hash(self.rows)

    def __repr__(self) -> str:
        return f"Matrix({[list(r) for r in self.rows]})"

    def __str__(self) -> str:
        width = max((len(str(v)) for row in self.rows for v in row), default=1)
        return "\n".join(" ".join(f"{v:>{width}}" for v in row) for row in self.rows)

    def __add__(self, other: Matrix) -> Matrix:
        if self.shape != other.shape:
            raise ValueError(f"shapes differ: {self.shape} vs {other.shape}")
        return Matrix([[a + b for a, b in zip(r, s)]
                       for r, s in zip(self.rows, other.rows)])

    def __matmul__(self, other: Matrix) -> Matrix:
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"cannot multiply {self.shape} by {other.shape}")
        cols = list(zip(*other.rows))
        return Matrix([[sum(a * b for a, b in zip(row, col)) for col in cols]
                       for row in self.rows])

    def __pow__(self, k: int) -> Matrix:
        """Square matrices to a non-negative power by repeated squaring."""
        if self.shape[0] != self.shape[1] or k < 0:
            raise ValueError("power needs a square matrix and k >= 0")
        result, base = Matrix.identity(self.shape[0]), self
        while k:
            if k & 1:
                result = result @ base
            base, k = base @ base, k >> 1
        return result

    def transpose(self) -> Matrix:
        return Matrix(zip(*self.rows))

    def rotate(self, clockwise: bool = True) -> Matrix:
        if clockwise:
            return Matrix(zip(*reversed(self.rows)))
        return Matrix(reversed(list(zip(*self.rows))))

    def spiral(self) -> list[int]:
        return spiral([list(r) for r in self.rows])

    def is_square(self) -> bool:
        return self.shape[0] == self.shape[1]

    def is_symmetric(self) -> bool:
        return self.is_square() and self == self.transpose()

    def is_identity(self) -> bool:
        return self.is_square() and self == Matrix.identity(self.shape[0])

    def is_toeplitz(self) -> bool:
        r = self.rows
        return all(r[i][j] == r[i - 1][j - 1]
                   for i in range(1, len(r)) for j in range(1, len(r[i])))
