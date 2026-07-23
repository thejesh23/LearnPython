"""Suffix automaton: the smallest DFA that accepts every substring of a string.

Built online, one character at a time, it stays minimal at all times and has at
most 2n states and 3n transitions. Each state represents a set of substrings
that occur at exactly the same set of end positions; `link` points to the state
holding the longest proper suffix that lives in a different such set, and `length`
is the longest substring in the state.

Adding a character extends the automaton and, where needed, "clones" a state to
keep the end-position equivalence classes correct — the one subtle step. The
payoff: the number of distinct substrings equals the sum over states of
(length[v] - length[link[v]]), computable in O(n).
"""


class SuffixAutomaton:
    def __init__(self) -> None:
        self.length = [0]
        self.link = [-1]
        self.trans: list[dict[str, int]] = [{}]
        self.last = 0

    def extend(self, ch: str) -> None:
        cur = self._new(self.length[self.last] + 1)
        p = self.last
        while p != -1 and ch not in self.trans[p]:
            self.trans[p][ch] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.trans[p][ch]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q  # q is already the right suffix state
            else:
                clone = self._new(self.length[p] + 1)
                self.trans[clone] = dict(self.trans[q])
                self.link[clone] = self.link[q]
                while p != -1 and self.trans[p].get(ch) == q:
                    self.trans[p][ch] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

    def _new(self, length: int) -> int:
        self.length.append(length)
        self.link.append(-1)
        self.trans.append({})
        return len(self.length) - 1

    def distinct_substrings(self) -> int:
        """Count of distinct non-empty substrings of the built string."""
        return sum(self.length[v] - self.length[self.link[v]]
                   for v in range(1, len(self.length)))


def brute_distinct(s: str) -> int:
    return len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})


def build(s: str) -> SuffixAutomaton:
    sam = SuffixAutomaton()
    for ch in s:
        sam.extend(ch)
    return sam


def main() -> None:
    for s in ["abcbc", "aaaa", "banana"]:
        n = build(s).distinct_substrings()
        print(f"'{s}': {n} distinct substrings (brute {brute_distinct(s)})")

    # Cross-check the automaton count against a brute-force set on many strings.
    for s in ["", "a", "ab", "aba", "abab", "mississippi", "abracadabra",
              "aaaaaa", "xyzzy", "abcabcabc"]:
        got = build(s).distinct_substrings()
        want = brute_distinct(s)
        assert got == want, (s, got, want)
    print("distinct-substring counts match brute force on all cases")


if __name__ == "__main__":
    main()
