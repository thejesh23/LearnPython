"""Huffman codes, the Burrows-Wheeler transform, and delta + varint integer packing."""

import heapq
from collections import Counter
from typing import NamedTuple


class HuffmanPayload(NamedTuple):
    """Everything a decoder needs: the code table, packed bytes, and how many bits are real."""

    codes: dict[str, str]
    data: bytes
    bit_count: int


def huffman_codes(text: str) -> dict[str, str]:
    """Prefix-free bit strings, shorter for more frequent chars (greedy merge of the two rarest)."""
    counts = Counter(text)
    if len(counts) <= 1:
        return {ch: "0" for ch in counts}  # a lone symbol still needs one bit
    # (weight, tiebreak, {char: code so far}); merging prepends 0 / 1 to each side.
    heap = [(n, i, {ch: ""}) for i, (ch, n) in enumerate(sorted(counts.items()))]
    heapq.heapify(heap)
    tick = len(heap)
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        merged = {c: "0" + code for c, code in left.items()} | {c: "1" + code for c, code in right.items()}
        heapq.heappush(heap, (w1 + w2, tick, merged))
        tick += 1
    return heap[0][2]


def huffman_encode(text: str) -> HuffmanPayload:
    """Encode with ``huffman_codes`` and pack the bits into bytes."""
    codes = huffman_codes(text)
    bits = "".join(codes[ch] for ch in text)
    padded = bits + "0" * (-len(bits) % 8)
    data = bytes(int(padded[i:i + 8], 2) for i in range(0, len(padded), 8))
    return HuffmanPayload(codes, data, len(bits))


def huffman_decode(payload: HuffmanPayload) -> str:
    """Read bits until they spell a code; prefix-freeness makes that unambiguous."""
    lookup = {code: ch for ch, code in payload.codes.items()}
    bits = "".join(f"{byte:08b}" for byte in payload.data)[:payload.bit_count]
    out, current = [], ""
    for bit in bits:
        current += bit
        if current in lookup:
            out.append(lookup[current])
            current = ""
    if current:
        raise ValueError("bit stream does not match the code table")
    return "".join(out)


SENTINEL = "\x00"


def bwt(text: str) -> str:
    """Last column of the sorted rotations of text + sentinel; like chars cluster into runs."""
    if SENTINEL in text:
        raise ValueError("input must not contain the sentinel \\x00")
    s = text + SENTINEL
    return "".join(rot[-1] for rot in sorted(s[i:] + s[:i] for i in range(len(s))))


def inverse_bwt(last: str) -> str:
    """Undo ``bwt`` with the LF mapping: the i-th 'x' in the last column is the i-th in the first."""
    if not last:
        return ""
    rank, seen = [], Counter()
    for ch in last:
        rank.append(seen[ch])
        seen[ch] += 1
    start, total = {}, 0
    for ch in sorted(seen):
        start[ch], total = total, total + seen[ch]
    row, out = 0, []  # row 0 is the rotation that starts with the sentinel
    for _ in range(len(last) - 1):
        out.append(last[row])
        row = start[last[row]] + rank[row]
    return "".join(reversed(out))


def pack_ints(values: list[int]) -> bytes:
    """Store gaps instead of values, zigzag the sign, then LEB128: 7 bits per byte."""
    out = bytearray()
    prev = 0
    for v in values:
        delta, prev = v - prev, v
        n = delta << 1 if delta >= 0 else (-delta << 1) - 1  # 0,-1,1,-2.. -> 0,1,2,3..
        while n >= 0x80:
            out.append(n & 0x7F | 0x80)  # high bit = more bytes follow
            n >>= 7
        out.append(n)
    return bytes(out)


def unpack_ints(data: bytes) -> list[int]:
    """Inverse of ``pack_ints``."""
    values: list[int] = []
    n = shift = 0
    for byte in data:
        n |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            delta = n >> 1 if n % 2 == 0 else -((n + 1) >> 1)
            values.append((values[-1] if values else 0) + delta)
            n = shift = 0
    if shift:
        raise ValueError("truncated varint")
    return values
