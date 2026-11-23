"""Linear models trained by batch gradient descent on standardised features.

Scaling first means one learning rate suits every feature; the scaling learned
in ``fit`` is reused in ``predict`` so test rows never leak into training.
"""

import math

from .data import Model, Row, r2_score, scale, standardise


def _dot(w: Row, x: Row) -> float:
    return sum(a * b for a, b in zip(w, x))


def _sigmoid(z: float) -> float:
    """Numerically stable logistic function (never calls exp on a large positive)."""
    return 1 / (1 + math.exp(-z)) if z >= 0 else math.exp(z) / (1 + math.exp(z))


class LinearRegression(Model):
    """Least squares: minimise the mean of (b + w . x - y) ** 2."""

    def __init__(self, lr: float = 0.1, epochs: int = 300) -> None:
        self.lr, self.epochs = lr, epochs

    def fit(self, X: list[Row], y: list[float]) -> "LinearRegression":
        """Learn weights w and bias b by gradient descent."""
        self.means, self.stds = standardise(X)
        Z, n = scale(X, self.means, self.stds), len(X)
        self.w, self.b = [0.0] * len(X[0]), 0.0
        for _ in range(self.epochs):
            errors = [self.b + _dot(self.w, z) - t for z, t in zip(Z, y)]
            self.b -= self.lr * 2 * sum(errors) / n  # d(MSE)/db
            self.w = [w - self.lr * 2 * sum(e * z[j] for e, z in zip(errors, Z)) / n
                      for j, w in enumerate(self.w)]
        return self

    def predict(self, X: list[Row]) -> list[float]:
        """b + w . x for each (scaled) row."""
        return [self.b + _dot(self.w, z) for z in scale(X, self.means, self.stds)]

    def coefficients(self) -> tuple[float, Row]:
        """(bias, weights) in the original, unscaled units."""
        w = [wj / s for wj, s in zip(self.w, self.stds)]
        return self.b - _dot(w, self.means), w

    def score(self, X: list[Row], y: list[float]) -> float:
        """R^2 rather than accuracy, since targets are numbers."""
        return r2_score(y, self.predict(X))


class LogisticRegression(Model):
    """One-vs-rest: a probability sigmoid(b + w . x) per class; the most likely wins."""

    def __init__(self, lr: float = 0.5, epochs: int = 200) -> None:
        self.lr, self.epochs = lr, epochs

    def fit(self, X: list[Row], y: list) -> "LogisticRegression":
        """Fit one binary classifier per class by minimising log loss."""
        self.means, self.stds = standardise(X)
        Z, n = scale(X, self.means, self.stds), len(X)
        self.params: dict[object, tuple[Row, float]] = {}
        for cls in sorted(set(y)):
            target = [float(label == cls) for label in y]
            w, b = [0.0] * len(X[0]), 0.0
            for _ in range(self.epochs):
                errors = [_sigmoid(b + _dot(w, z)) - t for z, t in zip(Z, target)]
                b -= self.lr * sum(errors) / n  # log-loss gradient is just (p - t) * x
                w = [wj - self.lr * sum(e * z[j] for e, z in zip(errors, Z)) / n
                     for j, wj in enumerate(w)]
            self.params[cls] = (w, b)
        return self

    def predict_proba(self, X: list[Row]) -> list[dict]:
        """Per-row {class: probability of that class vs the rest}."""
        return [{c: _sigmoid(b + _dot(w, z)) for c, (w, b) in self.params.items()}
                for z in scale(X, self.means, self.stds)]

    def predict(self, X: list[Row]) -> list:
        """The class with the highest one-vs-rest probability."""
        return [max(p, key=p.get) for p in self.predict_proba(X)]
