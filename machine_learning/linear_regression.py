"""Linear regression: fitting a straight line, twice, and getting the same answer.

With a single feature the least squares solution is a closed form you can derive
in a few lines: set the derivative of the squared error to zero and you get
slope = cov(x, y) / var(x), intercept = mean(y) - slope * mean(x). No iteration,
no learning rate, exact to floating point.

With many features the same idea needs linear algebra, so instead we walk downhill.
Batch gradient descent computes the average gradient of the squared error over the
whole dataset and steps against it. The error surface for linear regression is a
bowl (convex), so any small enough step size converges to the same unique minimum
the closed form finds. That agreement is the point of this file.

Quality is reported as R^2, the fraction of the variance in y the model explains:
1 - SSE/SST. R^2 = 1 is a perfect fit, 0 is no better than predicting the mean, and
negative means the model is worse than the mean. Fitting costs O(n) for one feature
and O(iters * n * d) for gradient descent.
"""

import random


def fit_closed_form(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Return (intercept, slope) minimising squared error for one feature."""
    n = len(xs)
    if n == 0:
        raise ValueError("need at least one point")
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    var = sum((x - mean_x) ** 2 for x in xs)
    if var == 0:
        # Every x is identical: no slope is identifiable, predict the mean.
        return mean_y, 0.0
    slope = cov / var
    return mean_y - slope * mean_x, slope


def predict(rows: list[list[float]], weights: list[float], bias: float) -> list[float]:
    return [bias + sum(w * v for w, v in zip(weights, row)) for row in rows]


def fit_gradient_descent(rows: list[list[float]], ys: list[float],
                         lr: float = 0.05, iters: int = 20000
                         ) -> tuple[float, list[float], list[float]]:
    """Return (bias, weights, loss history) from batch gradient descent."""
    n = len(rows)
    d = len(rows[0])
    weights = [0.0] * d
    bias = 0.0
    history: list[float] = []
    for step in range(iters):
        preds = predict(rows, weights, bias)
        errors = [p - y for p, y in zip(preds, ys)]
        # d/dw of mean squared error; the factor 2 is folded into lr by convention
        # in many texts, but we keep it explicit so the maths matches the docstring.
        grad_b = 2 / n * sum(errors)
        grad_w = [2 / n * sum(e * row[j] for e, row in zip(errors, rows))
                  for j in range(d)]
        bias -= lr * grad_b
        weights = [w - lr * g for w, g in zip(weights, grad_w)]
        if step % (iters // 5) == 0:
            history.append(sum(e * e for e in errors) / n)
    return bias, weights, history


def r_squared(ys: list[float], preds: list[float]) -> float:
    mean_y = sum(ys) / len(ys)
    sse = sum((y - p) ** 2 for y, p in zip(ys, preds))
    sst = sum((y - mean_y) ** 2 for y in ys)
    if sst == 0:
        return 1.0 if sse == 0 else 0.0
    return 1 - sse / sst


def standardise(rows: list[list[float]]) -> tuple[list[list[float]],
                                                  list[float], list[float]]:
    """Centre and scale each column; gradient descent converges far faster."""
    n, d = len(rows), len(rows[0])
    means = [sum(r[j] for r in rows) / n for j in range(d)]
    stds = []
    for j in range(d):
        var = sum((r[j] - means[j]) ** 2 for r in rows) / n
        stds.append(var ** 0.5 or 1.0)
    scaled = [[(r[j] - means[j]) / stds[j] for j in range(d)] for r in rows]
    return scaled, means, stds


def main() -> None:
    rng = random.Random(7)

    # --- one feature: closed form versus gradient descent -------------------
    xs = [i / 2 for i in range(40)]
    ys = [3.0 + 2.5 * x + rng.gauss(0, 1.0) for x in xs]

    intercept, slope = fit_closed_form(xs, ys)
    print("single feature, true model y = 3.0 + 2.5x + noise")
    print(f"  closed form:      intercept {intercept:.4f}, slope {slope:.4f}")

    rows = [[x] for x in xs]
    bias, weights, history = fit_gradient_descent(rows, ys, lr=0.005, iters=20000)
    print(f"  gradient descent: intercept {bias:.4f}, slope {weights[0]:.4f}")
    print(f"  max disagreement: "
          f"{max(abs(intercept - bias), abs(slope - weights[0])):.6f}")

    closed_preds = [intercept + slope * x for x in xs]
    print(f"  R^2 closed form:  {r_squared(ys, closed_preds):.4f}")
    print(f"  R^2 descent:      {r_squared(ys, predict(rows, weights, bias)):.4f}")
    print("  loss every 4000 iterations: " +
          ", ".join(f"{h:.3f}" for h in history))

    # --- three features: only gradient descent applies here -----------------
    true_w = [1.5, -2.0, 0.75]
    multi = [[rng.uniform(0, 10), rng.uniform(-5, 5), rng.uniform(0, 3)]
             for _ in range(200)]
    multi_y = [4.0 + sum(w * v for w, v in zip(true_w, row)) + rng.gauss(0, 0.5)
               for row in multi]

    scaled, means, stds = standardise(multi)
    s_bias, s_weights, _ = fit_gradient_descent(scaled, multi_y, lr=0.1, iters=5000)
    # Undo the scaling so the coefficients are comparable to the true model.
    raw_w = [w / s for w, s in zip(s_weights, stds)]
    raw_b = s_bias - sum(w * m for w, m in zip(raw_w, means))

    print("\nthree features, true model y = 4.0 + 1.5a - 2.0b + 0.75c + noise")
    print(f"  fitted intercept: {raw_b:.4f}")
    print("  fitted weights:   " + ", ".join(f"{w:.4f}" for w in raw_w))
    print(f"  R^2:              "
          f"{r_squared(multi_y, predict(multi, raw_w, raw_b)):.4f}")

    # --- edge cases ---------------------------------------------------------
    print("\nedge cases")
    print(f"  two points fit exactly: {fit_closed_form([0.0, 1.0], [1.0, 3.0])}")
    print(f"  vertical x (no slope):  {fit_closed_form([2.0, 2.0], [1.0, 5.0])}")
    flat = [5.0] * 4
    print(f"  constant y, R^2:        "
          f"{r_squared(flat, [5.0] * 4):.4f}")
    print(f"  mean-only model, R^2:   "
          f"{r_squared([1.0, 2.0, 3.0], [2.0, 2.0, 2.0]):.4f}")


if __name__ == "__main__":
    main()
