"""compress_kit: Huffman, LZ77, LZW, Burrows-Wheeler and delta + varint packing.

    >>> from compression.compress_kit import compress, decompress, pack_ints
    >>> compress("TOBEORNOTTOBEORTOBEORNOT", "lzw")[:10]
    [84, 79, 66, 69, 79, 82, 78, 79, 84, 256]
    >>> decompress(compress("abracadabra", "huffman"), "huffman")
    'abracadabra'
    >>> len(pack_ints([1_000_000, 1_000_003, 1_000_011]))
    5
"""

from collections.abc import Callable
from typing import Any

from .coding import (
    HuffmanPayload,
    bwt,
    huffman_codes,
    huffman_decode,
    huffman_encode,
    inverse_bwt,
    pack_ints,
    unpack_ints,
)
from .dictionary import Token, lz77_compress, lz77_decompress, lzw_decode, lzw_encode

# name -> (encode text into a payload, decode that payload back into text)
CODECS: dict[str, tuple[Callable[[str], Any], Callable[[Any], str]]] = {
    "huffman": (huffman_encode, huffman_decode),
    "lz77": (lz77_compress, lz77_decompress),
    "lzw": (lzw_encode, lzw_decode),
    "bwt": (bwt, inverse_bwt),
}

__all__ = [
    "CODECS",
    "compress",
    "decompress",
    "huffman_codes",
    "huffman_encode",
    "huffman_decode",
    "HuffmanPayload",
    "lz77_compress",
    "lz77_decompress",
    "Token",
    "lzw_encode",
    "lzw_decode",
    "bwt",
    "inverse_bwt",
    "pack_ints",
    "unpack_ints",
]


def _codec(method: str) -> tuple[Callable[[str], Any], Callable[[Any], str]]:
    try:
        return CODECS[method]
    except KeyError:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(CODECS)}") from None


def compress(text: str, method: str = "huffman") -> Any:
    """Encode ``text`` with the named codec; the payload type depends on the codec."""
    return _codec(method)[0](text)


def decompress(payload: Any, method: str = "huffman") -> str:
    """Decode a payload produced by ``compress`` with the same method."""
    return _codec(method)[1](payload)
