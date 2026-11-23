"""String utilities: many patterns at once, palindromes, repeats, windows, RLE, globs."""

from collections import deque
from itertools import groupby

from .search import suffix_array


def find_many(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """Aho-Corasick: start indexes of every pattern, in one pass over the text."""
    goto: list[dict[str, int]] = [{}]
    fail, out = [0], [[]]
    for word in set(filter(None, patterns)):  # build a trie of the patterns
        node = 0
        for ch in word:
            if ch not in goto[node]:
                goto[node][ch] = len(goto)
                goto.append({})
                fail.append(0)
                out.append([])
            node = goto[node][ch]
        out[node].append(word)
    queue = deque(goto[0].values())  # BFS: a failure target is always shallower
    while queue:
        node = queue.popleft()
        for ch, child in goto[node].items():
            queue.append(child)
            f = fail[node]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[child] = goto[f].get(ch, 0)
            out[child] = out[child] + out[fail[child]]  # inherit suffix matches
    hits: dict[str, list[int]] = {p: [] if p else list(range(len(text) + 1)) for p in patterns}
    node = 0
    for i, ch in enumerate(text):
        while node and ch not in goto[node]:
            node = fail[node]
        node = goto[node].get(ch, 0)
        for word in out[node]:
            hits[word].append(i - len(word) + 1)
    return hits


def longest_palindrome(text: str) -> str:
    """Manacher, O(n): '#' separators make every palindrome odd, mirrors reuse work."""
    t = "^#" + "#".join(text) + "#$"  # distinct sentinels stop expansion at the ends
    radii, center, right = [0] * len(t), 0, 0
    for i in range(1, len(t) - 1):
        if i < right:
            radii[i] = min(right - i, radii[2 * center - i])
        while t[i + radii[i] + 1] == t[i - radii[i] - 1]:
            radii[i] += 1
        if i + radii[i] > right:
            center, right = i, i + radii[i]
    radius, mid = max((r, -i) for i, r in enumerate(radii))  # leftmost on ties
    start = (-mid - radius) // 2
    return text[start:start + radius]


def longest_repeated_substring(text: str) -> str:
    """Longest substring occurring twice (overlaps allowed), via suffix array + LCP."""
    sa = suffix_array(text)
    rank = {suffix: i for i, suffix in enumerate(sa)}
    best_len = best_start = h = 0
    for i in range(len(text)):  # Kasai: LCP drops by at most 1 per step
        if rank[i] == 0:
            h = 0
            continue
        j = sa[rank[i] - 1]
        while i + h < len(text) and j + h < len(text) and text[i + h] == text[j + h]:
            h += 1
        if h > best_len:
            best_len, best_start = h, i
        h = max(h - 1, 0)
    return text[best_start:best_start + best_len]


def longest_unique_substring(text: str) -> str:
    """Sliding window: the longest run with no repeated character, O(n)."""
    last: dict[str, int] = {}
    start = best_start = best_len = 0
    for i, ch in enumerate(text):
        if last.get(ch, -1) >= start:  # seen inside the window: jump past it
            start = last[ch] + 1
        last[ch] = i
        if i - start + 1 > best_len:
            best_start, best_len = start, i - start + 1
    return text[best_start:best_start + best_len]


def rle_encode(text: str) -> list[tuple[str, int]]:
    """Run-length encode: 'aaab' -> [('a', 3), ('b', 1)]."""
    return [(ch, len(list(run))) for ch, run in groupby(text)]


def rle_decode(runs: list[tuple[str, int]]) -> str:
    """Exact inverse of rle_encode."""
    return "".join(ch * count for ch, count in runs)


def glob_match(text: str, pattern: str) -> bool:
    """Whole-string glob by DP: '?' is any one character, '*' any run."""
    row = [True] + [False] * len(pattern)  # row[j]: text[:0] matches pattern[:j]
    for j, p in enumerate(pattern, 1):
        row[j] = row[j - 1] and p == "*"
    for ch in text:
        new = [False] * (len(pattern) + 1)
        for j, p in enumerate(pattern, 1):
            if p == "*":
                new[j] = new[j - 1] or row[j]  # '*' matches empty, or eats ch
            else:
                new[j] = row[j - 1] and p in ("?", ch)
        row = new
    return row[-1]
