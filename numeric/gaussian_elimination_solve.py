"""Gaussian elimination: solve a dense linear system Ax = b directly.

Elimination reduces A to upper-triangular form by subtracting multiples of one
row from those below, mirroring every operation on b; back substitution then
reads off the unknowns from the bottom up. Done naively a tiny pivot magnifies
round-off, so partial pivoting swaps in the row with the largest available
pivot at each step, which keeps the multipliers bounded and the result stable.

The elimination also hands you two things for free. The product of the pivots,
times the sign of the row swaps, is the determinant. And a pivot that stays
zero even after pivoting means the columns are linearly dependent: the system
is singular, with no unique solution, and that is reported rather than dividing
by zero. The whole procedure is O(n^3) for an n-by-n system.
"""

Matrix = list[list[float]]
Vector = list[float]


def solve(A: Matrix, b: Vector) -> Vector:
    """Return x solving Ax = b via elimination with partial pivoting."""
    x, _ = _eliminate(A, b)
    if x is None:
        raise ValueError("matrix is singular; no unique solution")
    return x


def determinant(A: Matrix) -> float:
    """Determinant as the signed product of pivots from the same elimination."""
    n = len(A)
    _, det = _eliminate(A, [0.0] * n)
    return det


def _eliminate(A: Matrix, b: Vector) -> tuple[Vector | None, float]:
    n = len(A)
    # Augment with b and work on a copy so the inputs stay untouched.
    aug = [A[i][:] + [b[i]] for i in range(n)]
    det, eps = 1.0, 1e-12
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < eps:
            return None, 0.0  # singular column
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            det = -det  # a row swap flips the determinant's sign
        det *= aug[col][col]
        for r in range(col + 1, n):
            factor = aug[r][col] / aug[col][col]
            for k in range(col, n + 1):
                aug[r][k] -= factor * aug[col][k]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):  # back substitution
        s = aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / aug[i][i]
    return x, det


def main() -> None:
    # 2x + y - z = 8; -3x - y + 2z = -11; -2x + y + 2z = -3.
    # Textbook system with the exact solution (2, 3, -1).
    A = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
    b = [8.0, -11.0, -3.0]
    x = solve(A, b)
    print(f"solution: {[round(v, 6) for v in x]}  (expected [2, 3, -1])")

    # Residual A x - b should be ~0.
    residual = [sum(A[i][j] * x[j] for j in range(3)) - b[i] for i in range(3)]
    print(f"max residual: {max(abs(r) for r in residual):.2e}")

    print(f"det(A): {determinant(A):.4f}  (expected -1)")
    print(f"det([[1,2],[3,4]]): {determinant([[1.0, 2.0], [3.0, 4.0]]):.4f}")

    # A singular matrix (row 3 = row 1 + row 2) is detected.
    singular = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [5.0, 7.0, 9.0]]
    print(f"det(singular): {determinant(singular):.2e}")
    try:
        solve(singular, [1.0, 2.0, 3.0])
    except ValueError as e:
        print(f"detected: {e}")

    # Larger random system: cross-check the residual is tiny.
    import random

    rng = random.Random(0)
    n = 20
    M = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
    true_x = [rng.uniform(-5, 5) for _ in range(n)]
    rhs = [sum(M[i][j] * true_x[j] for j in range(n)) for i in range(n)]
    got = solve(M, rhs)
    err = max(abs(got[i] - true_x[i]) for i in range(n))
    print(f"20x20 random system max error: {err:.2e}")


if __name__ == "__main__":
    main()
