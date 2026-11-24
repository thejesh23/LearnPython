"""Ranked autocomplete: a trie that caches the top k words at each node."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class _TrieNode:
    children: dict[str, _TrieNode] = field(default_factory=dict)
    top: list[tuple[int, str]] = field(default_factory=list)  # (-count, word)


class Autocomplete:
    """add() is O(len(word) * k); suggest() is O(len(prefix)). Counts only grow."""

    def __init__(self, k: int = 3) -> None:
        self.k = k
        self.counts: dict[str, int] = {}
        self._root = _TrieNode()

    def add(self, word: str, times: int = 1) -> None:
        if times < 1:
            raise ValueError("times must be positive; counts only grow")
        count = self.counts.get(word, 0) + times
        self.counts[word] = count
        node = self._root
        path = [node]
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
            path.append(node)
        for node in path:
            node.top = [e for e in node.top if e[1] != word] + [(-count, word)]
            node.top.sort()
            del node.top[self.k:]

    def suggest(self, prefix: str) -> list[str]:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return [word for _, word in node.top]
