"""Counting set bits (population count), three ways.

The direct method shifts the number right one place at a time and adds the low
bit, costing one iteration per bit position — that is O(bit_length), so 64
iterations for a 64-bit value even if only one bit is set.

Brian Kernighan's trick does better. Subtracting one from n flips the lowest set
bit to zero and turns every zero below it into a one; anding that with n
therefore clears exactly the lowest set bit and leaves everything above it
alone. Looping until n is zero costs one iteration per set bit, so a sparse
number is counted almost instantly. The same identity is the basis for the
power-of-two test and for iterating over the members of a bitmask.

Since Python 3.10 there is int.bit_count(), which is both correct and fast
because it is implemented in C. Use it in real code; the loops above are worth
knowing because the reasoning behind them shows up all over bit manipulation.

All three require a non-negative input: a negative Python int has infinitely
many leading sign bits, so its population count is not finite.
"""


def count_naive(n: int) -> int:
    if n < 0:
        raise ValueError("population count needs a non-negative int")
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def count_kernighan(n: int) -> int:
    if n < 0:
        raise ValueError("population count needs a non-negative int")
    count = 0
    while n:
        n &= n - 1  # clears exactly the lowest set bit
        count += 1
    return count


def count_builtin(n: int) -> int:
    return n.bit_count()


def count_negative_in_width(n: int, width: int = 32) -> int:
    """For negatives, first commit to a width and take the two's complement."""
    return (n & ((1 << width) - 1)).bit_count()


def set_bit_positions(n: int) -> list[int]:
    """Kernighan's trick again: n & -n isolates the lowest set bit."""
    out: list[int] = []
    while n:
        low = n & -n
        out.append(low.bit_length() - 1)
        n ^= low
    return out


def main() -> None:
    for n in [0, 1, 2, 7, 8, 255, 256, 1023, 12345]:
        print(f"{n:>6} = {bin(n):>16}  naive={count_naive(n)} "
              f"kernighan={count_kernighan(n)} builtin={count_builtin(n)}")

    agree = all(
        count_naive(n) == count_kernighan(n) == count_builtin(n)
        for n in range(0, 5000)
    )
    print(f"\nall three agree for 0..4999: {agree}")

    # The iteration counts differ sharply on a sparse number.
    sparse = 1 << 63
    print(f"1 << 63: naive loops {sparse.bit_length()} times, "
          f"Kernighan loops {count_kernighan(sparse)} time")
    dense = (1 << 64) - 1
    print(f"64 ones: bit_count={count_builtin(dense)}")

    print(f"\npositions of set bits in 0b101101: {set_bit_positions(0b101101)}")
    print(f"positions in 0: {set_bit_positions(0)}")

    try:
        count_kernighan(-8)
    except ValueError as exc:
        print(f"\ncount_kernighan(-8): {exc}")
    print(f"-8 as 8-bit two's complement has "
          f"{count_negative_in_width(-8, 8)} set bits")
    print(f"-1 as 32-bit two's complement has "
          f"{count_negative_in_width(-1, 32)} set bits")

    # Arbitrary precision means huge inputs are fine.
    big = (1 << 500) | (1 << 250) | 3
    print(f"a 501-bit number: bit_count={big.bit_count()}, "
          f"kernighan={count_kernighan(big)}")


if __name__ == "__main__":
    main()
