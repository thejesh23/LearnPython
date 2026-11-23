# compress_kit

Huffman, LZ77, LZW and the Burrows-Wheeler transform behind one `compress()` / `decompress()` pair, plus delta + varint packing for integer lists.

```bash
python3 -m compression.compress_kit     # eight examples plus a round-trip self-check
```

```python
from compression.compress_kit import compress, decompress

codes = compress("TOBEORNOTTOBEORTOBEORNOT", "lzw")    # [84, 79, 66, 69, ...]
decompress(codes, "lzw")                               # 'TOBEORNOTTOBEORTOBEORNOT'
```

| API | Module | Idea |
|---|---|---|
| `huffman_codes`, `huffman_encode`, `huffman_decode` | `coding.py` | short codes for common symbols, packed into bytes |
| `bwt`, `inverse_bwt` | `coding.py` | a reversible shuffle that groups like letters into runs |
| `pack_ints`, `unpack_ints` | `coding.py` | store gaps, zigzag the sign, 7 bits per varint byte |
| `lz77_compress`, `lz77_decompress` | `dictionary.py` | copy from a sliding window of earlier text |
| `lzw_encode`, `lzw_decode` | `dictionary.py` | a phrase table both sides build without sending it |
| `compress`, `decompress`, `CODECS` | `__init__.py` | pick any text codec by name |

Standalone versions live next to this folder, e.g. `../huffman_codec.py`.
