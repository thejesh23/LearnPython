"""Binary search tree helpers on the same Node type."""

from .binary_tree import Node, inorder


def insert(root: Node | None, value: int) -> Node:
    """Iterative insert; duplicates are ignored."""
    if root is None:
        return Node(value)
    node = root
    while True:
        if value == node.value:
            return root
        side = "left" if value < node.value else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, Node(value))
            return root
        node = child


def build_bst(values: list[int]) -> Node | None:
    root = None
    for v in values:
        root = insert(root, v)
    return root


def contains(root: Node | None, value: int) -> bool:
    while root and root.value != value:
        root = root.left if value < root.value else root.right
    return root is not None


def is_valid_bst(root: Node | None) -> bool:
    """Strictly increasing inorder sequence, checked lazily."""
    previous = None
    for value in inorder(root):
        if previous is not None and value <= previous:
            return False
        previous = value
    return True


def lowest_common_ancestor(root: Node | None, a: int, b: int) -> Node | None:
    """Walk down until a and b fall on different sides (O(height))."""
    node = root
    while node:
        if a < node.value and b < node.value:
            node = node.left
        elif a > node.value and b > node.value:
            node = node.right
        else:
            return node
    return None
