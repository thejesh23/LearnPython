"""convert_kit: units, Roman numerals, number words and bases behind one API.

    >>> from conversions.convert_kit import convert, to_roman, to_words
    >>> convert(100, "C", "F")
    212.0
    >>> to_roman(1994), to_words(1001)
    ('MCMXCIV', 'one thousand and one')
"""

from .numerals import from_base, from_roman, to_base, to_roman, to_words
from .units import UNITS, clock, convert, humanize_bytes, quantity_of

__all__ = [
    "convert",
    "quantity_of",
    "UNITS",
    "humanize_bytes",
    "clock",
    "to_roman",
    "from_roman",
    "to_words",
    "to_base",
    "from_base",
]
