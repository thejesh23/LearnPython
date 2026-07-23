"""Gaussian naive Bayes: classify by the most probable class under independence.

Bayes' rule says the posterior of a class given the features is proportional to
the prior times the likelihood. Naive Bayes makes the strong simplifying
assumption that the features are conditionally independent given the class, so
the joint likelihood factorises into a product of one-dimensional densities.
For continuous features each of those is modelled as a Gaussian, fitted with the
per-class mean and variance of that feature.

Training is a single pass that just accumulates counts, sums and sums of
squares, so it is O(n * d) and needs no iteration. Prediction sums log-priors
and log-densities to avoid underflow from multiplying many small probabilities,
and picks the class with the largest log-posterior. Despite the unrealistic
independence assumption the classifier is often surprisingly accurate, which is
why it remains a strong, cheap baseline. Accuracy is reported on held-back rows.
"""

import math
from collections import defaultdict

Row = list[float]


class GaussianNB:
    """Per-class feature means and variances, plus class log-priors."""

    def __init__(self) -> None:
        self.means: dict[str, list[float]] = {}
        self.variances: dict[str, list[float]] = {}
        self.log_prior: dict[str, float] = {}

    def fit(self, rows: list[Row], labels: list[str]) -> "GaussianNB":
        n = len(rows)
        d = len(rows[0])
        groups: dict[str, list[Row]] = defaultdict(list)
        for r, y in zip(rows, labels):
            groups[y].append(r)
        for cls, members in groups.items():
            m = len(members)
            means = [sum(r[j] for r in members) / m for j in range(d)]
            # Variance with a small floor so a constant feature never divides
            # by zero in the Gaussian density.
            var = [max(sum((r[j] - means[j]) ** 2 for r in members) / m, 1e-9)
                   for j in range(d)]
            self.means[cls] = means
            self.variances[cls] = var
            self.log_prior[cls] = math.log(m / n)
        return self

    def _log_likelihood(self, cls: str, row: Row) -> float:
        total = self.log_prior[cls]
        means = self.means[cls]
        var = self.variances[cls]
        for j, x in enumerate(row):
            # Log of the Gaussian density N(x; mean, var).
            total += -0.5 * math.log(2 * math.pi * var[j]) \
                - (x - means[j]) ** 2 / (2 * var[j])
        return total

    def predict(self, row: Row) -> str:
        return max(self.means, key=lambda c: self._log_likelihood(c, row))


def accuracy(model: GaussianNB, rows: list[Row], labels: list[str]) -> float:
    hits = sum(1 for r, y in zip(rows, labels) if model.predict(r) == y)
    return hits / len(labels)


def main() -> None:
    import random

    rng = random.Random(0)

    # Two Gaussian blobs in 2D, well separated but overlapping a little.
    def blob(cx: float, cy: float, n: int) -> list[Row]:
        return [[rng.gauss(cx, 1.0), rng.gauss(cy, 1.0)] for _ in range(n)]

    rows = blob(0.0, 0.0, 60) + blob(4.0, 4.0, 60)
    labels = ["A"] * 60 + ["B"] * 60

    # Shuffle and split 70/30 into train and test.
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    cut = int(0.7 * len(idx))
    tr, te = idx[:cut], idx[cut:]
    train_x = [rows[i] for i in tr]
    train_y = [labels[i] for i in tr]
    test_x = [rows[i] for i in te]
    test_y = [labels[i] for i in te]

    model = GaussianNB().fit(train_x, train_y)
    print("fitted parameters")
    for cls in sorted(model.means):
        print(f"  class {cls}: mean={[round(v, 3) for v in model.means[cls]]}, "
              f"var={[round(v, 3) for v in model.variances[cls]]}")

    print(f"\ntrain accuracy: {accuracy(model, train_x, train_y) * 100:.2f}%")
    print(f"test accuracy:  {accuracy(model, test_x, test_y) * 100:.2f}%")

    print("\nsample predictions (features -> class)")
    for r in ([0.2, -0.1], [3.8, 4.2], [2.0, 2.0]):
        print(f"  {r} -> {model.predict(r)}")

    # Edge case: a clearly separable one-feature problem, expect 100%.
    xs = [[1.0], [1.2], [0.9], [5.0], [5.1], [4.8]]
    ys = ["low", "low", "low", "high", "high", "high"]
    tiny = GaussianNB().fit(xs, ys)
    print(f"\nseparable 1D set, train accuracy: "
          f"{accuracy(tiny, xs, ys) * 100:.2f}%")
    print(f"  predict [1.1] -> {tiny.predict([1.1])}, "
          f"[4.9] -> {tiny.predict([4.9])}")


if __name__ == "__main__":
    main()
