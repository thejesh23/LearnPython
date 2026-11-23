"""backtrack_kit: N queens, subset sum, pruned permutations, word search, sudoku.

    >>> from backtracking.backtrack_kit import n_queens, subset_sums
    >>> len(n_queens(8))
    92
    >>> subset_sums([3, 34, 4, 12, 5, 2], 9)
    [[2, 3, 4], [4, 5]]
"""

from .search import n_queens, permutations_where, subset_sums, word_path
from .sudoku import is_solved, solve_sudoku

__all__ = ["n_queens", "subset_sums", "permutations_where", "word_path", "solve_sudoku", "is_solved"]
