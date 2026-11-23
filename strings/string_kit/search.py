"""Substring search behind one signature: ``f(text, pattern) -> start indexes``.

Every function reports overlapping matches in increasing order and may assume a
non-empty pattern; ``find_all`` handles the empty pattern once for all of them.
"""

from bisect import bisect_left, bisect_right

BASE, MOD = 256, 1_000_000_007


def naive_search(text: str, pattern: str) -> list[int]:
    """Try every alignment: O(n*m), the baseline the others improve on."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


def build_lps(pattern: str) -> list[int]:
    """lps[i]: longest proper prefix of pattern[:i+1] that is also its suffix."""
    lps, length = [0] * len(pattern), 0
    for i in range(1, len(pattern)):
        while length and pattern[i] != pattern[length]:
            length = lps[length - 1]  # fall back, never restart from zero
        if pattern[i] == pattern[length]:
            length += 1
        lps[i] = length
    return lps


def kmp_search(text: str, pattern: str) -> list[int]:
    """Knuth-Morris-Pratt, O(n + m): the text pointer never moves backwards."""
    lps, out, j = build_lps(pattern), [], 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            out.append(i - j + 1)
            j = lps[j - 1]  # keep going for overlapping matches
    return out


def z_array(s: str) -> list[int]:
    """z[i]: length of the longest substring starting at i that is a prefix of s."""
    n = len(s)
    z, left, right = [0] * n, 0, 0
    if n:
        z[0] = n  # by convention the whole string matches itself
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])  # reuse the current Z-box
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def z_search(text: str, pattern: str) -> list[int]:
    """Z-array of pattern + text: a value >= len(pattern) past the pattern is a match."""
    m = len(pattern)
    z = z_array(pattern + text)
    return [i - m for i in range(m, len(z)) if z[i] >= m]


def rabin_karp(text: str, pattern: str) -> list[int]:
    """Rolling hash: O(1) per slide, compare strings only when hashes collide."""
    n, m = len(text), len(pattern)
    if m > n:
        return []
    high = pow(BASE, m - 1, MOD)  # weight of the character leaving the window
    want = have = 0
    for i in range(m):
        want = (want * BASE + ord(pattern[i])) % MOD
        have = (have * BASE + ord(text[i])) % MOD
    out = []
    for i in range(n - m + 1):
        if have == want and text[i:i + m] == pattern:  # verify: hashes can collide
            out.append(i)
        if i + m < n:
            have = ((have - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return out


def suffix_array(text: str) -> list[int]:
    """Start indexes of all suffixes in sorted order, by prefix doubling."""
    n = len(text)
    sa, rank, k = list(range(n)), [ord(c) for c in text], 1
    while n > 1:
        def key(i: int) -> tuple[int, int]:
            return rank[i], rank[i + k] if i + k < n else -1

        sa.sort(key=key)
        new_rank = [0] * n
        for a, b in zip(sa, sa[1:]):
            new_rank[b] = new_rank[a] + (key(a) != key(b))
        rank, k = new_rank, k * 2
        if rank[sa[-1]] == n - 1:  # all ranks distinct: fully sorted
            break
    return sa


def suffix_array_search(text: str, pattern: str) -> list[int]:
    """Matches are one contiguous block of the suffix array; binary search its ends."""
    sa, m = suffix_array(text), len(pattern)

    def prefix(i: int) -> str:
        return text[i:i + m]

    return sorted(sa[bisect_left(sa, pattern, key=prefix):bisect_right(sa, pattern, key=prefix)])


def builtin_search(text: str, pattern: str) -> list[int]:
    """str.find in a loop, restarting one past each hit so overlaps count."""
    out, i = [], text.find(pattern)
    while i != -1:
        out.append(i)
        i = text.find(pattern, i + 1)
    return out
