"""CART: a classification tree grown one greedy yes-or-no question at a time.

Impurity is measured with the gini index, 1 - sum(p_c^2) over the class
proportions in a node. It is zero when a node holds a single class and largest
when the classes are evenly mixed. A split is scored by the weighted average
impurity of the two children, and the gain is the parent's impurity minus that
average.

Growing the tree means searching, at every node, every feature and every
threshold that could separate two adjacent observed values, and keeping the split
with the largest gain. That is O(n * d) candidate splits per node with sorting,
and it is greedy: the best split now may not belong to the best tree overall, but
searching all trees is intractable.

Left unchecked the tree keeps splitting until each leaf is pure, which memorises
the training set. A maximum depth, a minimum node size and a minimum gain are the
three simple brakes used here. Prediction walks one root-to-leaf path, so it costs
O(depth).
"""

from collections import Counter
from dataclasses import dataclass


Row = list[float]


def gini(labels: list[str]) -> float:
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    return 1.0 - sum((c / n) ** 2 for c in counts.values())


@dataclass
class Node:
    """Either a leaf (prediction set) or an internal split (feature/threshold)."""
    prediction: str | None = None
    feature: int | None = None
    threshold: float | None = None
    left: "Node | None" = None
    right: "Node | None" = None
    samples: int = 0
    impurity: float = 0.0
    distribution: dict[str, int] | None = None

    @property
    def is_leaf(self) -> bool:
        return self.prediction is not None


def best_split(rows: list[Row], labels: list[str]
               ) -> tuple[float, int | None, float | None]:
    """Return (gain, feature, threshold) for the highest-gain split, if any."""
    n = len(rows)
    parent = gini(labels)
    best = (0.0, None, None)
    for feature in range(len(rows[0])):
        order = sorted(range(n), key=lambda i: rows[i][feature])
        values = [rows[i][feature] for i in order]
        sorted_labels = [labels[i] for i in order]
        for i in range(1, n):
            if values[i] == values[i - 1]:
                continue  # no threshold can separate equal values
            threshold = (values[i] + values[i - 1]) / 2
            left, right = sorted_labels[:i], sorted_labels[i:]
            weighted = (len(left) * gini(left) + len(right) * gini(right)) / n
            gain = parent - weighted
            if gain > best[0]:
                best = (gain, feature, threshold)
    return best


def majority(labels: list[str]) -> str:
    """Most common label; ties broken alphabetically so output is stable."""
    counts = Counter(labels)
    top = max(counts.values())
    return min(label for label, c in counts.items() if c == top)


def build(rows: list[Row], labels: list[str], max_depth: int = 4,
          min_samples: int = 2, min_gain: float = 1e-7, depth: int = 0) -> Node:
    impurity = gini(labels)
    node = Node(samples=len(labels), impurity=impurity,
                distribution=dict(sorted(Counter(labels).items())))
    if (depth >= max_depth or len(labels) < min_samples or impurity == 0.0):
        node.prediction = majority(labels)
        return node

    gain, feature, threshold = best_split(rows, labels)
    if feature is None or gain < min_gain:
        node.prediction = majority(labels)
        return node

    left_idx = [i for i, r in enumerate(rows) if r[feature] <= threshold]
    right_idx = [i for i, r in enumerate(rows) if r[feature] > threshold]
    node.feature, node.threshold = feature, threshold
    node.left = build([rows[i] for i in left_idx], [labels[i] for i in left_idx],
                      max_depth, min_samples, min_gain, depth + 1)
    node.right = build([rows[i] for i in right_idx], [labels[i] for i in right_idx],
                       max_depth, min_samples, min_gain, depth + 1)
    return node


def predict(node: Node, row: Row) -> str:
    while not node.is_leaf:
        assert node.feature is not None and node.threshold is not None
        node = node.left if row[node.feature] <= node.threshold else node.right
        assert node is not None
    assert node.prediction is not None
    return node.prediction


def render(node: Node, names: list[str], indent: str = "",
           branch: str = "") -> list[str]:
    head = f"{indent}{branch}"
    if node.is_leaf:
        return [f"{head}predict {node.prediction}  "
                f"(n={node.samples}, gini={node.impurity:.3f}, "
                f"{node.distribution})"]
    label = names[node.feature] if node.feature is not None else "?"
    lines = [f"{head}{label} <= {node.threshold:.3f}?  "
             f"(n={node.samples}, gini={node.impurity:.3f})"]
    child_indent = indent + ("    " if branch else "")
    lines += render(node.left, names, child_indent, "yes: ")
    lines += render(node.right, names, child_indent, "no:  ")
    return lines


def depth_of(node: Node) -> int:
    if node.is_leaf:
        return 0
    return 1 + max(depth_of(node.left), depth_of(node.right))


def accuracy(node: Node, rows: list[Row], labels: list[str]) -> float:
    hits = sum(1 for r, y in zip(rows, labels) if predict(node, r) == y)
    return hits / len(labels)


def main() -> None:
    # A tiny weather set: outlook is coded 0=sunny 1=overcast 2=rain.
    names = ["outlook", "temperature", "humidity", "windy"]
    rows: list[Row] = [
        [0, 29, 85, 0], [0, 27, 90, 1], [1, 28, 78, 0], [2, 21, 96, 0],
        [2, 20, 80, 0], [2, 18, 70, 1], [1, 18, 65, 1], [0, 22, 95, 0],
        [0, 21, 70, 0], [2, 24, 80, 0], [0, 24, 70, 1], [1, 22, 90, 1],
        [1, 27, 75, 0], [2, 22, 91, 1],
    ]
    labels = ["no", "no", "yes", "yes", "yes", "no", "yes", "no",
              "yes", "yes", "yes", "yes", "yes", "no"]

    tree = build(rows, labels, max_depth=3)
    print("learned tree (max_depth=3)")
    for line in render(tree, names):
        print("  " + line)
    print(f"\ndepth {depth_of(tree)}, "
          f"training accuracy {accuracy(tree, rows, labels) * 100:.2f}%")

    print("\npredictions")
    for row in ([1, 25, 70, 0], [0, 30, 95, 0], [2, 20, 90, 1]):
        print(f"  {row} -> {predict(tree, row)}")

    # The root split is the single most informative question in the data.
    gain, feature, threshold = best_split(rows, labels)
    print(f"\nbest root split: {names[feature]} <= {threshold:.2f}, "
          f"gain {gain:.4f} (parent gini {gini(labels):.4f})")

    print("\ndepth controls how much the tree memorises")
    for d in (0, 1, 2, 3, 5, 10):
        t = build(rows, labels, max_depth=d)
        print(f"  max_depth {d:>2}: actual depth {depth_of(t)}, "
              f"training accuracy {accuracy(t, rows, labels) * 100:>6.2f}%")

    print("\ngini impurity")
    print(f"  all one class:        {gini(['a'] * 6):.4f}")
    print(f"  50/50 two classes:    {gini(['a', 'a', 'b', 'b']):.4f}")
    print(f"  even over three:      {gini(['a', 'b', 'c']):.4f}")
    print(f"  empty node:           {gini([]):.4f}")

    print("\nedge cases")
    pure = build([[1.0], [2.0]], ["yes", "yes"])
    print(f"  pure input -> leaf: {pure.is_leaf}, predicts {pure.prediction}")
    same = build([[1.0], [1.0]], ["yes", "no"])
    print(f"  identical rows, conflicting labels -> leaf: {same.is_leaf}, "
          f"predicts {same.prediction}")
    one = build([[3.0, 4.0]], ["no"])
    print(f"  single row: {one.prediction}, n={one.samples}")


if __name__ == "__main__":
    main()
