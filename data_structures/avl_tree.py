"""AVL tree: a BST that rebalances on every insert, keeping height O(log n).

The invariant is strict — for every node, |height(left) - height(right)| <= 1.
After an insert the path back to the root is checked, and the first unbalanced
node is fixed with one of four rotations:

    left-left    -> rotate right
    right-right  -> rotate left
    left-right   -> rotate the child left, then rotate right
    right-left   -> rotate the child right, then rotate left

That keeps lookups at a guaranteed O(log n), unlike a plain BST which degrades
to O(n) on sorted input. Red-black trees relax the invariant (height within 2x)
for fewer rotations — which is why they back most standard-library maps.
"""

from dataclasses import dataclass


@dataclass
class Node:
    value: int
    height: int = 1
    left: "Node | None" = None
    right: "Node | None" = None


def height(node: Node | None) -> int:
    return node.height if node else 0


def balance_factor(node: Node) -> int:
    return height(node.left) - height(node.right)


def update_height(node: Node) -> None:
    node.height = 1 + max(height(node.left), height(node.right))


def rotate_right(y: Node) -> Node:
    x = y.left
    y.left, x.right = x.right, y
    update_height(y)
    update_height(x)
    return x


def rotate_left(x: Node) -> Node:
    y = x.right
    x.right, y.left = y.left, x
    update_height(x)
    update_height(y)
    return y


class AVLTree:
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
        else:
            return node
        update_height(node)

        balance = balance_factor(node)
        if balance > 1 and value < node.left.value:  # left-left
            return rotate_right(node)
        if balance < -1 and value > node.right.value:  # right-right
            return rotate_left(node)
        if balance > 1:  # left-right
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if balance < -1:  # right-left
            node.right = rotate_right(node.right)
            return rotate_left(node)
        return node

    def contains(self, value: int) -> bool:
        node = self.root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def in_order(self) -> list[int]:
        out: list[int] = []

        def walk(node: Node | None) -> None:
            if node:
                walk(node.left)
                out.append(node.value)
                walk(node.right)

        walk(self.root)
        return out

    def is_balanced(self) -> bool:
        def check(node: Node | None) -> bool:
            if node is None:
                return True
            return abs(balance_factor(node)) <= 1 and check(node.left) and check(node.right)

        return check(self.root)


def main() -> None:
    # Sorted input: the case that ruins a plain BST.
    avl = AVLTree(list(range(1, 16)))
    print(f"15 sorted inserts -> height {height(avl.root)} (a plain BST would be 15)")
    print(f"balanced: {avl.is_balanced()}, root value {avl.root.value}")
    print(f"in-order: {avl.in_order()}")
    print(f"contains 7: {avl.contains(7)}, contains 99: {avl.contains(99)}")

    # Each rotation case, one at a time.
    print(f"left-left  [3,2,1] root -> {AVLTree([3, 2, 1]).root.value}")
    print(f"right-right[1,2,3] root -> {AVLTree([1, 2, 3]).root.value}")
    print(f"left-right [3,1,2] root -> {AVLTree([3, 1, 2]).root.value}")
    print(f"right-left [1,3,2] root -> {AVLTree([1, 3, 2]).root.value}")


if __name__ == "__main__":
    main()
