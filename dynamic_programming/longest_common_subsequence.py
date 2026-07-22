"""Longest common subsequence: the longest sequence appearing in both inputs in
order, though not necessarily contiguously.

"ACE" is a subsequence of "ABCDE" but "AEC" is not, because order must hold.
The state is lcs[i][j], the length of the best common subsequence of the first
i characters of a and the first j characters of b. Compare the two characters
ending those prefixes: if they match, they can both be consumed and the answer
is 1 + lcs[i-1][j-1]; if they do not, one of the two characters must be
dropped, so the answer is max(lcs[i-1][j], lcs[i][j-1]).

Walking the finished table backwards from the bottom right recovers an actual
subsequence: a diagonal move means the characters matched, and otherwise you
follow whichever neighbour holds the same value. Ties mean several optimal
answers exist and the walk simply picks one.

Complexity: O(m * n) time and space; this is the engine behind diff tools.
"""


def lcs_table(a: str, b: str) -> list[list[int]]:
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def lcs_length(a: str, b: str) -> int:
    return lcs_table(a, b)[len(a)][len(b)]


def lcs_string(a: str, b: str) -> str:
    """Backtrack through the table to recover one longest common subsequence."""
    table = lcs_table(a, b)
    out: list[str] = []
    i, j = len(a), len(b)
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out)


def lcs_length_rolling(a: str, b: str) -> int:
    """Length only, in O(min(m, n)) space — the table cannot be backtracked."""
    if len(b) > len(a):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for ch in a:
        curr = [0] * (len(b) + 1)
        for j, other in enumerate(b, start=1):
            curr[j] = prev[j - 1] + 1 if ch == other else max(prev[j], curr[j - 1])
        prev = curr
    return prev[len(b)]


def print_table(a: str, b: str) -> None:
    table = lcs_table(a, b)
    print("      " + "  ".join(f"{c}" for c in " " + b))
    for i, row in enumerate(table):
        label = " " if i == 0 else a[i - 1]
        print(f"  {label}  " + "  ".join(str(v) for v in row))


def main() -> None:
    pairs = [
        ("AGGTAB", "GXTXAYB"),
        ("dynamic", "programming"),
        ("abcde", "ace"),
        ("kitten", "sitting"),
    ]
    for a, b in pairs:
        result = lcs_string(a, b)
        print(f"{a!r} vs {b!r} -> {result!r} (length {len(result)})")
        assert len(result) == lcs_length(a, b) == lcs_length_rolling(a, b)

    print("\nedge cases:")
    print("  empty vs 'abc':   ", repr(lcs_string("", "abc")))
    print("  identical strings:", repr(lcs_string("hello", "hello")))
    print("  nothing in common:", repr(lcs_string("abc", "xyz")))

    print("\ntable for 'abcde' vs 'ace':")
    print_table("abcde", "ace")


if __name__ == "__main__":
    main()
