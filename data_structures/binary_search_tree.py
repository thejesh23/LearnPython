"""Binary search tree: left subtree < node < right subtree.

That single invariant gives O(h) search, insert and delete, where h is the
height — O(log n) if the tree is balanced, O(n) if it degenerates into a list
(which is exactly what inserting sorted data does). Balancing is what AVL and
red-black trees add.

Deletion has three cases; the two-child case is the interesting one: replace
the node's value with its in-order successor, then delete that successor,
which by construction has at most one child.
"""

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: "Node | None" = None
    right: "Node | None" = None


class BST:
    def __init__(self, values: list[int] | None = None) -> None:
        self.root: Node | None = None
        for value in values or []:
            self.insert(value)

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Node | None, value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node  # duplicates ignored

    def contains(self, value: int) -> bool:
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def delete(self, value: int) -> None:
        self.root = self._delete(self.root, value)

    def _delete(self, node: Node | None, value: int) -> Node | None:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right  # smallest value in the right subtree
            while successor.left:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return node

    def in_order(self) -> Iterator[int]:
        """In-order traversal of a BST yields the values in sorted order."""

        def walk(node: Node | None) -> Iterator[int]:
            if node:
                yield from walk(node.left)
                yield node.value
                yield from walk(node.right)

        return walk(self.root)

    def height(self) -> int:
        def h(node: Node | None) -> int:
            return 0 if node is None else 1 + max(h(node.left), h(node.right))

        return h(self.root)

    def minimum(self) -> int | None:
        node = self.root
        while node and node.left:
            node = node.left
        return node.value if node else None


def main() -> None:
    tree = BST([50, 30, 70, 20, 40, 60, 80])
    print(f"in-order: {list(tree.in_order())}")
    print(f"contains 40: {tree.contains(40)}, contains 45: {tree.contains(45)}")
    print(f"height: {tree.height()}, min: {tree.minimum()}")

    tree.delete(20)  # leaf
    tree.delete(30)  # one child
    tree.delete(50)  # two children -> successor replaces it
    print(f"after deletes: {list(tree.in_order())}")

    degenerate = BST([1, 2, 3, 4, 5])
    print(f"sorted input degenerates: height {degenerate.height()} for 5 nodes")


if __name__ == "__main__":
    main()
