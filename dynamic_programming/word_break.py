"""Word break: can a string be cut into a sequence of dictionary words?

Greedily taking the longest matching prefix fails: with the words "ab", "abc"
and "cd", the string "abcd" tempts you into "abc" and leaves a stranded "d",
while the correct split is "ab" then "cd". Taking the shortest prefix fails on
mirrored examples, so every cut point has to be considered.

The state is ok[i], meaning the first i characters can be segmented. It holds
when some earlier cut j has ok[j] true and the piece s[j:i] is in the
dictionary, with ok[0] true because the empty prefix is trivially segmented.
Storing the j that worked for each i lets one valid segmentation be walked
back. Limiting the inner scan to the longest dictionary word keeps it cheap on
long strings.

Complexity: O(n * L) substring tests where L is the longest word length, each
test costing O(L) to hash, so O(n * L**2) overall with O(n) space.
"""


def word_break(s: str, words: list[str]) -> bool:
    vocab = set(words)
    longest = max((len(w) for w in vocab), default=0)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - longest), i):
            if ok[j] and s[j:i] in vocab:
                ok[i] = True
                break
    return ok[len(s)]


def word_break_segmentation(s: str, words: list[str]) -> list[str] | None:
    """Return one valid segmentation, or None if the string cannot be split."""
    vocab = set(words)
    longest = max((len(w) for w in vocab), default=0)
    cut: list[int | None] = [None] * (len(s) + 1)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - longest), i):
            if ok[j] and s[j:i] in vocab:
                ok[i], cut[i] = True, j
                break
    if not ok[len(s)]:
        return None
    out: list[str] = []
    i = len(s)
    while i > 0:
        j = cut[i]
        assert j is not None
        out.append(s[j:i])
        i = j
    out.reverse()
    return out


def word_break_all(s: str, words: list[str]) -> list[list[str]]:
    """Every segmentation, memoised by suffix start — can be exponential."""
    vocab = set(words)
    longest = max((len(w) for w in vocab), default=0)
    cache: dict[int, list[list[str]]] = {}

    def solve(start: int) -> list[list[str]]:
        if start == len(s):
            return [[]]
        if start in cache:
            return cache[start]
        found: list[list[str]] = []
        for end in range(start + 1, min(len(s), start + longest) + 1):
            piece = s[start:end]
            if piece in vocab:
                found.extend([piece] + rest for rest in solve(end))
        cache[start] = found
        return found

    return solve(0)


def main() -> None:
    cases = [
        ("applepenapple", ["apple", "pen"]),
        ("catsanddog", ["cat", "cats", "and", "sand", "dog"]),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"]),
        ("aaaaaaa", ["aaa", "aaaa"]),
        ("leetcode", ["leet", "code"]),
    ]
    for s, words in cases:
        pieces = word_break_segmentation(s, words)
        print(f"{s!r} with {words}")
        print(f"  breakable: {word_break(s, words)}  segmentation: {pieces}")
        assert (pieces is not None) == word_break(s, words)
        if pieces is not None:
            assert "".join(pieces) == s

    print("\nall segmentations of 'catsanddog':")
    for pieces in word_break_all("catsanddog", ["cat", "cats", "and", "sand",
                                                "dog"]):
        print("  " + " ".join(pieces))

    print("\nedge cases:")
    print("  empty string:", word_break("", ["a"]),
          word_break_segmentation("", ["a"]))
    print("  empty dictionary:", word_break("abc", []),
          word_break_segmentation("abc", []))
    print("  word longer than string:", word_break("ab", ["abcd"]))
    print("  exact single word:", word_break_segmentation("hello", ["hello"]))


if __name__ == "__main__":
    main()
