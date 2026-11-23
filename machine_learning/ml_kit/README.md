# ml_kit

Five classic models behind one `fit(X, y)` / `predict(X)` / `score(X, y)` interface, with tiny seeded datasets to try them on.

```bash
python3 -m machine_learning.ml_kit     # seven examples plus a self-check
```

```python
from machine_learning.ml_kit import KNNClassifier, make_blobs, train_test_split

X, y = make_blobs([[2, 2], [6, 6]], n_per_center=50, seed=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, seed=1)
KNNClassifier(k=5).fit(X_train, y_train).score(X_test, y_test)    # accuracy, e.g. 1.0
```

| API | Module | Teaches |
|---|---|---|
| `make_blobs`, `make_regression`, `train_test_split` | `data.py` | reproducible toy data and a held-out test set |
| `standardise`, `scale`, `accuracy`, `r2_score`, `Model` | `data.py` | feature scaling, metrics, the shared interface |
| `LinearRegression`, `LogisticRegression` | `linear.py` | gradient descent on squared error and log loss (one-vs-rest) |
| `KNNClassifier`, `GaussianNB`, `DecisionTree` | `classifiers.py` | nearest neighbours, Bayes' rule, gini-greedy CART |

The self-check checks k-NN and naive Bayes against brute-force versions and linear regression against `statistics.linear_regression`.
Standalone versions live next to this folder, e.g. `../knn_classifier.py`.
