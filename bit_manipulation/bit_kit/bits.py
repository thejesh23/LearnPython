"""Single-bit operations, counting, powers of two and fixed-width views.

Python ints have no fixed width: ``~5`` is ``-6`` and ``-1 >> 1`` is still
``-1``. To mimic a 32-bit register, mask with ``(1 << width) - 1`` and convert
back with ``to_signed``.
"""


def set_bit(n: int, i: int) -> int:
    """n with bit i turned on (or with the mask 1 << i)."""
    return n | 1 << i


def clear_bit(n: int, i: int) -> int:
    """n with bit i turned off (and with the inverted mask)."""
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    """n with bit i flipped (xor with the mask)."""
    return n ^ 1 << i


def test_bit(n: int, i: int) -> bool:
    """True if bit i of n is set."""
    return n >> i & 1 == 1


def popcount(n: int) -> int:
    """Number of set bits, by Kernighan's trick: ``n & (n - 1)`` drops the lowest one.

    Loops once per set bit, not once per bit. Negatives have infinitely many
    set bits in Python, so convert them with ``to_unsigned`` first.
    """
    if n < 0:
        raise ValueError("popcount of a negative int is infinite; use to_unsigned first")
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def lowest_set_bit(n: int) -> int:
    """The value of n's lowest set bit (``n & -n``), or 0 for 0."""
    return n & -n


def is_power_of_two(n: int) -> bool:
    """True for 1, 2, 4, 8, ...: exactly one bit set, so n & (n - 1) is zero."""
    return n > 0 and n & (n - 1) == 0


def next_power_of_two(n: int) -> int:
    """Smallest power of two >= n (1 for n <= 1), read off ``bit_length``."""
    return 1 if n <= 1 else 1 << (n - 1).bit_length()


def to_unsigned(n: int, width: int = 32) -> int:
    """Reinterpret n as a ``width``-bit two's complement pattern (0 .. 2**width - 1)."""
    return n & ((1 << width) - 1)


def to_signed(n: int, width: int = 32) -> int:
    """Inverse of ``to_unsigned``: sign-extend a ``width``-bit pattern."""
    n = to_unsigned(n, width)
    return n - (1 << width) if n >> (width - 1) & 1 else n
