"""Three classifiers with curved or piecewise boundaries: k-NN, naive Bayes, a tree."""

import math
from collections import Counter

from .data import Model, Row


class KNNClassifier(Model):
    """No training at all: vote among the k nearest stored rows."""

    def __init__(self, k: int = 5) -> None:
        if k <= 0:
            raise ValueError("k must be positive")
        self.k = k

    def fit(self, X: list[Row], y: list) -> "KNNClassifier":
        """Just remember the data; the model *is* the dataset."""
        self.X, self.y = X, y
        return self

    def predict(self, X: list[Row]) -> list:
        """Majority label of the k closest rows; a tie goes to the nearest of the tied."""
        out = []
        for q in X:
            near = sorted(((math.dist(q, p), i) for i, p in enumerate(self.X)))[: self.k]
            labels = [self.y[i] for _, i in near]  # nearest first
            votes = Counter(labels)
            top = max(votes.values())
            out.append(next(label for label in labels if votes[label] == top))
        return out


class GaussianNB(Model):
    """Bayes' rule, assuming features are independent and normal within each class."""

    def fit(self, X: list[Row], y: list) -> "GaussianNB":
        """Per class: log prior, feature means and variances."""
        self.stats: dict[object, tuple[float, Row, Row]] = {}
        for cls in sorted(set(y)):
            cols = list(zip(*[row for row, label in zip(X, y) if label == cls]))
            means = [sum(c) / len(c) for c in cols]
            var = [max(sum((v - m) ** 2 for v in c) / len(c), 1e-9) for c, m in zip(cols, means)]
            self.stats[cls] = (math.log(len(cols[0]) / len(X)), means, var)
        return self

    def log_posterior(self, cls: object, row: Row) -> float:
        """log P(cls) + sum of log N(x_j; mean_j, var_j), up to a shared constant."""
        prior, means, var = self.stats[cls]
        return prior - sum(0.5 * math.log(2 * math.pi * s) + (x - m) ** 2 / (2 * s)
                           for x, m, s in zip(row, means, var))

    def predict(self, X: list[Row]) -> list:
        """The class with the highest posterior for each row."""
        return [max(self.stats, key=lambda c: self.log_posterior(c, row)) for row in X]


def gini(labels: list) -> float:
    """Chance two random picks disagree: 0 for a pure node."""
    n = len(labels)
    return 1.0 - sum((c / n) ** 2 for c in Counter(labels).values()) if n else 0.0


class DecisionTree(Model):
    """CART: greedily split on the threshold that most reduces gini impurity.

    A leaf is ``(label,)``; an internal node is ``(feature, threshold, left, right)``.
    """

    def __init__(self, max_depth: int = 5) -> None:
        self.max_depth = max_depth

    def fit(self, X: list[Row], y: list) -> "DecisionTree":
        """Grow the tree top-down until nodes are pure or max_depth is reached."""
        self.root = self._grow(X, y, 0)
        return self

    def _grow(self, X: list[Row], y: list, depth: int) -> tuple:
        leaf = (Counter(y).most_common(1)[0][0],)
        if depth == self.max_depth or len(set(y)) == 1:
            return leaf
        best = (gini(y), -1, 0.0)
        for j in range(len(X[0])):
            values = sorted({row[j] for row in X})
            for lo, hi in zip(values, values[1:]):
                t = (lo + hi) / 2  # midway between neighbouring values
                left = [c for row, c in zip(X, y) if row[j] <= t]
                right = [c for row, c in zip(X, y) if row[j] > t]
                impurity = (len(left) * gini(left) + len(right) * gini(right)) / len(y)
                if impurity < best[0] - 1e-12:
                    best = (impurity, j, t)
        _, j, t = best
        if j < 0:
            return leaf  # no split lowers impurity

        def child(go_left: bool) -> tuple:
            idx = [i for i, row in enumerate(X) if (row[j] <= t) == go_left]
            return self._grow([X[i] for i in idx], [y[i] for i in idx], depth + 1)

        return (j, t, child(True), child(False))

    def predict(self, X: list[Row]) -> list:
        """Walk from the root, going left when row[feature] <= threshold."""
        out = []
        for row in X:
            node = self.root
            while len(node) == 4:
                node = node[2] if row[node[0]] <= node[1] else node[3]
            out.append(node[0])
        return out
