"""Gradient boosting: build a strong regressor from many tiny weak ones.

Boosting fits an additive model one term at a time. Each new term is trained on
the errors the running ensemble still makes, so it concentrates on what has not
yet been explained. For squared-error regression the gradient of the loss is
just the residual (target minus current prediction), so gradient boosting here
reduces to repeatedly fitting a small tree to the current residuals and adding a
shrunken version of it to the prediction.

The weak learner is a depth-1 regression tree, a stump: it picks the single
feature and threshold whose split most reduces the squared error, then predicts
the mean target on each side. A stump alone underfits badly, but summing a few
hundred of them, each nudged in by a small learning rate, produces a flexible
curve. The learning rate trades accuracy for the number of stages, and the
training loss is shown falling monotonically as stages are added.
"""

Row = list[float]


class Stump:
    """A depth-1 regression tree: one split, two constant predictions."""

    def __init__(self, feature: int, threshold: float,
                 left: float, right: float) -> None:
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right

    def predict(self, row: Row) -> float:
        return self.left if row[self.feature] <= self.threshold else self.right


def fit_stump(rows: list[Row], targets: list[float]) -> Stump:
    """Choose the split minimising total squared error of the two leaf means."""
    n = len(rows)
    d = len(rows[0])
    best_sse = float("inf")
    best = Stump(0, 0.0, 0.0, 0.0)
    for feature in range(d):
        order = sorted(range(n), key=lambda i: rows[i][feature])
        vals = [rows[i][feature] for i in order]
        tgt = [targets[i] for i in order]
        # Prefix sums let us evaluate every threshold in one linear sweep.
        total = sum(tgt)
        left_sum = 0.0
        for i in range(1, n):
            left_sum += tgt[i - 1]
            if vals[i] == vals[i - 1]:
                continue
            right_sum = total - left_sum
            left_mean = left_sum / i
            right_mean = right_sum / (n - i)
            # SSE = sum(y^2) - (leaf_sum^2 / count); constant sum(y^2) dropped.
            sse = -(left_sum ** 2 / i + right_sum ** 2 / (n - i))
            if sse < best_sse:
                best_sse = sse
                thr = (vals[i] + vals[i - 1]) / 2
                best = Stump(feature, thr, left_mean, right_mean)
    return best


class GradientBoost:
    """Sum of shrunken stumps fitted stage by stage to the residuals."""

    def __init__(self, n_stages: int = 200, learning_rate: float = 0.1) -> None:
        self.n_stages = n_stages
        self.learning_rate = learning_rate
        self.base = 0.0
        self.stumps: list[Stump] = []

    def fit(self, rows: list[Row], y: list[float]) -> "GradientBoost":
        self.base = sum(y) / len(y)  # start from the mean
        pred = [self.base] * len(y)
        self.history: list[float] = []
        for _ in range(self.n_stages):
            residual = [y[i] - pred[i] for i in range(len(y))]
            stump = fit_stump(rows, residual)
            self.stumps.append(stump)
            for i in range(len(y)):
                pred[i] += self.learning_rate * stump.predict(rows[i])
            mse = sum((y[i] - pred[i]) ** 2 for i in range(len(y))) / len(y)
            self.history.append(mse)
        return self

    def predict(self, row: Row) -> float:
        return self.base + self.learning_rate * sum(
            s.predict(row) for s in self.stumps)


def main() -> None:
    import math
    import random

    rng = random.Random(11)

    # One-feature nonlinear target with a bit of noise: y = sin(x) + x/3.
    rows: list[Row] = []
    y: list[float] = []
    for _ in range(120):
        x = rng.uniform(0, 6)
        rows.append([x])
        y.append(math.sin(x) + x / 3 + rng.gauss(0, 0.05))

    model = GradientBoost(n_stages=200, learning_rate=0.1).fit(rows, y)

    print("training MSE as stages are added")
    for stage in (1, 5, 20, 50, 100, 200):
        print(f"  after {stage:>3} stumps: MSE {model.history[stage - 1]:.5f}")

    # Loss must fall over training.
    print(f"\nfirst-stage MSE {model.history[0]:.5f} -> "
          f"final MSE {model.history[-1]:.5f}")
    print(f"loss decreased: {model.history[-1] < model.history[0]}")
    monotone = all(model.history[i] <= model.history[i - 1] + 1e-9
                   for i in range(1, len(model.history)))
    print(f"loss is (weakly) monotone: {monotone}")

    # Predictions track the true function between the training noise.
    print("\nx -> prediction vs true sin(x)+x/3")
    for x in (0.5, 2.0, 3.5, 5.0):
        true = math.sin(x) + x / 3
        print(f"  x={x}: pred {model.predict([x]):.4f}, true {true:.4f}")

    # A single stump underfits; the ensemble does far better.
    one = GradientBoost(n_stages=1, learning_rate=1.0).fit(rows, y)
    print(f"\nsingle stump MSE:  {one.history[-1]:.5f}")
    print(f"200-stump MSE:     {model.history[-1]:.5f}")


if __name__ == "__main__":
    main()
