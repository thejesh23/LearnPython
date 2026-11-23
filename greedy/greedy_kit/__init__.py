"""greedy_kit: activity selection, meeting rooms, jump game, fractional knapsack, Huffman.

    >>> from greedy.greedy_kit import min_jumps, fractional_knapsack
    >>> min_jumps([2, 3, 1, 1, 4])
    2
    >>> fractional_knapsack([("a", 60, 10), ("b", 100, 20), ("c", 120, 30)], 50)[0]
    240.0
"""

from .priority import decode, encode, fractional_knapsack, huffman_codes
from .scheduling import assign_rooms, min_jumps, min_rooms, select_activities

__all__ = [
    "select_activities",
    "assign_rooms",
    "min_rooms",
    "min_jumps",
    "fractional_knapsack",
    "huffman_codes",
    "encode",
    "decode",
]
