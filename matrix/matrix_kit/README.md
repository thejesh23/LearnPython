# matrix_kit

The `matrix/` samples put together: an immutable `Matrix` value that plugs
into Python's operators, plus functions that walk or transform plain
list-of-lists grids in place.

```bash
python3 -m matrix.matrix_kit     # seven examples plus a randomized self-check
```

| Name | Module | What it does |
|---|---|---|
| `Matrix(rows)`, `Matrix.identity(n)` | `matrix.py` | validated, hashable, `==`, `+`, `@`, `**` (repeated squaring) |
| `.transpose()`, `.rotate(clockwise=True)`, `.spiral()` | `matrix.py` | new matrices, any shape |
| `.is_square()`, `.is_symmetric()`, `.is_identity()`, `.is_toeplitz()` | `matrix.py` | shape checks |
| `spiral(grid)` | `grid.py` | clockwise walk with four shrinking walls |
| `rotate_in_place(grid, clockwise=True)` | `grid.py` | square grids, O(1) extra space |
| `set_zeroes(grid)` | `grid.py` | zero rows and columns using the first row and column as markers |

Standalone versions live next to this folder, e.g. `../spiral_order.py`.
