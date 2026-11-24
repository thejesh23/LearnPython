# linked_list_kit

The `linked_lists/` samples behind one API, all working on plain `Node`
objects by relinking pointers rather than copying values.

```bash
python3 -m linked_lists.linked_list_kit     # seven examples plus a randomized self-check
```

| Function | Module | What it does |
|---|---|---|
| `Node`, `from_values`, `to_values`, `iter_nodes`, `show` | `nodes.py` | build, walk and print lists |
| `reverse`, `reverse_in_groups(head, k)` | `algorithms.py` | in-place reversal, whole or k at a time |
| `middle`, `length` | `algorithms.py` | tortoise and hare, counting |
| `merge_sorted(a, b)`, `merge_k(lists)` | `algorithms.py` | stable merges, O(N log k) for k lists |
| `is_palindrome(head)` | `algorithms.py` | O(1) space, leaves the list as it found it |
| `add_numbers(a, b)` | `algorithms.py` | digit lists, least significant first |
| `find_cycle(head)` | `algorithms.py` | Floyd: cycle entry and loop length |

Standalone versions live next to this folder, e.g. `../linked_list_cycle.py`.
