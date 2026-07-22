"""A complete Huffman codec: code table, bit packing, and a serialised codebook.

greedy/huffman_encoding.py explains *why* the greedy merge builds an optimal
tree. This file assumes that and deals with the parts a real file format needs:
turning the tree into a symbol-to-bits table, packing those bits into whole
bytes, and shipping the codebook so a decoder that has never seen the input can
rebuild the tree.

Bit packing needs a length. A stream of codes rarely ends on a byte boundary,
so the container stores the number of valid bits; without it the padding zeros
would decode as extra symbols. The codebook here is stored as (symbol, code)
pairs, which is simple to read; real formats send only the code *lengths* and
derive canonical codes from them, which is much smaller.

Decoding walks the tree one bit at a time, emitting a symbol at every leaf.
"""

import heapq
from collections import Counter
from dataclasses import dataclass, field


@dataclass(order=True)
class Node:
    freq: int
    order: int
    symbol: str | None = field(default=None, compare=False)
    left: "Node | None" = field(default=None, compare=False)
    right: "Node | None" = field(default=None, compare=False)


def build_codes(text: str) -> dict[str, str]:
    counts = Counter(text)
    if not counts:
        return {}
    if len(counts) == 1:  # a lone symbol has no branch, so give it one bit
        return {next(iter(counts)): "0"}

    tick = iter(range(1 << 30))
    heap = [Node(f, next(tick), s) for s, f in sorted(counts.items())]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, Node(a.freq + b.freq, next(tick), None, a, b))

    codes: dict[str, str] = {}

    def walk(node: Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix
            return
        assert node.left and node.right
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(heap[0], "")
    return codes


def tree_from_codes(codes: dict[str, str]) -> Node:
    """Rebuild a decode tree from the codebook alone; frequencies are irrelevant."""
    root = Node(0, 0)
    for symbol, code in codes.items():
        node = root
        for bit in code:
            if bit == "0":
                node.left = node.left or Node(0, 0)
                node = node.left
            else:
                node.right = node.right or Node(0, 0)
                node = node.right
        node.symbol = symbol
    return root


def encode(text: str) -> tuple[dict[str, str], bytes, int]:
    codes = build_codes(text)
    bits = "".join(codes[ch] for ch in text)
    padded = bits + "0" * (-len(bits) % 8)
    packed = bytes(int(padded[i:i + 8], 2) for i in range(0, len(padded), 8))
    return codes, packed, len(bits)


def decode(codes: dict[str, str], packed: bytes, bit_count: int) -> str:
    if not codes or bit_count == 0:
        return ""
    bits = "".join(f"{byte:08b}" for byte in packed)[:bit_count]
    root = tree_from_codes(codes)
    out: list[str] = []
    node = root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node is None:
            raise ValueError("bit stream does not match the codebook")
        if node.symbol is not None:
            out.append(node.symbol)
            node = root
    return "".join(out)


def serialise_codebook(codes: dict[str, str]) -> str:
    return "|".join(f"{ord(sym)}:{code}" for sym, code in sorted(codes.items()))


def parse_codebook(blob: str) -> dict[str, str]:
    if not blob:
        return {}
    pairs = (item.split(":") for item in blob.split("|"))
    return {chr(int(point)): code for point, code in pairs}


def report(text: str, packed: bytes, book: str) -> str:
    if not text:
        return "n/a (empty input)"
    before = len(text)
    after = len(packed) + len(book.encode())
    return (f"{before} B -> {len(packed)} B payload + {len(book.encode())} B "
            f"codebook = {after} B ({after / before:.2f}x)")


def main() -> None:
    samples = [
        "",
        "abracadabra",
        "aaaaaaaaaaaaaaaaaaaabbbbbccccd",
        "the quick brown fox jumps over the lazy dog",
    ]
    for text in samples:
        codes, packed, nbits = encode(text)
        book = serialise_codebook(codes)
        back = decode(parse_codebook(book), packed, nbits)
        print(f"input     : {text!r}")
        print(f"codes     : {codes}")
        print(f"packed    : {packed.hex()} ({nbits} bits)")
        print(f"round-trip: {back == text}")
        print(f"size      : {report(text, packed, book)}")
        print()

    # Small inputs lose to the codebook overhead even when the payload shrinks.
    codes, packed, nbits = encode("aaaa")
    print(f"'aaaa' packs into {len(packed)} byte(s) but ships a codebook too")
    print(f"decoded: {decode(codes, packed, nbits)!r}")


if __name__ == "__main__":
    main()
