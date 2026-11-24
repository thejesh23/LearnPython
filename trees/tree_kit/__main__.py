"""Examples and self-check: python3 -m trees.tree_kit"""

import random
import sys

from . import (
    Autocomplete,
    Node,
    build_bst,
    contains,
    from_level_order,
    inorder,
    is_valid_bst,
    levels,
    lowest_common_ancestor,
    postorder,
    preorder,
    shape,
    to_level_order,
)


def recursive_orders(node: Node | None, out: dict[str, list[int]]) -> None:
    if node is None:
        return
    out["pre"].append(node.value)
    recursive_orders(node.left, out)
    out["in"].append(node.value)
    recursive_orders(node.right, out)
    out["post"].append(node.value)


def naive_shape(node: Node | None) -> tuple[int, int, bool]:
    if node is None:
        return -1, 0, True
    lh, ld, lb = naive_shape(node.left)
    rh, rd, rb = naive_shape(node.right)
    return (1 + max(lh, rh), max(ld, rd, lh + rh + 2),
            lb and rb and abs(lh - rh) <= 1)


def random_tree(rng: random.Random, depth: int) -> Node | None:
    if depth == 0 or rng.random() < 0.25:
        return None
    return Node(rng.randint(0, 99), random_tree(rng, depth - 1),
                random_tree(rng, depth - 1))


def examples() -> None:
    root = from_level_order([1, 2, 3, 4, 5, None, 6, None, None, 7])
    print("1. preorder", list(preorder(root)), "inorder", list(inorder(root)))
    print("2. levels:", levels(root), "round trip:", to_level_order(root))
    print("3. (height, diameter, balanced):", shape(root))
    bst = build_bst([50, 30, 70, 20, 40, 60, 80])
    lca = lowest_common_ancestor(bst, 20, 40)
    print(f"4. BST valid: {is_valid_bst(bst)}, has 60: {contains(bst, 60)}, "
          f"lca(20, 40) = {lca.value if lca else None}")
    print("5. not a BST:", is_valid_bst(Node(5, Node(3), Node(8, Node(4)))))
    chain = None
    for v in range(50_000):
        chain = Node(v, left=chain)
    print(f"6. a 50,000-deep chain: height {shape(chain)[0]}, "
          f"inorder starts {list(inorder(chain))[:3]}")
    ac = Autocomplete(k=3)
    for word, times in [("car", 5), ("care", 7), ("cart", 3), ("cat", 9), ("dog", 2)]:
        ac.add(word, times)
    print("7. suggest('car'):", ac.suggest("car"), "suggest('c'):", ac.suggest("c"))


def self_check() -> None:
    rng = random.Random(17)
    for _ in range(500):
        t = random_tree(rng, 7)
        orders: dict[str, list[int]] = {"pre": [], "in": [], "post": []}
        recursive_orders(t, orders)
        assert list(preorder(t)) == orders["pre"]
        assert list(inorder(t)) == orders["in"]
        assert list(postorder(t)) == orders["post"]
        assert from_level_order(to_level_order(t)) == t
        assert shape(t) == naive_shape(t)
        values = rng.sample(range(1000), rng.randint(1, 40))
        bst = build_bst(values)
        assert list(inorder(bst)) == sorted(values) and is_valid_bst(bst)
        a, b = rng.choice(values), rng.choice(values)
        lca = lowest_common_ancestor(bst, a, b)
        assert lca is not None and min(a, b) <= lca.value <= max(a, b)
    ac = Autocomplete(k=4)
    words = ["".join(rng.choices("abc", k=rng.randint(1, 5))) for _ in range(300)]
    for w in words:
        ac.add(w, rng.randint(1, 5))
    for prefix in {w[:i] for w in words for i in range(len(w) + 1)}:
        ranked = sorted((-c, w) for w, c in ac.counts.items() if w.startswith(prefix))
        assert ac.suggest(prefix) == [w for _, w in ranked[:4]]


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
