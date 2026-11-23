# bit_kit

Bit manipulation in Python, where ints have no fixed width: single-bit operations, counting, powers of two, two's complement views, xor puzzles and bitmask subsets.

```bash
python3 -m bit_manipulation.bit_kit     # seven examples plus a randomized self-check
```

| Function | Module | Trick |
|---|---|---|
| `set_bit`, `clear_bit`, `toggle_bit`, `test_bit` | `bits.py` | or / and-not / xor / shift with `1 << i` |
| `popcount`, `lowest_set_bit` | `bits.py` | `n & (n - 1)` and `n & -n` |
| `is_power_of_two`, `next_power_of_two` | `bits.py` | one set bit; `bit_length` |
| `to_unsigned`, `to_signed` | `bits.py` | mask to a width, then sign-extend |
| `single_number`, `two_single_numbers`, `missing_number` | `tricks.py` | pairs cancel under xor |
| `subsets`, `submasks` | `tricks.py` | a bitmask is a subset; `(sub - 1) & mask` |

Standalone versions live next to this folder, e.g. `../count_set_bits.py`.
