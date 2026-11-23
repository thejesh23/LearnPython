"""Tiny seeded datasets, a train/test split, scaling, metrics and the Model base class.

Rows are ``list[float]`` and a dataset is ``(X, y)``: a list of rows plus one
label (classification) or number (regression) per row.
"""

import random

Row = list[float]


def make_blobs(centers: list[Row], n_per_center: int = 50, spread: float = 1.0,
               seed: int = 0) -> tuple[list[Row], list[int]]:
    """Gaussian clouds around each centre; the label is the centre's index."""
    rng = random.Random(seed)
    X, y = [], []
    for label, centre in enumerate(centers):
        for _ in range(n_per_center):
            X.append([rng.gauss(c, spread) for c in centre])
            y.append(label)
    return X, y


def make_regression(n: int, weights: Row, bias: float, noise: float = 0.1,
                    seed: int = 0) -> tuple[list[Row], list[float]]:
    """Points with y = bias + weights . x + Gaussian noise, x uniform in [-5, 5]."""
    rng = random.Random(seed)
    X = [[rng.uniform(-5, 5) for _ in weights] for _ in range(n)]
    y = [bias + sum(w * v for w, v in zip(weights, row)) + rng.gauss(0, noise) for row in X]
    return X, y


def train_test_split(X: list[Row], y: list, test_size: float = 0.25,
                     seed: int = 0) -> tuple[list[Row], list[Row], list, list]:
    """Shuffle once, then hold out ``test_size`` of the rows: X_train, X_test, y_train, y_test."""
    order = list(range(len(X)))
    random.Random(seed).shuffle(order)
    cut = len(X) - int(len(X) * test_size)
    train, test = order[:cut], order[cut:]
    return [X[i] for i in train], [X[i] for i in test], [y[i] for i in train], [y[i] for i in test]


def standardise(X: list[Row]) -> tuple[Row, Row]:
    """Per-column (means, stds); a constant column gets std 1 so it never divides by 0."""
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    stds = [(sum((row[j] - means[j]) ** 2 for row in X) / n) ** 0.5 or 1.0 for j in range(d)]
    return means, stds


def scale(X: list[Row], means: Row, stds: Row) -> list[Row]:
    """Apply a scaling learned by ``standardise`` (on training data only)."""
    return [[(v - m) / s for v, m, s in zip(row, means, stds)] for row in X]


def accuracy(y_true: list, y_pred: list) -> float:
    """Fraction of predictions that match the true label."""
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)


def r2_score(y_true: list[float], y_pred: list[float]) -> float:
    """1 - SSE/SST: 1.0 is a perfect fit, 0.0 is no better than predicting the mean."""
    mean = sum(y_true) / len(y_true)
    sse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    sst = sum((t - mean) ** 2 for t in y_true)
    return 1.0 - sse / sst if sst else float(sse == 0)


class Model:
    """Shared interface: ``fit(X, y)`` returns self, ``predict(X)`` returns a list."""

    def fit(self, X: list[Row], y: list) -> "Model":
        """Learn from rows X and targets y; returns self so calls can chain."""
        raise NotImplementedError

    def predict(self, X: list[Row]) -> list:
        """One prediction per row."""
        raise NotImplementedError

    def score(self, X: list[Row], y: list) -> float:
        """Accuracy on (X, y); regressors override this with R^2."""
        return accuracy(y, self.predict(X))
