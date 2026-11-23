# nt_kit

Primality, factoring and modular arithmetic: the number theory that RSA, Diffie-Hellman and hashing tricks rest on.

```bash
python3 -m number_theory.nt_kit     # seven examples plus a self-check against brute force
```

```python
from number_theory.nt_kit import crt, factorize, sqrt_mod

factorize(600851475143)        # [71, 839, 1471, 6857]
crt([2, 3, 2], [3, 5, 7])      # (23, 105)
sqrt_mod(10, 13)               # 7  (7 * 7 = 49 = 10 mod 13)
```

| Function | Module | Method |
|---|---|---|
| `extended_gcd`, `mod_inverse` | `modular.py` | extended Euclid |
| `crt` | `modular.py` | merge congruences pairwise; moduli may share factors |
| `legendre`, `sqrt_mod` | `modular.py` | Euler's criterion, Tonelli-Shanks |
| `discrete_log` | `modular.py` | baby-step giant-step |
| `is_prime`, `next_prime` | `primes.py` | deterministic Miller-Rabin |
| `pollard_rho`, `factorize`, `divisors`, `totient` | `primes.py` | Pollard's rho, then build on the factorisation |

Standalone versions live next to this folder, e.g. `../pollard_rho.py`.
