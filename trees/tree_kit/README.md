# tree_kit

The `trees/` samples put together on one `Node` type. Every traversal uses an
explicit stack or queue, so a 50,000-deep tree works as well as a small one.

```bash
python3 -m trees.tree_kit     # seven examples plus a randomized self-check
```

| Name | Module | What it does |
|---|---|---|
| `Node`, `from_level_order`, `to_level_order` | `binary_tree.py` | build and serialise in LeetCode's level-order format |
| `preorder`, `inorder`, `postorder`, `levels` | `binary_tree.py` | lazy, iterative traversals |
| `shape(root)` | `binary_tree.py` | height, diameter and balance in one post-order pass |
| `insert`, `build_bst`, `contains`, `is_valid_bst` | `bst.py` | binary search tree basics |
| `lowest_common_ancestor(root, a, b)` | `bst.py` | O(height) LCA using the ordering |
| `Autocomplete(k)` | `autocomplete.py` | a trie caching the top k completions per prefix |

Standalone versions live next to this folder, e.g. `../binary_tree_traversals.py`.
