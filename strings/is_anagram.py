"""Anagram detection: same multiset of characters, different order.

Sorting both strings is O(n log n) and one line. Counting is O(n) and is the
version that extends: grouping anagrams needs a canonical *key* per word, and
a frozen Counter (or the sorted tuple) is exactly that.
"""

from collections import Counter, defaultdict


def is_anagram_sorted(a: str, b: str) -> bool:
    return sorted(a) == sorted(b)


def is_anagram_counted(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    counts: dict[str, int] = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1
    return True


def is_anagram_relaxed(a: str, b: str) -> bool:
    """Ignore case and spaces — the version people actually mean."""
    clean = lambda s: Counter(ch for ch in s.casefold() if ch.isalnum())  # noqa: E731
    return clean(a) == clean(b)


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[str, ...], list[str]] = defaultdict(list)
    for word in words:
        groups[tuple(sorted(word))].append(word)
    return list(groups.values())


def main() -> None:
    print(is_anagram_sorted("listen", "silent"), is_anagram_sorted("rat", "car"))
    print(is_anagram_counted("anagram", "nagaram"))
    print(is_anagram_relaxed("Dormitory", "Dirty Room"))
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))


if __name__ == "__main__":
    main()
