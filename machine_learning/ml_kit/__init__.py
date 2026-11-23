"""ml_kit: five models with one ``fit(X, y)`` / ``predict(X)`` / ``score(X, y)`` interface.

    >>> from machine_learning.ml_kit import DecisionTree, KNNClassifier
    >>> X, y = [[1, 1], [1, 2], [8, 8], [9, 8]], ["low", "low", "high", "high"]
    >>> KNNClassifier(k=3).fit(X, y).predict([[2, 1], [7, 9]])
    ['low', 'high']
    >>> DecisionTree().fit(X, y).root
    (0, 4.5, ('low',), ('high',))
"""

from .classifiers import DecisionTree, GaussianNB, KNNClassifier, gini
from .data import (
    Model,
    accuracy,
    make_blobs,
    make_regression,
    r2_score,
    scale,
    standardise,
    train_test_split,
)
from .linear import LinearRegression, LogisticRegression

__all__ = [
    "Model",
    "LinearRegression",
    "LogisticRegression",
    "KNNClassifier",
    "GaussianNB",
    "DecisionTree",
    "gini",
    "make_blobs",
    "make_regression",
    "train_test_split",
    "standardise",
    "scale",
    "accuracy",
    "r2_score",
]
