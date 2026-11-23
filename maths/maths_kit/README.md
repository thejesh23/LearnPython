# maths_kit

Exact integer maths on Python's big ints: gcd/lcm, modular powers, integer roots, combinations, base conversion and primes.

```bash
python3 -m maths.maths_kit     # seven examples plus a randomized self-check
```

```python
from maths.maths_kit import gcd, power_mod, prime_factors, to_base

gcd(84, 36, 120)                     # 12
power_mod(2, 100, 1_000_000_007)     # 976371285
prime_factors(360)                   # {2: 3, 3: 2, 5: 1}
to_base(255, 16)                     # 'ff'
```

| Function | Module | Teaches |
|---|---|---|
| `gcd`, `lcm` | `arithmetic.py` | Euclid's algorithm, divide before multiplying |
| `power_mod` | `arithmetic.py` | square-and-multiply over the exponent's bits |
| `isqrt` | `arithmetic.py` | Newton's method on integers (where floats fail) |
| `comb` | `arithmetic.py` | n choose r without huge factorials |
| `to_base`, `from_base` | `arithmetic.py` | repeated division and Horner's method |
| `is_prime`, `primes_below`, `prime_factors` | `primes.py` | 6k +/- 1 trial division, the sieve, factorisation |

The self-check compares each function with `math`/`pow`/`int` on random inputs.
Standalone versions live next to this folder, e.g. `../sieve_of_eratosthenes.py`.
