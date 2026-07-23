"""Levenshtein edit distance, plus the actual list of edits that achieves it.

The DP table dp[i][j] is the cheapest way to turn the first i characters of `a`
into the first j characters of `b`, using single-character insert, delete, and
substitute, each of cost one. The recurrence takes the best of three moves; a
match is a free "substitute" of a character by itself.

The distance alone throws away *how*. Keeping the full table lets you backtrack
from the bottom-right corner to the top-left, reading off each move you took,
and so recover a concrete operation script. Applying that script left to right
transforms `a` into `b` one edit at a time — the value made auditable.
"""

from dataclasses import dataclass


@dataclass
class Op:
    kind: str  # "keep", "insert", "delete", "substitute"
    index: int  # position in the current (evolving) string
    char: str = ""


def edit_table(a: str, b: str) -> list[list[int]]:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i  # delete all of a's prefix
    for j in range(m + 1):
        dp[0][j] = j  # insert all of b's prefix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,        # delete a[i-1]
                           dp[i][j - 1] + 1,        # insert b[j-1]
                           dp[i - 1][j - 1] + cost)  # match / substitute
    return dp


def recover_ops(a: str, b: str) -> list[Op]:
    dp = edit_table(a, b)
    i, j = len(a), len(b)
    ops: list[Op] = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            ops.append(Op("keep", i - 1, a[i - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(Op("substitute", i - 1, b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(Op("delete", i - 1, a[i - 1]))
            i -= 1
        else:
            ops.append(Op("insert", i, b[j - 1]))  # insert before position i
            j -= 1
    ops.reverse()
    return ops


def apply_ops(a: str, ops: list[Op]) -> str:
    chars = list(a)
    shift = 0  # net inserts-minus-deletes applied to the left of current index
    for op in ops:
        pos = op.index + shift
        if op.kind == "keep":
            pass
        elif op.kind == "substitute":
            chars[pos] = op.char
        elif op.kind == "delete":
            del chars[pos]
            shift -= 1
        else:  # insert
            chars.insert(pos, op.char)
            shift += 1
    return "".join(chars)


def main() -> None:
    a, b = "kitten", "sitting"
    ops = recover_ops(a, b)
    print(f"'{a}' -> '{b}', distance {edit_table(a, b)[len(a)][len(b)]}")
    for op in ops:
        if op.kind != "keep":
            print(f"  {op.kind:11} at {op.index} -> {op.char!r}")
    print(f"apply_ops reconstructs: {apply_ops(a, ops)!r}")

    # The recovered script must always rebuild b, and its edit count must
    # equal the DP distance.
    pairs = [("kitten", "sitting"), ("", "abc"), ("abc", ""), ("flaw", "lawn"),
             ("intention", "execution"), ("abc", "abc"), ("a", "b")]
    for x, y in pairs:
        script = recover_ops(x, y)
        assert apply_ops(x, script) == y, (x, y, apply_ops(x, script))
        edits = sum(1 for o in script if o.kind != "keep")
        assert edits == edit_table(x, y)[len(x)][len(y)], (x, y)
    print("every recovered script rebuilds b with the minimal edit count")


if __name__ == "__main__":
    main()
