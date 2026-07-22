"""Trie (prefix tree): one node per character, shared prefixes stored once.

Lookup costs O(m) in the key length — independent of how many keys are stored,
which is what a hash table cannot promise. The payoff is prefix queries:
autocomplete, longest-prefix routing, and dictionary-based word breaking all
fall out of walking to a node and enumerating below it.

Memory is the trade: a node per character, per branch.
"""

from collections.abc import Iterator


class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self, words: list[str] | None = None) -> None:
        self.root = TrieNode()
        for word in words or []:
            self.insert(word)

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def _walk(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def contains(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def with_prefix(self, prefix: str) -> list[str]:
        """Autocomplete: every stored word beginning with `prefix`."""
        node = self._walk(prefix)
        if node is None:
            return []
        return [prefix + suffix for suffix in self._collect(node)]

    def _collect(self, node: TrieNode) -> Iterator[str]:
        if node.is_word:
            yield ""
        for ch, child in sorted(node.children.items()):
            for suffix in self._collect(child):
                yield ch + suffix

    def longest_prefix_of(self, text: str) -> str:
        """Longest stored word that is a prefix of `text` — IP routing style."""
        node, best, current = self.root, "", ""
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                break
            current += ch
            if node.is_word:
                best = current
        return best

    def delete(self, word: str) -> bool:
        def prune(node: TrieNode, depth: int) -> bool:
            """Return True when this node can be removed by its parent."""
            if depth == len(word):
                if not node.is_word:
                    return False
                node.is_word = False
                return not node.children
            ch = word[depth]
            child = node.children.get(ch)
            if child is None:
                return False
            if prune(child, depth + 1):
                del node.children[ch]
                return not node.children and not node.is_word
            return False

        return prune(self.root, 0) or True


def main() -> None:
    trie = Trie(["cat", "car", "card", "care", "dog", "do"])
    print(f"contains 'car': {trie.contains('car')}, 'ca': {trie.contains('ca')}")
    print(f"starts_with 'ca': {trie.starts_with('ca')}")
    print(f"autocomplete 'car': {trie.with_prefix('car')}")
    print(f"autocomplete 'd': {trie.with_prefix('d')}")
    print(f"autocomplete 'x': {trie.with_prefix('x')}")
    print(f"longest prefix of 'cardigan': {trie.longest_prefix_of('cardigan')!r}")
    trie.delete("car")
    print(f"after deleting 'car': contains 'car' {trie.contains('car')}, "
          f"'card' still {trie.contains('card')}")


if __name__ == "__main__":
    main()
