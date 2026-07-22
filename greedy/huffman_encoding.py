"""Huffman coding: an optimal prefix code built by repeated greedy merging.

Count how often each symbol occurs, then put every symbol in a min-heap keyed
by frequency. Repeatedly pop the two least frequent nodes and push a new node
whose frequency is their sum and whose children they are. When one node is left
it is the root; walking left appends a 0 bit and walking right a 1, so each
symbol's path spells its code.

The greedy step is justified by an exchange argument: in an optimal tree the two
least frequent symbols can always be made deepest siblings, because swapping any
deeper symbol with a more frequent shallower one never increases the total
cost. Merging them therefore commits to nothing an optimal tree would refuse.

Because every symbol sits at a leaf, no code is a prefix of another, so the
stream decodes unambiguously with no separators. Building costs O(k log k) for k
distinct symbols; encoding and decoding are linear. The one-symbol input is the
edge case worth handling: it has no branch to encode, so it gets the code "0".
"""

import heapq
from collections import Counter
from dataclasses import dataclass, field


@dataclass(order=True)
class Node:
    freq: int
    order: int                      # tie-break so heapq never compares payloads
    symbol: str | None = field(default=None, compare=False)
    left: "Node | None" = field(default=None, compare=False)
    right: "Node | None" = field(default=None, compare=False)


def build_tree(text: str) -> Node | None:
    counts = Counter(text)
    if not counts:
        return None
    counter = iter(range(1 << 30))
    heap = [Node(f, next(counter), sym) for sym, f in sorted(counts.items())]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, Node(a.freq + b.freq, next(counter), None, a, b))
    return heap[0]


def build_codebook(root: Node | None) -> dict[str, str]:
    if root is None:
        return {}
    if root.symbol is not None:  # a single distinct symbol has no branches
        return {root.symbol: "0"}
    codes: dict[str, str] = {}

    def walk(node: Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix
            return
        assert node.left is not None and node.right is not None
        walk(node.left, prefix + "0")
        walk(node.right, prefix + "1")

    walk(root, "")
    return codes


def encode(text: str, codes: dict[str, str]) -> str:
    return "".join(codes[ch] for ch in text)


def decode(bits: str, root: Node | None) -> str:
    if root is None:
        return ""
    if root.symbol is not None:
        return root.symbol * len(bits)
    out: list[str] = []
    node = root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        assert node is not None
        if node.symbol is not None:
            out.append(node.symbol)
            node = root
    return "".join(out)


def report(text: str) -> None:
    root = build_tree(text)
    codes = build_codebook(root)
    bits = encode(text, codes)
    back = decode(bits, root)
    fixed = len(text) * 8
    print(f"text ({len(text)} chars): {text!r}")
    if codes:
        widest = max(len(c) for c in codes.values())
        for sym, code in sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[0])):
            print(f"  {sym!r:>5} -> {code:<{widest}}  ({text.count(sym)}x)")
    print(f"  encoded bits: {len(bits)} vs {fixed} fixed-width")
    ratio = len(bits) / fixed if fixed else 0.0
    print(f"  compression ratio: {ratio:.3f}  round-trip ok: {back == text}")


def main() -> None:
    report("abracadabra")
    print()
    report("the quick brown fox jumps over the lazy dog")
    print()
    report("aaaaaaaaaaaaaaaaaaaab")

    print()
    print(f"empty text codebook: {build_codebook(build_tree(''))}")
    print(f"empty text decode:   {decode('', build_tree(''))!r}")

    single = build_tree("zzzz")
    print(f"single symbol codebook: {build_codebook(single)}")
    print(f"single symbol round-trip: "
          f"{decode(encode('zzzz', build_codebook(single)), single)!r}")

    # Uniform frequencies give a balanced tree: every code is the same length,
    # so Huffman does no better here than a flat 2-bit code would.
    report("abcd" * 4)


if __name__ == "__main__":
    main()
