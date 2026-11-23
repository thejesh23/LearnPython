# greedy_kit

Greedy algorithms where one local rule is provably optimal: earliest finish, earliest free room, furthest reach, best density and rarest-first merging.

```bash
python3 -m greedy.greedy_kit     # six examples plus a randomized self-check against brute force
```

| Function | Module | Greedy rule |
|---|---|---|
| `select_activities(activities)` | `scheduling.py` | take the activity that finishes first |
| `assign_rooms(meetings)`, `min_rooms(meetings)` | `scheduling.py` | reuse the room that frees up earliest |
| `min_jumps(nums)` | `scheduling.py` | jump to the window with the furthest reach |
| `fractional_knapsack(items, capacity)` | `priority.py` | highest value per unit weight first |
| `huffman_codes(text)`, `encode`, `decode` | `priority.py` | merge the two rarest subtrees |

Intervals are `(name, start, end)` tuples, and touching endpoints do not overlap. Standalone versions live next to this folder, e.g. `../huffman_encoding.py`.
