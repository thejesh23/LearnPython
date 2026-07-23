"""Principal component analysis: find the directions of greatest variance.

PCA re-expresses data in a new orthogonal basis ordered by how much variance
each axis captures. Those axes are the eigenvectors of the covariance matrix,
and their eigenvalues are the variances along them. Centering the data first is
essential: PCA is about spread around the mean, not distance from the origin.
Projecting onto the top few components gives the best low-rank approximation of
the data in a least-squares sense, which is why PCA is the standard linear tool
for dimensionality reduction and visualisation.

Rather than a full eigensolver this uses power iteration with deflation: find
the top eigenvector of the covariance matrix, subtract its contribution, and
repeat for the next. Each component costs O(iters * d^2) plus O(n * d) to build
the covariance. The eigenvalues sum to the total variance, so dividing each by
that sum gives the fraction of variance a component explains, reported below.
"""

Matrix = list[list[float]]
Vector = list[float]


def column_means(data: Matrix) -> Vector:
    n = len(data)
    d = len(data[0])
    return [sum(row[j] for row in data) / n for j in range(d)]


def center(data: Matrix) -> tuple[Matrix, Vector]:
    mu = column_means(data)
    return [[row[j] - mu[j] for j in range(len(mu))] for row in data], mu


def covariance(centered: Matrix) -> Matrix:
    n = len(centered)
    d = len(centered[0])
    # Sample covariance with the (n-1) divisor.
    return [[sum(centered[k][i] * centered[k][j] for k in range(n)) / (n - 1)
             for j in range(d)] for i in range(d)]


def mat_vec(A: Matrix, v: Vector) -> Vector:
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def top_eigenpair(A: Matrix, iterations: int = 2000,
                  tol: float = 1e-12) -> tuple[float, Vector]:
    d = len(A)
    v = [1.0 / (i + 1) ** 0.5 for i in range(d)]
    norm = sum(x * x for x in v) ** 0.5
    v = [x / norm for x in v]
    lam = 0.0
    for _ in range(iterations):
        w = mat_vec(A, v)
        norm = sum(x * x for x in w) ** 0.5
        v_new = [x / norm for x in w]
        lam_new = sum(v_new[i] * mat_vec(A, v_new)[i] for i in range(d))
        if abs(lam_new - lam) < tol:
            return lam_new, v_new
        v, lam = v_new, lam_new
    return lam, v


def pca(data: Matrix, k: int) -> tuple[list[Vector], list[float], Vector]:
    """Return the top-k components, their eigenvalues, and the data mean."""
    centered, mu = center(data)
    cov = covariance(centered)
    d = len(cov)
    components: list[Vector] = []
    eigvals: list[float] = []
    work = [row[:] for row in cov]
    for _ in range(k):
        lam, vec = top_eigenpair(work)
        components.append(vec)
        eigvals.append(lam)
        # Deflate: remove this eigendirection so the next iteration finds
        # the following one.
        work = [[work[i][j] - lam * vec[i] * vec[j] for j in range(d)]
                for i in range(d)]
    return components, eigvals, mu


def project(data: Matrix, components: list[Vector], mu: Vector) -> Matrix:
    out: Matrix = []
    for row in data:
        centered = [row[j] - mu[j] for j in range(len(mu))]
        out.append([sum(centered[j] * comp[j] for j in range(len(comp)))
                    for comp in components])
    return out


def main() -> None:
    import random

    rng = random.Random(3)

    # Data that mostly lives along the line y = 2x, with a little spread off it.
    data: Matrix = []
    for _ in range(200):
        t = rng.uniform(-3, 3)
        off = rng.gauss(0, 0.3)
        data.append([t + off, 2 * t - off])

    comps, eigvals, mu = pca(data, k=2)
    total = sum(eigvals)
    print(f"data mean: {[round(v, 4) for v in mu]}")
    print("principal components (eigenvalue, direction, explained variance)")
    for lam, comp in zip(eigvals, comps):
        print(f"  lambda={lam:>8.4f}  dir={[round(v, 4) for v in comp]}  "
              f"explains {lam / total * 100:>6.2f}%")

    # The first component should align with (1, 2) normalised.
    import math
    expected = [1 / math.sqrt(5), 2 / math.sqrt(5)]
    align = abs(sum(comps[0][j] * expected[j] for j in range(2)))
    print(f"\n|component1 . (1,2)/sqrt5| = {align:.4f}  (expect ~1)")

    # Components are orthonormal.
    print(f"unit length of component1: "
          f"{sum(c * c for c in comps[0]) ** 0.5:.6f}")
    print(f"component1 . component2:   "
          f"{sum(comps[0][j] * comps[1][j] for j in range(2)):.2e}")

    # Reduce to 1D: keep only the dominant component, most variance survives.
    reduced = project(data, comps[:1], mu)
    var_1d = sum(r[0] ** 2 for r in reduced) / (len(reduced) - 1)
    print(f"\nvariance kept by first component alone: {var_1d:.4f} "
          f"of {total:.4f} total ({var_1d / total * 100:.2f}%)")
    print(f"first 3 projected coordinates (1D): "
          f"{[round(r[0], 3) for r in reduced[:3]]}")


if __name__ == "__main__":
    main()
