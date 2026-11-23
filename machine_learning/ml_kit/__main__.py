"""Examples and self-check: python3 -m machine_learning.ml_kit"""

import math
import random
import statistics
import sys

from . import (
    DecisionTree,
    GaussianNB,
    KNNClassifier,
    LinearRegression,
    LogisticRegression,
    gini,
    make_blobs,
    make_regression,
    train_test_split,
)

CENTERS = [[2.0, 2.0], [6.0, 6.0], [2.0, 6.0]]


def examples() -> None:
    X, y = make_blobs(CENTERS, n_per_center=50, spread=1.0, seed=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, seed=1)
    print(f"1. three blobs: {len(X_train)} training rows, {len(X_test)} test rows")
    for i, model in enumerate([LogisticRegression(), KNNClassifier(k=5), GaussianNB(), DecisionTree(3)], 2):
        acc = model.fit(X_train, y_train).score(X_test, y_test)
        print(f"{i}. {type(model).__name__:<18} test accuracy {acc:.3f}")
    probs = LogisticRegression().fit(X_train, y_train).predict_proba([[4.0, 4.0]])[0]
    print("6. one-vs-rest probabilities at (4, 4):", {c: round(p, 3) for c, p in probs.items()})
    X, y = make_regression(200, weights=[3.0, -2.0], bias=1.0, noise=0.5, seed=2)
    reg = LinearRegression().fit(X, y)
    bias, weights = reg.coefficients()
    print(f"7. linear fit of y = 1 + 3a - 2b: bias {bias:.2f}, weights {[round(w, 2) for w in weights]}, "
          f"R^2 {reg.score(X, y):.4f}")


def nb_brute_force(X: list, y: list, row: list) -> int:
    """Naive Bayes written straight from the formula with statistics.NormalDist."""
    def posterior(cls: int) -> float:
        rows = [r for r, label in zip(X, y) if label == cls]
        p = len(rows) / len(X)
        for j, x in enumerate(row):
            col = [r[j] for r in rows]
            p *= statistics.NormalDist(statistics.fmean(col), statistics.pstdev(col)).pdf(x)
        return p
    return max(sorted(set(y)), key=posterior)


def self_check() -> None:
    rng = random.Random(9)
    X, y = make_blobs(CENTERS, n_per_center=40, spread=0.8, seed=9)
    X_train, X_test, y_train, y_test = train_test_split(X, y, seed=9)
    assert sorted(X_train + X_test) == sorted(X) and len(X_test) == 30
    for model in (LogisticRegression(), KNNClassifier(), GaussianNB(), DecisionTree()):
        acc = model.fit(X_train, y_train).score(X_test, y_test)
        assert acc >= 0.9, (type(model).__name__, acc)
    assert DecisionTree(max_depth=20).fit(X, y).score(X, y) == 1.0  # distinct rows: memorised
    knn1 = KNNClassifier(k=1).fit(X_train, y_train)
    nb = GaussianNB().fit(X_train, y_train)
    queries = [[rng.uniform(0, 8), rng.uniform(0, 8)] for _ in range(100)]
    for q, pred_knn, pred_nb in zip(queries, knn1.predict(queries), nb.predict(queries)):
        nearest = min(range(len(X_train)), key=lambda i: math.dist(q, X_train[i]))
        assert pred_knn == y_train[nearest]
        assert pred_nb == nb_brute_force(X_train, y_train, q)
    # One feature: gradient descent must agree with the closed-form least-squares line.
    xs = [[rng.uniform(-3, 3)] for _ in range(50)]
    ys = [0.5 - 1.5 * x[0] + rng.gauss(0, 0.3) for x in xs]
    slope, intercept = statistics.linear_regression([x[0] for x in xs], ys)
    bias, (w,) = LinearRegression().fit(xs, ys).coefficients()
    assert math.isclose(w, slope, abs_tol=1e-6) and math.isclose(bias, intercept, abs_tol=1e-6)
    assert gini(["a", "a"]) == 0.0 and gini(["a", "b"]) == 0.5 and gini([]) == 0.0


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
