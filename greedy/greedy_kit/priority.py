"""Greedy by priority: best value density first, rarest symbols merged first."""

import heapq
from collections import Counter
from collections.abc import Sequence

Item = tuple[str, float, float]  # name, value, weight


def fractional_knapsack(items: Sequence[Item], capacity: float) -> tuple[float, list[tuple[str, float]]]:
    """Best value when items may be split, and the fraction taken of each item used.

    Take items by value per unit weight, highest first, and a fraction of the
    first one that does not fit. Optimal only because items are divisible;
    for 0/1 knapsack the same rule can be wrong.
    """
    total, taken, room = 0.0, [], capacity
    for name, value, weight in sorted(items, key=lambda it: it[1] / it[2], reverse=True):
        if room <= 0:
            break
        fraction = 1.0 if weight <= room else room / weight
        taken.append((name, fraction))
        total += value * fraction
        room = room - weight if fraction == 1.0 else 0
    return total, taken


def huffman_codes(text: str) -> dict[str, str]:
    """An optimal prefix-free bit code for the symbols of text.

    Repeatedly merge the two least frequent subtrees; every symbol in the
    left one gains a leading 0, every symbol in the right one a leading 1.
    """
    counts = Counter(text)
    if len(counts) == 1:
        return {next(iter(counts)): "0"}  # one symbol still needs one bit
    # (frequency, tie-break, codes so far); the tie-break keeps dicts uncompared.
    heap = [(f, i, {sym: ""}) for i, (sym, f) in enumerate(sorted(counts.items()))]
    heapq.heapify(heap)
    tie = len(heap)
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        merged = {s: "0" + c for s, c in left.items()} | {s: "1" + c for s, c in right.items()}
        heapq.heappush(heap, (f1 + f2, tie, merged))
        tie += 1
    return heap[0][2] if heap else {}


def encode(text: str, codes: dict[str, str]) -> str:
    """Concatenate each symbol's code."""
    return "".join(codes[ch] for ch in text)


def decode(bits: str, codes: dict[str, str]) -> str:
    """Read bits left to right; prefix-freeness means the first match is the symbol."""
    lookup = {code: sym for sym, code in codes.items()}
    out, current = [], ""
    for bit in bits:
        current += bit
        if current in lookup:
            out.append(lookup[current])
            current = ""
    if current:
        raise ValueError("bits end in the middle of a code")
    return "".join(out)
