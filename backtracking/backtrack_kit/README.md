# backtrack_kit

Five backtracking searches built on the same choose / recurse / undo loop, each with the pruning that makes it fast.

```bash
python3 -m backtracking.backtrack_kit     # six examples plus a randomized self-check
```

| Function | Module | Pruning |
|---|---|---|
| `n_queens(n, limit)` | `search.py` | column and diagonal sets, O(1) conflict test |
| `subset_sums(numbers, target)` | `search.py` | sorted input, suffix sums, duplicate skipping |
| `permutations_where(items, prefix_ok)` | `search.py` | reject a bad prefix, not each full ordering |
| `word_path(grid, word)` | `search.py` | stop at the first mismatched letter |
| `solve_sudoku(grid)`, `is_solved(grid)` | `sudoku.py` | bitmask candidates, most-constrained cell first |

Inputs are never mutated. Standalone versions live next to this folder, e.g. `../sudoku_solver.py`.
