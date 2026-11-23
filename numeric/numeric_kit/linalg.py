"""Dense linear algebra on lists of lists: solve, determinant, dominant eigenpair."""

Matrix = list[list[float]]
Vector = list[float]


def mat_vec(A: Matrix, v: Vector) -> Vector:
    """The product A @ v."""
    return [sum(a * x for a, x in zip(row, v)) for row in A]


def _eliminate(A: Matrix, b: Vector) -> tuple[Vector | None, float]:
    """Gaussian elimination with partial pivoting. Returns (x or None, det)."""
    n = len(A)
    aug = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]  # work on a copy
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            return None, 0.0
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            det = -det  # a row swap flips the determinant's sign
        det *= aug[col][col]
        for r in range(col + 1, n):
            factor = aug[r][col] / aug[col][col]
            for k in range(col, n + 1):
                aug[r][k] -= factor * aug[col][k]
    x = [0.0] * n
    for i in reversed(range(n)):  # back substitution
        x[i] = (aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))) / aug[i][i]
    return x, det


def solve(A: Matrix, b: Vector) -> Vector:
    """x with A @ x == b. Raises ValueError if A is singular."""
    x, _ = _eliminate(A, b)
    if x is None:
        raise ValueError("matrix is singular; no unique solution")
    return x


def determinant(A: Matrix) -> float:
    """Signed product of the pivots from the same elimination."""
    return _eliminate(A, [0.0] * len(A))[1]


def dominant_eigen(A: Matrix, tol: float = 1e-10, max_iter: int = 10_000) -> tuple[float, Vector]:
    """Power iteration: (largest-magnitude eigenvalue, unit eigenvector).

    Repeatedly multiplying by A amplifies the dominant direction; convergence
    is fast when that eigenvalue is well separated from the next one.
    """
    v = [1.0 / (i + 1) for i in range(len(A))]  # asymmetric start, unlikely orthogonal
    for _ in range(max_iter):
        w = mat_vec(A, v)
        norm = sum(x * x for x in w) ** 0.5
        if norm == 0:
            return 0.0, v
        w = [x / norm for x in w]
        if sum(a * b for a, b in zip(w, v)) < 0:
            w = [-x for x in w]  # keep a consistent sign between steps
        done = max(abs(a - b) for a, b in zip(w, v)) < tol  # the direction stopped moving
        v = w
        if done:
            break
    return sum(a * b for a, b in zip(v, mat_vec(A, v))), v  # Rayleigh quotient
