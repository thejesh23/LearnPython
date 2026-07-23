"""Longest repeated substring: the longest string that occurs at least twice.

Two suffixes that share a long common prefix witness a repeat, and in a suffix
array the suffixes sharing the longest prefixes sit next to each other. So the
answer is simply the largest value in the LCP array — the longest common prefix
between any two adjacent sorted suffixes — and the substring itself is that many
leading characters of the corresponding suffix.

Building the suffix array by prefix-doubling and the LCP array by Kasai's
algorithm makes the whole thing O(n log n), far better than the O(n^3) brute
force of testing every substring for a second occurrence.
"""


def build_suffix_array(s: str) -> list[int]:
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while k < n:
        def key(i: int) -> tuple[int, int]:
            return (rank[i], rank[i + k] if i + k < n else -1)

        sa.sort(key=key)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (key(sa[i]) != key(sa[i - 1]))
        rank = tmp[:]
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def build_lcp(s: str, sa: list[int]) -> list[int]:
    n = len(s)
    rank = [0] * n
    for i, suf in enumerate(sa):
        rank[suf] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] == 0:
            h = 0
            continue
        j = sa[rank[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rank[i]] = h
        if h:
            h -= 1
    return lcp


def longest_repeated_substring(s: str) -> str:
    if len(s) < 2:
        return ""
    sa = build_suffix_array(s)
    lcp = build_lcp(s, sa)
    best_len = max(lcp)
    if best_len == 0:
        return ""
    pos = lcp.index(best_len)
    start = sa[pos]
    return s[start:start + best_len]


def brute_longest_repeated(s: str) -> str:
    best = ""
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]
            if len(sub) > len(best) and s.find(sub, i + 1) != -1:
                best = sub
    return best


def main() -> None:
    for s in ["banana", "abcpqrabpqz", "aaaaa", "abcdef", "mississippi"]:
        got = longest_repeated_substring(s)
        print(f"'{s}': longest repeat = {got!r}")

    # A repeat means a second occurrence exists; cross-check length against
    # the brute-force answer (ties may differ, so compare lengths only).
    for s in ["banana", "aaaaa", "abcdef", "mississippi", "abababab",
              "abcpqrabpqz", "z", "", "aa", "xyzxy"]:
        got = longest_repeated_substring(s)
        want = brute_longest_repeated(s)
        if got:
            assert s.find(got) != s.rfind(got), (s, got)
        assert len(got) == len(want), (s, got, want)
    print("all lengths match brute force and every repeat truly recurs")


if __name__ == "__main__":
    main()
