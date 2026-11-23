"""cipher_kit: Caesar, Vigenere and XOR ciphers, plus the attacks that break them.

Historical toys for learning; never use them to protect real data.

    >>> from ciphers.cipher_kit import caesar_encrypt, vigenere_encrypt, xor_bytes
    >>> caesar_encrypt("Attack at dawn!", 3)
    'Dwwdfn dw gdzq!'
    >>> vigenere_encrypt("attack at dawn", "lemon")
    'lxfopv ef rnhr'
    >>> xor_bytes(xor_bytes(b"hi", b"k"), b"k")
    b'hi'
"""

from .classical import (
    caesar_decrypt,
    caesar_encrypt,
    crack_caesar,
    crack_vigenere,
    english_score,
    guess_key_length,
    index_of_coincidence,
    vigenere_decrypt,
    vigenere_encrypt,
)
from .xor import crack_repeating_xor, crack_single_byte_xor, text_score, xor_bytes

__all__ = [
    "caesar_encrypt",
    "caesar_decrypt",
    "crack_caesar",
    "vigenere_encrypt",
    "vigenere_decrypt",
    "guess_key_length",
    "crack_vigenere",
    "english_score",
    "index_of_coincidence",
    "xor_bytes",
    "crack_single_byte_xor",
    "crack_repeating_xor",
    "text_score",
]
