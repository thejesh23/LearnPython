"""Single-bit surgery: set, clear, toggle, test, extract — and the xor swap.

The four one-bit operations all build on a single-bit mask 1 << i. Or with it to
set the bit, and with its complement to clear it, xor with it to toggle, and
shift the value down and mask with 1 to read it. Writing a computed value into a
bit is a clear followed by an or, which is worth doing in one helper so the two
halves cannot drift apart.

Extracting a range of bits is the same idea with a wider mask: shift the value
right by the range's low index, then and with (1 << length) - 1 to keep only the
bits wanted.

The xor swap exchanges two variables with no temporary: a ^= b, b ^= a, a ^= b.
It is a genuinely pretty identity, and you should not use it. It silently zeroes
the value when both names refer to the same storage, it is slower than a real
swap on any modern processor because of the serial dependency, and in Python the
tuple assignment a, b = b, a is both clearer and faster. Know it so you can read
it in old C, not so you can write it.

Every operation here is O(1) and works on Python's arbitrary-precision ints.
"""


def set_bit(n: int, i: int) -> int:
    return n | (1 << i)


def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    return n ^ (1 << i)


def test_bit(n: int, i: int) -> bool:
    return bool(n >> i & 1)


def write_bit(n: int, i: int, value: bool) -> int:
    """Clear then set, so a computed value lands correctly either way."""
    return (n & ~(1 << i)) | (int(value) << i)


def extract_bits(n: int, low: int, length: int) -> int:
    """The `length` bits starting at position `low`, as an integer."""
    if length < 0 or low < 0:
        raise ValueError("low and length must be non-negative")
    return n >> low & ((1 << length) - 1)


def write_bits(n: int, low: int, length: int, value: int) -> int:
    mask = ((1 << length) - 1) << low
    return (n & ~mask) | ((value << low) & mask)


def xor_swap(a: int, b: int) -> tuple[int, int]:
    """Faithful to the C idiom; see the docstring for why not to use it."""
    a ^= b
    b ^= a
    a ^= b
    return a, b


def xor_swap_in_place(values: list[int], i: int, j: int) -> None:
    """The dangerous form: when i == j the element is destroyed."""
    values[i] ^= values[j]
    values[j] ^= values[i]
    values[i] ^= values[j]


def bits(n: int, width: int = 8) -> str:
    return format(n & ((1 << width) - 1), f"0{width}b")


def main() -> None:
    n = 0b1010_0110
    print(f"n              = {bits(n)}")
    print(f"set_bit(n, 0)  = {bits(set_bit(n, 0))}")
    print(f"clear_bit(n,1) = {bits(clear_bit(n, 1))}")
    print(f"toggle_bit(n,7)= {bits(toggle_bit(n, 7))}")
    print(f"test_bit(n, 5) = {test_bit(n, 5)}, test_bit(n, 4) = {test_bit(n, 4)}")
    print(f"write_bit(n,2,False) = {bits(write_bit(n, 2, False))}")
    print(f"write_bit(n,3,True)  = {bits(write_bit(n, 3, True))}")

    # Setting an already-set bit and clearing an already-clear one are no-ops.
    print(f"\nset an already-set bit:   {bits(set_bit(n, 1))} unchanged="
          f"{set_bit(n, 1) == n}")
    print(f"clear an already-clear:   {bits(clear_bit(n, 0))} unchanged="
          f"{clear_bit(n, 0) == n}")
    print(f"toggle twice restores:    {toggle_bit(toggle_bit(n, 4), 4) == n}")

    print(f"\nextract_bits(n, 4, 4) = {bits(extract_bits(n, 4, 4), 4)} "
          f"(= {extract_bits(n, 4, 4)})")
    print(f"extract_bits(n, 1, 3) = {bits(extract_bits(n, 1, 3), 3)} "
          f"(= {extract_bits(n, 1, 3)})")
    print(f"extract_bits(n, 0, 0) = {extract_bits(n, 0, 0)}")
    print(f"write_bits(n, 4, 4, 0b1111) = {bits(write_bits(n, 4, 4, 0b1111))}")
    print(f"write_bits(n, 0, 4, 0b0000) = {bits(write_bits(n, 0, 4, 0))}")

    print(f"\nxor_swap(3, 9) = {xor_swap(3, 9)}")
    print(f"tuple swap is the same: {(9, 3)}")

    values = [11, 22, 33]
    xor_swap_in_place(values, 0, 2)
    print(f"xor swap of distinct indices: {values}")
    xor_swap_in_place(values, 1, 1)  # aliased: the value is xored with itself
    print(f"xor swap with i == j destroyed the element: {values}")

    # Bits beyond a value's length behave as zeros, and there is no top bit.
    print(f"\ntest_bit(1, 500) = {test_bit(1, 500)}")
    print(f"set_bit(0, 500).bit_length() = {set_bit(0, 500).bit_length()}")
    print(f"clear_bit(-1, 3) = {clear_bit(-1, 3)} (negatives have endless ones)")


if __name__ == "__main__":
    main()
