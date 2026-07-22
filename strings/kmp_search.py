"""Knuth-Morris-Pratt: substring search in O(n + m), never backing up the text.

The failure function (`lps`) records, for each prefix of the pattern, the
length of the longest proper prefix that is also a suffix. On a mismatch, that
tells you how far the pattern can shift without missing a match — so the text
pointer only ever moves forward.

Naive search is O(n*m) on adversarial input like "aaaa...b" in "aaaa...a".
"""


def build_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]  # fall back, do not restart
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text: str, pattern: str) -> list[int]:
    """All start indices where `pattern` occurs in `text`."""
    if not pattern:
        return list(range(len(text) + 1))
    lps = build_lps(pattern)
    out: list[int] = []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                out.append(i - j)
                j = lps[j - 1]  # keep going for overlapping matches
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return out


def main() -> None:
    print(f"lps('ababaca') = {build_lps('ababaca')}")
    print(f"lps('aaaa')    = {build_lps('aaaa')}")
    print(kmp_search("ababcabcabababd", "ababd"))
    print(kmp_search("aaaaa", "aa"))  # overlapping matches
    print(kmp_search("abc", "xyz"))
    print(f"str.find agrees: {'ababcabcabababd'.find('ababd')}")


if __name__ == "__main__":
    main()
