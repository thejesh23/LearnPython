# cipher_kit

Caesar, Vigenere and repeating-key XOR, each paired with the attack that breaks it.

```bash
python3 -m ciphers.cipher_kit     # eight examples plus a self-check
```

| Function | Module | What it does |
|---|---|---|
| `caesar_encrypt`, `caesar_decrypt`, `crack_caesar` | `classical.py` | shift letters; brute-force all 26 keys by English letter frequency |
| `vigenere_encrypt`, `vigenere_decrypt` | `classical.py` | a Caesar shift that changes with each key letter |
| `guess_key_length`, `crack_vigenere` | `classical.py` | index of coincidence finds the key length, then each slice is a Caesar crack |
| `xor_bytes`, `crack_single_byte_xor`, `crack_repeating_xor` | `xor.py` | self-inverse XOR; a short key splits into 256-way brute forces |

These are historical toys. Never use them to protect real data.

Standalone versions live next to this folder, e.g. `../vigenere_cipher.py`.
