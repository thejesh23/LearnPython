"""string_kit: one ``find_all()`` over five search algorithms, plus string utilities.

    >>> from strings.string_kit import find_all, longest_palindrome
    >>> find_all("abababa", "aba", algo="z")
    [0, 2, 4]
    >>> longest_palindrome("forgeeksskeegfor")
    'geeksskeeg'
"""

from collections.abc import Callable

from . import search
from .search import build_lps, suffix_array, z_array
from .text import (
    find_many,
    glob_match,
    longest_palindrome,
    longest_repeated_substring,
    longest_unique_substring,
    rle_decode,
    rle_encode,
)

ALGORITHMS: dict[str, Callable[[str, str], list[int]]] = {
    "naive": search.naive_search,
    "kmp": search.kmp_search,
    "z": search.z_search,
    "rabin_karp": search.rabin_karp,
    "suffix_array": search.suffix_array_search,
    "builtin": search.builtin_search,
}

__all__ = [
    "ALGORITHMS", "find_all", "find_many", "build_lps", "z_array", "suffix_array",
    "longest_palindrome", "longest_repeated_substring", "longest_unique_substring",
    "rle_encode", "rle_decode", "glob_match",
]


def find_all(text: str, pattern: str, algo: str = "kmp") -> list[int]:
    """Every start index of ``pattern`` in ``text`` (overlaps included), ascending.

    An empty pattern matches at every position 0..len(text), like str.find.
    """
    if algo not in ALGORITHMS:
        raise ValueError(f"unknown algorithm {algo!r}; choose from {sorted(ALGORITHMS)}")
    if not pattern:
        return list(range(len(text) + 1))
    return ALGORITHMS[algo](text, pattern)
