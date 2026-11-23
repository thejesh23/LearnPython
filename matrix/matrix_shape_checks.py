"""Recognising special matrices: identity, symmetric, diagonal, Toeplitz.

Each property is a statement about pairs of cells, so each check is a single
all() over the cells it constrains:

- identity: 1 on the diagonal, 0 everywhere else;
- diagonal: anything on the diagonal, 0 elsewhere;
- symmetric: m[i][j] == m[j][i], i.e. equal to its own transpose;
- upper / lower triangular: zeros below / above the diagonal;
- Toeplitz: constant along every top-left to bottom-right diagonal, so each
  cell equals its upper-left neighbour.

Pascal's triangle is laid out as a matrix to give the checks something
interesting: the symmetric Pascal matrix P[i][j] = C(i + j, i) is symmetric,
and it factors as L @ L^T where L is the lower-triangular Pascal matrix.
"""

from math import comb

Matrix = list[list[int]]


def is_square(m: Matrix) -> bool:
    return all(len(row) == len(m) for row in m)


def is_identity(m: Matrix) -> bool:
    return is_square(m) and all(
        v == (1 if i == j else 0) for i, row in enumerate(m) for j, v in enumerate(row)
    )


def is_diagonal(m: Matrix) -> bool:
    return is_square(m) and all(
        v == 0 for i, row in enumerate(m) for j, v in enumerate(row) if i != j
    )


def is_symmetric(m: Matrix) -> bool:
    return is_square(m) and all(
        m[i][j] == m[j][i] for i in range(len(m)) for j in range(i)
    )


def is_upper_triangular(m: Matrix) -> bool:
    return is_square(m) and all(m[i][j] == 0 for i in range(len(m)) for j in range(i))


def is_lower_triangular(m: Matrix) -> bool:
    return is_upper_triangular(transpose(m)) if is_square(m) else False


def is_rectangular(m: Matrix) -> bool:
    return all(len(row) == len(m[0]) for row in m)


def is_toeplitz(m: Matrix) -> bool:
    return is_rectangular(m) and all(
        m[i][j] == m[i - 1][j - 1]
        for i in range(1, len(m))
        for j in range(1, len(m[i]))
    )


def identity(n: int) -> Matrix:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def pascal_symmetric(n: int) -> Matrix:
    return [[comb(i + j, i) for j in range(n)] for i in range(n)]


def pascal_lower(n: int) -> Matrix:
    return [[comb(i, j) for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(m: Matrix) -> Matrix:
    return [list(col) for col in zip(*m)]


def report(label: str, m: Matrix) -> None:
    checks = {
        "identity": is_identity, "diagonal": is_diagonal, "symmetric": is_symmetric,
        "upper": is_upper_triangular, "lower": is_lower_triangular,
        "toeplitz": is_toeplitz,
    }
    hits = [name for name, check in checks.items() if check(m)]
    print(f"{label:<18} {', '.join(hits) or '-'}")


def main() -> None:
    report("identity(4)", identity(4))
    report("diag(2, 5, 7)", [[2, 0, 0], [0, 5, 0], [0, 0, 7]])
    report("pascal symmetric", pascal_symmetric(5))
    report("pascal lower", pascal_lower(5))
    report("toeplitz 3x4", [[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]])
    report("upper", [[1, 2, 3], [0, 4, 5], [0, 0, 6]])
    report("ragged", [[1, 2], [3]])
    report("plain", [[1, 2], [3, 4]])

    print("\nsymmetric Pascal matrix:")
    for row in pascal_symmetric(5):
        print("  " + " ".join(f"{v:3}" for v in row))

    ok = all(
        matmul(pascal_lower(n), transpose(pascal_lower(n))) == pascal_symmetric(n)
        for n in range(1, 10)
    )
    print(f"\nL @ L^T == symmetric Pascal for n <= 9: {ok}")
    p5 = pascal_symmetric(5)
    print(f"I @ P == P: {matmul(identity(5), p5) == p5}")


if __name__ == "__main__":
    main()
