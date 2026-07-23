"""QR decomposition: split a matrix into an orthonormal Q and triangular R.

Gram-Schmidt takes the columns of A one at a time and removes from each column
the part that already lies along the earlier columns, leaving a residual that is
orthogonal to all of them; normalising that residual gives one column of Q. The
coefficients removed, together with the residual lengths, form the upper-
triangular R, so that A = QR with Q having orthonormal columns (Q^T Q = I).

The factorisation costs O(m n^2) and is the numerically stable workhorse behind
least squares. Because Q is orthonormal it preserves lengths, so minimising
||Ax - b|| is the same as minimising ||Rx - Q^T b||; the triangular system
R x = Q^T b then solves by back substitution. Classical Gram-Schmidt can lose
orthogonality on ill-conditioned data, so the modified variant used here
subtracts each projection as soon as it is known.
"""

Matrix = list[list[float]]
Vector = list[float]


def qr_decompose(A: Matrix) -> tuple[Matrix, Matrix]:
    """Return Q (m x n, orthonormal columns) and R (n x n, upper) with A = QR."""
    m = len(A)
    n = len(A[0])
    # Work with columns; Q columns are built in place from A's columns.
    cols = [[A[i][j] for i in range(m)] for j in range(n)]
    q_cols: list[Vector] = []
    R = [[0.0] * n for _ in range(n)]
    for j in range(n):
        v = cols[j][:]
        for i in range(len(q_cols)):
            # Modified Gram-Schmidt: project onto each finished q as we go.
            r = sum(q_cols[i][k] * v[k] for k in range(m))
            R[i][j] = r
            for k in range(m):
                v[k] -= r * q_cols[i][k]
        norm = sum(x * x for x in v) ** 0.5
        if norm < 1e-12:
            raise ValueError("columns are linearly dependent")
        R[j][j] = norm
        q_cols.append([x / norm for x in v])
    Q = [[q_cols[j][i] for j in range(n)] for i in range(m)]
    return Q, R


def back_substitution(R: Matrix, b: Vector) -> Vector:
    """Solve R x = b for upper-triangular R."""
    n = len(R)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(R[i][j] * x[j] for j in range(i + 1, n))) / R[i][i]
    return x


def least_squares(A: Matrix, b: Vector) -> Vector:
    """Minimise ||Ax - b|| via A = QR, solving R x = Q^T b."""
    Q, R = qr_decompose(A)
    m, n = len(A), len(A[0])
    qtb = [sum(Q[i][j] * b[i] for i in range(m)) for j in range(n)]
    return back_substitution(R, qtb)


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def main() -> None:
    A = [[12.0, -51.0, 4.0],
         [6.0, 167.0, -68.0],
         [-4.0, 24.0, -41.0]]
    Q, R = qr_decompose(A)
    n = len(A)

    # Q^T Q should be the identity: columns are orthonormal.
    qtq = [[sum(Q[k][i] * Q[k][j] for k in range(len(Q)))
            for j in range(n)] for i in range(n)]
    off = max(abs(qtq[i][j] - (1.0 if i == j else 0.0))
              for i in range(n) for j in range(n))
    print(f"max |Q^T Q - I|: {off:.2e}")

    # QR should reconstruct A.
    qr = matmul(Q, R)
    recon = max(abs(qr[i][j] - A[i][j]) for i in range(n) for j in range(n))
    print(f"max |QR - A|: {recon:.2e}")

    # R is upper-triangular: entries below the diagonal are zero.
    below = max(abs(R[i][j]) for i in range(n) for j in range(i))
    print(f"max below-diagonal |R|: {below:.2e}")

    # Least squares: fit y = a + b*x to noisy-ish points, overdetermined.
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    ys = [1.0, 3.1, 4.9, 7.2, 8.8]  # roughly y = 1 + 2x
    design = [[1.0, x] for x in xs]
    a, b = least_squares(design, ys)
    print(f"\nleast-squares line: y = {a:.4f} + {b:.4f} x")
    rss = sum((a + b * x - y) ** 2 for x, y in zip(xs, ys))
    print(f"residual sum of squares: {rss:.5f}")

    # Exact fit through 2 points: line passes through both, zero residual.
    exact = least_squares([[1.0, 0.0], [1.0, 2.0]], [1.0, 5.0])
    print(f"exact 2-point fit: y = {exact[0]:.4f} + {exact[1]:.4f} x "
          f"(expect 1 + 2x)")


if __name__ == "__main__":
    main()
