"""tree_kit: binary trees, BSTs and ranked autocomplete, all stack-safe.

    >>> from trees.tree_kit import from_level_order, levels, shape
    >>> root = from_level_order([1, 2, 3, None, 4])
    >>> levels(root), shape(root)
    ([[1], [2, 3], [4]], (2, 3, True))
"""

from .autocomplete import Autocomplete
from .binary_tree import (
    Node,
    from_level_order,
    inorder,
    levels,
    postorder,
    preorder,
    shape,
    to_level_order,
)
from .bst import build_bst, contains, insert, is_valid_bst, lowest_common_ancestor

__all__ = [
    "Node",
    "from_level_order",
    "to_level_order",
    "preorder",
    "inorder",
    "postorder",
    "levels",
    "shape",
    "insert",
    "build_bst",
    "contains",
    "is_valid_bst",
    "lowest_common_ancestor",
    "Autocomplete",
]
