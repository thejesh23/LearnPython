"""k-nearest neighbours: classify by asking whoever is closest.

There is no training. The model is the dataset. To classify a new point you
measure its euclidean distance to every stored example, take the k smallest, and
let them vote on the label. That makes fitting O(1) and prediction O(n * d), the
opposite trade-off from most learners.

Two details decide whether it behaves well. The first is k. A small k follows the
data closely and copies its noise; a large k smooths the boundary until it starts
ignoring genuine structure. Odd k avoids the commonest ties in binary problems.
The second is scale: distance treats all features alike, so a column measured in
thousands will drown one measured in fractions unless you standardise first.

Ties still happen with more than two classes, so we break them deterministically
by the nearest member of each tied class, then by label. That keeps the output
reproducible instead of depending on dictionary insertion order.
"""

import math
import random
from collections import Counter


Point = list[float]


def euclidean(a: Point, b: Point) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def neighbours(train: list[tuple[Point, str]], query: Point,
               k: int) -> list[tuple[float, str]]:
    """The k closest (distance, label) pairs, nearest first."""
    scored = sorted((euclidean(p, query), label) for p, label in train)
    return scored[:k]


def vote(near: list[tuple[float, str]]) -> tuple[str, dict[str, int]]:
    """Majority label; ties go to the class whose nearest member is closest."""
    counts = Counter(label for _, label in near)
    best = max(counts.values())
    tied = sorted(label for label, c in counts.items() if c == best)
    if len(tied) == 1:
        return tied[0], dict(counts)
    closest = {label: min(d for d, m in near if m == label) for label in tied}
    winner = min(tied, key=lambda label: (closest[label], label))
    return winner, dict(counts)


def classify(train: list[tuple[Point, str]], query: Point, k: int) -> str:
    if k <= 0:
        raise ValueError("k must be positive")
    return vote(neighbours(train, query, min(k, len(train))))[0]


def standardise(points: list[Point]) -> tuple[list[Point], list[float],
                                              list[float]]:
    """Centre and scale each column so no feature dominates by units alone."""
    n, d = len(points), len(points[0])
    mu = [sum(p[j] for p in points) / n for j in range(d)]
    sigma = []
    for j in range(d):
        var = sum((p[j] - mu[j]) ** 2 for p in points) / n
        sigma.append(math.sqrt(var) or 1.0)  # a constant column scales by 1
    return ([[(p[j] - mu[j]) / sigma[j] for j in range(d)] for p in points],
            mu, sigma)


def accuracy(train: list[tuple[Point, str]], test: list[tuple[Point, str]],
             k: int) -> float:
    hits = sum(1 for p, label in test if classify(train, p, k) == label)
    return hits / len(test)


def main() -> None:
    rng = random.Random(5)

    train: list[tuple[Point, str]] = []
    for _ in range(60):
        train.append(([rng.gauss(2, 1.0), rng.gauss(2, 1.0)], "red"))
    for _ in range(60):
        train.append(([rng.gauss(6, 1.0), rng.gauss(6, 1.0)], "blue"))
    for _ in range(60):
        train.append(([rng.gauss(2, 1.0), rng.gauss(6, 1.0)], "green"))

    test: list[tuple[Point, str]] = []
    for centre, label in (((2, 2), "red"), ((6, 6), "blue"), ((2, 6), "green")):
        for _ in range(20):
            test.append(([rng.gauss(centre[0], 1.0), rng.gauss(centre[1], 1.0)],
                         label))

    print("three classes, 180 training points, 60 test points")
    for k in (1, 3, 5, 11, 25, 51):
        print(f"  k = {k:>2}: test accuracy {accuracy(train, test, k) * 100:>6.2f}%")

    # A point near the boundary flips label as k widens the neighbourhood.
    print("\none query, varying k")
    query = [3.6, 4.2]
    for k in (1, 3, 5, 9, 21, 45):
        near = neighbours(train, query, k)
        label, counts = vote(near)
        tally = ", ".join(f"{c}:{n}" for c, n in sorted(counts.items()))
        print(f"  k = {k:>2} -> {label:<5} ({tally})")

    print("\nnearest five neighbours of that query")
    for d, label in neighbours(train, query, 5):
        print(f"  {label:<5} at distance {d:.4f}")

    print("\nedge cases")
    print(f"  k = 1 on a training point reproduces its own label: "
          f"{classify(train, train[0][0], 1) == train[0][1]}")
    print(f"  k larger than the dataset is clamped: "
          f"{classify(train, query, 10_000)}")
    tie_set: list[tuple[Point, str]] = [([0.0, 0.0], "a"), ([2.0, 0.0], "b")]
    print(f"  exact 1-1 tie, 'b' is nearer: "
          f"{classify(tie_set, [1.5, 0.0], 2)}")
    print(f"  exact 1-1 tie, 'a' is nearer: "
          f"{classify(tie_set, [0.5, 0.0], 2)}")
    try:
        classify(train, query, 0)
    except ValueError as exc:
        print(f"  k = 0: ValueError({exc})")

    # Column 0 separates the classes; column 1 is wide-ranging noise. Raw
    # distances are decided almost entirely by column 1 and give the wrong
    # answer, which standardising the columns repairs.
    skewed = [([0.0, 5000.0], "a"), ([0.2, 5300.0], "a"),
              ([10.0, 5100.0], "b"), ([10.2, 5400.0], "b")]
    query2 = [0.1, 5390.0]
    print(f"\n  raw features, query {query2} -> "
          f"{classify(skewed, query2, 1)} (wrong; the noisy column dominates)")
    scaled, mu, sigma = standardise([p for p, _ in skewed])
    scaled_train = [(p, label) for p, (_, label) in zip(scaled, skewed)]
    scaled_q = [(v - m) / s for v, m, s in zip(query2, mu, sigma)]
    print(f"  standardised features       -> "
          f"{classify(scaled_train, scaled_q, 1)} (right)")


if __name__ == "__main__":
    main()
