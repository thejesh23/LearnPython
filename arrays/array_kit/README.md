# array_kit

The core array patterns in one place: hash-map lookups, two pointers, in-place partitioning, prefix sums, sliding windows and sweeps.

```bash
python3 -m arrays.array_kit     # ten examples plus a randomized self-check
```

| Function | Module | Pattern |
|---|---|---|
| `two_sum`, `three_sum` | `pointers.py` | complement lookup; sort + two pointers |
| `move_zeroes`, `partition3`, `rotate` | `pointers.py` | read/write pointers, Dutch flag, reversal trick |
| `PrefixSums`, `count_subarrays_with_sum` | `scans.py` | O(1) range sums, prefix-sum frequencies |
| `window_max`, `majority`, `merge_intervals` | `scans.py` | monotonic deque, Boyer-Moore vote, sort + sweep |

Every function returns a new list; inputs are never mutated. Standalone versions live next to this folder, e.g. `../sliding_window_maximum.py`.
