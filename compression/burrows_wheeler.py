"""Burrows-Wheeler transform: a reversible permutation that clusters like letters.

Write down every rotation of the text, sort them, and read off the last column.
That column is the transform. Each character in it is the one that *precedes* a
sorted context, and in natural text the same contexts recur ("he" is usually
preceded by t), so the output arrives in long runs — perfect food for
move-to-front plus run-length or entropy coding. bzip2 is built on exactly this.

Inverting it looks impossible until you notice the first column is just the
last column sorted. The i-th occurrence of a character in the last column and
the i-th occurrence in the first column are the same character of the original
string; that pairing is the LF mapping, and following it backwards replays the
text. A sentinel character smaller than everything else marks the true start so
no rotation bookkeeping is needed.

Naive rotation sorting is O(n^2 log n); real implementations use suffix arrays.
"""

SENTINEL = "\x00"


def bwt(text: str) -> str:
    if SENTINEL in text:
        raise ValueError("input must not contain the sentinel")
    s = text + SENTINEL
    rotations = sorted(s[i:] + s[:i] for i in range(len(s)))
    return "".join(rot[-1] for rot in rotations)


def inverse_bwt(last: str) -> str:
    if not last:
        return ""
    n = len(last)
    # Rank of each position among equal characters, then where that character
    # starts in the sorted (first) column. rank + start is the LF mapping.
    seen: dict[str, int] = {}
    rank = [0] * n
    for i, ch in enumerate(last):
        rank[i] = seen.get(ch, 0)
        seen[ch] = rank[i] + 1
    start: dict[str, int] = {}
    total = 0
    for ch in sorted(seen):
        start[ch] = total
        total += seen[ch]

    # Row 0 is the rotation beginning with the sentinel; each LF step walks one
    # character further back through the original string.
    row = 0
    out: list[str] = []
    for _ in range(n - 1):
        ch = last[row]
        out.append(ch)
        row = start[ch] + rank[row]
    out.reverse()
    return "".join(out)


def longest_run(s: str) -> int:
    best = run = 0
    for i, ch in enumerate(s):
        run = run + 1 if i and ch == s[i - 1] else 1
        best = max(best, run)
    return best


def main() -> None:
    samples = ["", "banana", "the rain in spain stays mainly in the plain", "abcdef"]
    for text in samples:
        coded = bwt(text)
        back = inverse_bwt(coded)
        shown = coded.replace(SENTINEL, "$")
        print(f"input      : {text!r}")
        print(f"transform  : {shown!r}")
        print(f"round-trip : {back == text}")
        print(f"longest run: {longest_run(text)} -> {longest_run(coded)}")
        print()

    # The transform is the same length as the input plus the sentinel, so on its
    # own it compresses nothing; the gain shows up in what comes after it.
    text = "the rain in spain"
    print(f"size {len(text)} -> {len(bwt(text))} chars (no gain until RLE/entropy)")


if __name__ == "__main__":
    main()
