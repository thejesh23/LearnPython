"""Transposing and rotating a matrix, in place and with zip.

Transpose swaps m[i][j] with m[j][i]: mirror across the main diagonal. A
90-degree clockwise rotation is a transpose followed by reversing each row;
counter-clockwise is a transpose followed by reversing the row order. Both run
in O(n^2) time with O(1) extra space for a square matrix.

The in-place version only works for square matrices, because a 2x3 matrix
rotates into a 3x2 one and cannot reuse its own storage. For any shape,
zip(*m) builds the transpose in one line, and rotation is zip over the
reversed rows.
"""

Matrix = list[list[int]]


def transpose_in_place(m: Matrix) -> None:
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]


def rotate_clockwise_in_place(m: Matrix) -> None:
    transpose_in_place(m)
    for row in m:
        row.reverse()


def rotate_counter_in_place(m: Matrix) -> None:
    transpose_in_place(m)
    m.reverse()


def transpose(m: Matrix) -> Matrix:
    return [list(col) for col in zip(*m)]


def rotate_clockwise(m: Matrix) -> Matrix:
    return [list(col) for col in zip(*reversed(m))]


def rotate_by_layers(m: Matrix) -> None:
    """Four-way cyclic swaps, one ring at a time: the version without a transpose."""
    n = len(m)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = m[first][i]
            m[first][i] = m[last - offset][first]
            m[last - offset][first] = m[last][last - offset]
            m[last][last - offset] = m[i][last]
            m[i][last] = top


def show(label: str, m: Matrix) -> None:
    print(label)
    for row in m:
        print("  " + " ".join(f"{v:2}" for v in row))


def main() -> None:
    square = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    show("original:", square)

    m = [row[:] for row in square]
    rotate_clockwise_in_place(m)
    show("clockwise:", m)

    m = [row[:] for row in square]
    rotate_counter_in_place(m)
    show("counter-clockwise:", m)

    wide = [[1, 2, 3], [4, 5, 6]]
    show("2x3 transpose with zip:", transpose(wide))
    show("2x3 rotated with zip:", rotate_clockwise(wide))

    four_turns = [row[:] for row in square]
    for _ in range(4):
        rotate_clockwise_in_place(four_turns)
    print(f"\nfour clockwise turns restore it: {four_turns == square}")

    ok = True
    for n in range(0, 7):
        base = [[r * n + c for c in range(n)] for r in range(n)]
        a, b = [r[:] for r in base], [r[:] for r in base]
        rotate_clockwise_in_place(a)
        rotate_by_layers(b)
        ok &= a == b == rotate_clockwise(base)
    print(f"transpose+reverse, ring swaps and zip agree for n <= 6: {ok}")


if __name__ == "__main__":
    main()
