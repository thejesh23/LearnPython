"""Examples and self-check: python3 -m bit_manipulation.bit_kit"""

import itertools
import random
import sys

from . import (
    clear_bit,
    is_power_of_two,
    lowest_set_bit,
    missing_number,
    next_power_of_two,
    popcount,
    set_bit,
    single_number,
    submasks,
    subsets,
    test_bit,
    to_signed,
    to_unsigned,
    toggle_bit,
    two_single_numbers,
)


def examples() -> None:
    n = 0b1010
    print(f"1. n={n:04b}: set bit 0 -> {set_bit(n, 0):04b}, clear bit 1 -> {clear_bit(n, 1):04b},"
          f" toggle bit 3 -> {toggle_bit(n, 3):04b}, bit 3 set? {test_bit(n, 3)}")
    print("2. popcount(255) =", popcount(255), "| lowest set bit of 0b10100 =", bin(lowest_set_bit(0b10100)))
    print("3. powers of two up to 20:", [k for k in range(21) if is_power_of_two(k)],
          "| next for 17:", next_power_of_two(17))
    print("4. -1 as 8 bits:", bin(to_unsigned(-1, 8)),
          "| 0b10000000 as signed 8 bits:", to_signed(0b1000_0000, 8))
    print("5. single:", single_number([4, 1, 2, 1, 2]),
          "| two singles:", two_single_numbers([1, 2, 1, 3, 2, 5]),
          "| missing from 0..5:", missing_number([3, 0, 1, 5, 2]))
    print("6. subsets of abc:", subsets("abc"))
    print("7. submasks of 0b1011:", [f"{m:04b}" for m in submasks(0b1011)])


def self_check() -> None:
    rng = random.Random(9)
    for _ in range(500):
        n, i, w = rng.randint(0, 1 << 40), rng.randint(0, 45), rng.choice((8, 16, 32, 64))
        digits = format(n, "b")[::-1].ljust(64, "0")  # digits[i] is bit i, as text
        assert popcount(n) == digits.count("1") == n.bit_count()
        assert test_bit(n, i) == (digits[i] == "1")
        assert test_bit(set_bit(n, i), i) and not test_bit(clear_bit(n, i), i)
        assert toggle_bit(toggle_bit(n, i), i) == n != toggle_bit(n, i)
        assert lowest_set_bit(n) == (1 << digits.index("1") if n else 0)
        assert is_power_of_two(n) == (n in {1 << k for k in range(41)})
        m = rng.randint(-1000, 1 << 20)
        assert next_power_of_two(m) == next(p for p in (1 << k for k in range(22)) if p >= m)
        s = rng.randint(-(1 << (w - 1)), (1 << (w - 1)) - 1)
        assert to_signed(to_unsigned(s, w), w) == s and 0 <= to_unsigned(s, w) < 1 << w
        assert to_unsigned(s, w) == int.from_bytes(s.to_bytes(w // 8, "big", signed=True), "big")
    for _ in range(200):
        pool = rng.sample(range(-50, 50), 8)
        nums = pool[2:] * 2 + pool[:2]
        rng.shuffle(nums)
        assert single_number(pool[1:] * 2 + pool[:1]) == pool[0]
        assert two_single_numbers(nums) == tuple(sorted(pool[:2]))
        full = list(range(rng.randint(1, 20)))
        gone = full.pop(rng.randrange(len(full)))
        rng.shuffle(full)
        assert missing_number(full) == gone
    items = list("abcde")
    expected = [list(c) for r in range(6) for c in itertools.combinations(items, r)]
    assert sorted(subsets(items)) == sorted(expected) and len(subsets(items)) == 32
    for mask in (0, 1, 0b1011, 0b110110):
        assert submasks(mask) == [s for s in range(mask, -1, -1) if s & mask == s]
    try:
        popcount(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative popcount accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
