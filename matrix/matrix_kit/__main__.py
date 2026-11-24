"""Examples and self-check: python3 -m matrix.matrix_kit"""

import random
import sys

from . import Matrix, rotate_in_place, set_zeroes, spiral


def examples() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    print(f"1. {m!r} has shape {m.shape}")
    print("2. rotated clockwise:\n" + str(m.rotate()))
    wide = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print("3. spiral of 3x4:", wide.spiral())
    print(f"4. m @ m.T = {(m @ m.transpose())!r}, symmetric: "
          f"{(m @ m.transpose()).is_symmetric()}")
    fib = Matrix([[1, 1], [1, 0]]) ** 30
    print(f"5. Fibonacci via [[1,1],[1,0]] ** 30: {fib.rows[0][1]}")
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_zeroes(grid)
    print(f"6. set zeroes: {grid}")
    try:
        m @ m
    except ValueError as err:
        print(f"7. refused: {err}")


def self_check() -> None:
    rng = random.Random(13)
    for _ in range(300):
        r, c = rng.randint(1, 6), rng.randint(1, 6)
        m = Matrix([[rng.randint(-5, 5) for _ in range(c)] for _ in range(r)])
        assert m.rotate().rotate().rotate().rotate() == m
        assert m.rotate().rotate(clockwise=False) == m
        assert m.transpose().transpose() == m
        assert sorted(m.spiral()) == sorted(v for row in m.rows for v in row)
        assert Matrix.identity(r) @ m == m == m @ Matrix.identity(c)
        assert (m @ m.transpose()).is_symmetric()
        if r == c:
            grid = [list(row) for row in m.rows]
            rotate_in_place(grid)
            assert Matrix(grid) == m.rotate()
            assert m ** 3 == m @ m @ m and m ** 0 == Matrix.identity(r)
        grid = [[rng.choice([0, 1, 2]) for _ in range(c)] for _ in range(r)]
        zero_rows = {i for i, row in enumerate(grid) if 0 in row}
        zero_cols = {j for row in grid for j, v in enumerate(row) if v == 0}
        want = [[0 if i in zero_rows or j in zero_cols else v
                 for j, v in enumerate(row)] for i, row in enumerate(grid)]
        set_zeroes(grid)
        assert grid == want
    fib = Matrix([[1, 1], [1, 0]]) ** 90
    assert fib.rows[0][1] == 2880067194370816120
    assert spiral([]) == [] and Matrix([[1, 2], [2, 1]]).is_toeplitz()


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
