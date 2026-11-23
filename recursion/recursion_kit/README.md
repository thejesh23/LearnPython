# recursion_kit

Recursive generators for permutations, combinations and subsets, plus recursion that mirrors a problem's shape: nested lists, Tower of Hanoi and Ackermann.

```bash
python3 -m recursion.recursion_kit     # seven examples plus a randomized self-check
```

| Function | Module | Idea |
|---|---|---|
| `permutations(items, unique)` | `combinatorics.py` | swap into slot k, recurse, swap back |
| `combinations(items, k)`, `power_set(items)` | `combinatorics.py` | choose / un-choose, include / exclude |
| `flatten(nested)`, `depth(nested)` | `structure.py` | recursion follows the data's nesting |
| `hanoi(n)` | `structure.py` | solve n - 1, move one, solve n - 1 again |
| `ackermann(m, n)`, `recursion_limit(limit)` | `structure.py` | deep recursion and a context manager that restores the limit |

Standalone versions live next to this folder, e.g. `../tower_of_hanoi.py`.
