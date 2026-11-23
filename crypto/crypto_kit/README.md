# crypto_kit

SHA-256 and HMAC from scratch, Merkle membership proofs, textbook RSA, Diffie-Hellman and Shamir secret sharing.

> **Toy / educational only, not for real security.** No padding, no constant-time code, tiny keys.
> Use `hashlib`, `hmac`, `secrets` and a reviewed library such as `cryptography` for anything real.

```bash
python3 -m crypto.crypto_kit     # eight examples plus a self-check against hashlib and hmac
```

| API | Module | What it shows |
|---|---|---|
| `sha256`, `hmac_sha256` | `hashing.py` | Merkle-Damgard hashing; why HMAC nests two hashes |
| `MerkleTree`, `verify_proof` | `hashing.py` | one root commits to every item; O(log n) proofs |
| `is_probable_prime`, `generate_prime` | `keys.py` | Miller-Rabin and random prime generation |
| `rsa_keypair`, `rsa_encrypt`, `rsa_decrypt`, `rsa_sign`, `rsa_verify` | `keys.py` | textbook RSA (deterministic and malleable) |
| `dh_keypair`, `dh_shared_secret` | `keys.py` | agreeing on a secret over an open channel |
| `split_secret`, `reconstruct_secret` | `keys.py` | any k of n shares rebuild the secret |

Functions that need randomness take an optional `rng` (a `random.Random`) so demos repeat; the default is `secrets.SystemRandom()`.

Standalone versions live next to this folder, e.g. `../sha256_from_scratch.py`.
