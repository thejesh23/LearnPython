"""Ranked autocomplete: a trie whose nodes remember their best completions.

data_structures/trie.py lists every word under a prefix. Real autocomplete
wants only the top few, ranked by how often each word was chosen, and must
answer while the user types. Walking the whole subtree under "a" on every
keystroke would visit most of the dictionary.

The trick is to cache, at every node, the k best words in its subtree. A query
then walks down the prefix and returns that node's cached list: O(len(prefix))
with no subtree walk. The price moves to updates, which refresh the cache on
each node along the word's path, O(len(word) * k). Typing is far more common
than adding words, so that is the right trade.

Counts here only ever grow, which is what keeps the cache simple: a word can
only climb, so a word pushed out of a node's top k never needs to come back.
Supporting decrements would mean refilling the cache from the subtree.
"""

from __future__ import annotations

import heapq
import random
from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, TrieNode] = field(default_factory=dict)
    top: list[tuple[int, str]] = field(default_factory=list)  # (-count, word)


class Autocomplete:
    def __init__(self, k: int = 3) -> None:
        self.k = k
        self.root = TrieNode()
        self.counts: dict[str, int] = {}

    def add(self, word: str, times: int = 1) -> None:
        count = self.counts.get(word, 0) + times
        self.counts[word] = count
        for node in [self.root, *self._path(word)]:
            node.top = [entry for entry in node.top if entry[1] != word]
            node.top.append((-count, word))
            node.top.sort()
            del node.top[self.k:]

    def _path(self, word: str) -> list[TrieNode]:
        nodes, node = [], self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
            nodes.append(node)
        return nodes

    def suggest(self, prefix: str) -> list[str]:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return [word for _, word in node.top]

    def suggest_brute(self, prefix: str) -> list[str]:
        matches = [(-c, w) for w, c in self.counts.items() if w.startswith(prefix)]
        return [w for _, w in heapq.nsmallest(self.k, matches)]


def main() -> None:
    ac = Autocomplete(k=3)
    for word, times in [("car", 5), ("card", 2), ("care", 7), ("careful", 1),
                        ("cart", 3), ("cat", 9), ("dog", 4), ("door", 1)]:
        ac.add(word, times)

    for prefix in ["c", "ca", "car", "care", "d", "do", "x", ""]:
        print(f"{prefix!r:>8}: {ac.suggest(prefix)}")

    print("\nthe user keeps choosing 'careful':")
    ac.add("careful", 10)
    print(f"{'car':>8}: {ac.suggest('car')}")

    rng = random.Random(10)
    big = Autocomplete(k=4)
    words = ["".join(rng.choices("abc", k=rng.randint(1, 5))) for _ in range(300)]
    for w in words:
        big.add(w, rng.randint(1, 5))
    prefixes = {w[:i] for w in words for i in range(len(w) + 1)}
    ok = all(big.suggest(p) == big.suggest_brute(p) for p in prefixes)
    print(f"\ncached top-k matches brute force on {len(prefixes)} prefixes: {ok}")


if __name__ == "__main__":
    main()
