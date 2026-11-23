"""bit_kit: single-bit operations, popcount, powers of two, xor tricks, bitmasks.

    >>> from bit_manipulation.bit_kit import popcount, single_number, to_signed
    >>> popcount(0b1011_0110)
    5
    >>> single_number([4, 1, 2, 1, 2])
    4
    >>> to_signed(0xFFFFFFFF)
    -1
"""

from .bits import (
    clear_bit,
    is_power_of_two,
    lowest_set_bit,
    next_power_of_two,
    popcount,
    set_bit,
    test_bit,
    to_signed,
    to_unsigned,
    toggle_bit,
)
from .tricks import missing_number, single_number, submasks, subsets, two_single_numbers

__all__ = [
    "set_bit",
    "clear_bit",
    "toggle_bit",
    "test_bit",
    "popcount",
    "lowest_set_bit",
    "is_power_of_two",
    "next_power_of_two",
    "to_unsigned",
    "to_signed",
    "single_number",
    "two_single_numbers",
    "missing_number",
    "subsets",
    "submasks",
]
