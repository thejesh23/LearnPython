"""Rabin-Karp: hash the pattern, roll the hash across the text.

A rolling hash updates in O(1) when the window slides — subtract the outgoing
character's contribution, shift, add the incoming one. Compare hashes first and
only verify a real match on a hit, so the expected cost is O(n + m).

Hash collisions make the worst case O(n*m); a large prime modulus makes them
rare. The real payoff is multi-pattern search: hash every pattern once and
check the window hash against a set.
"""

BASE = 256
MOD = 1_000_000_007


def rabin_karp(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    high = pow(BASE, m - 1, MOD)  # BASE^(m-1), for removing the leading char
    pattern_hash = window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % MOD
        window_hash = (window_hash * BASE + ord(text[i])) % MOD

    out: list[int] = []
    for i in range(n - m + 1):
        if window_hash == pattern_hash and text[i:i + m] == pattern:
            out.append(i)  # verify: equal hashes can still be different strings
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * high) % MOD
            window_hash = (window_hash * BASE + ord(text[i + m])) % MOD
    return out


def search_many(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """Same-length patterns share one rolling hash pass."""
    if not patterns:
        return {}
    m = len(patterns[0])
    assert all(len(p) == m for p in patterns), "same length required"
    wanted = {p: [] for p in patterns}
    hashes = {}
    for p in patterns:
        h = 0
        for ch in p:
            h = (h * BASE + ord(ch)) % MOD
        hashes.setdefault(h, []).append(p)

    high = pow(BASE, m - 1, MOD)
    window = 0
    for i in range(min(m, len(text))):
        window = (window * BASE + ord(text[i])) % MOD
    for i in range(len(text) - m + 1):
        for candidate in hashes.get(window, []):
            if text[i:i + m] == candidate:
                wanted[candidate].append(i)
        if i < len(text) - m:
            window = (window - ord(text[i]) * high) % MOD
            window = (window * BASE + ord(text[i + m])) % MOD
    return wanted


def main() -> None:
    print(rabin_karp("abracadabra", "abra"))
    print(rabin_karp("aaaaa", "aa"))
    print(rabin_karp("abc", "d"))
    print(search_many("the cat sat on the mat", ["cat", "mat", "sat"]))


if __name__ == "__main__":
    main()
