# puzzle_kit

One breadth-first solver for any state-space puzzle (water jugs, missionaries and cannibals, sliding tiles), plus FizzBuzz and Game of Life driven by rules stored as data.

```bash
python3 -m puzzles.puzzle_kit     # seven examples plus a randomized self-check (from the repo root)
```

```python
from puzzles.puzzle_kit import bfs_solve, solve_jugs, life_step, period, from_picture

solve_jugs(4, 3, 2)                       # [(0, 0), (0, 3), (3, 0), (3, 3), (4, 2)]
glider = from_picture(".#.\n..#\n###")
period(glider)                            # (4, (1, 1)): repeats every 4 steps, one cell down-right
life_step(glider, rule="B36/S23")         # HighLife: a different rule string, same code
```

| API | Module |
|---|---|
| `bfs_solve(start, is_goal, moves)` | `search.py` |
| `solve_jugs` / `jug_moves`, `solve_missionaries` / `missionaries_moves`, `solve_sliding` / `sliding_moves` | `search.py` |
| `fizzbuzz`, `fizzbuzz_stream`, `FIZZBUZZ` | `rules.py` |
| `parse_rule`, `life_step`, `life_run`, `period`, `from_picture`, `render` | `rules.py` |

The self-check confirms BFS paths are legal and shortest (against a separate reachable-set count) and that Life matches a brute-force neighbour count.
Standalone versions live next to this folder, e.g. `../water_jug_and_bfs_puzzles.py` and `../game_of_life.py`.
