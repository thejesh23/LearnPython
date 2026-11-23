"""Examples and self-check: python3 -m strings.string_kit"""

import fnmatch
import random
import sys
from collections.abc import Callable

from . import (
    ALGORITHMS,
    build_lps,
    find_all,
    find_many,
    glob_match,
    longest_palindrome,
    longest_repeated_substring,
    longest_unique_substring,
    rle_decode,
    rle_encode,
    suffix_array,
    z_array,
)


def examples() -> None:
    text = "abracadabra"
    print("1. find 'abra' in", repr(text), {name: find_all(text, "abra", name) for name in ALGORITHMS})
    print("2. the tables behind them: lps('ababaca') =", build_lps("ababaca"),
          "| z('aabxaab') =", z_array("aabxaab"))
    print("3. suffix array of 'banana':", [("banana"[i:], i) for i in suffix_array("banana")])
    print("4. Aho-Corasick on 'ushers':", find_many("ushers", ["he", "she", "hers", "his"]))
    print("5. longest palindrome:", repr(longest_palindrome("babad")), repr(longest_palindrome("cbbd")))
    print("6. longest repeat:", repr(longest_repeated_substring("banana")),
          "| longest without repeats:", repr(longest_unique_substring("pwwkew")))
    runs = rle_encode("aaabccdddd")
    print("7. RLE:", runs, "->", repr(rle_decode(runs)), "| 'abcd' expands:", rle_encode("abcd"))
    print("8. glob:", glob_match("report.txt", "*.t?t"), glob_match("adceb", "*a*b"),
          glob_match("acdcb", "a*c?b"))


def occurrences(text: str, pattern: str) -> list[int]:
    return [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]


def brute_longest(text: str, ok: Callable[[str], bool]) -> int:
    """Length of the longest substring satisfying ``ok``, by trying them all."""
    subs = (text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1))
    return max((len(s) for s in subs if ok(s)), default=0)


def self_check() -> None:
    rng = random.Random(11)
    for _ in range(600):
        alphabet = rng.choice(["ab", "abc", "acgt"])
        text = "".join(rng.choices(alphabet, k=rng.randint(0, 40)))
        start = rng.randint(0, len(text))
        patterns = ["".join(rng.choices(alphabet, k=rng.randint(0, 4))),
                    text[start:start + rng.randint(0, 6)]]
        for pattern in patterns:
            want = occurrences(text, pattern)
            for name in ALGORITHMS:
                assert find_all(text, pattern, name) == want, (name, text, pattern)
        assert find_many(text, patterns) == {p: occurrences(text, p) for p in patterns}
        assert suffix_array(text) == sorted(range(len(text)), key=lambda i: text[i:])

        pal = longest_palindrome(text)
        assert pal in text and pal == pal[::-1]
        assert len(pal) == brute_longest(text, lambda s: s == s[::-1]), text
        rep = longest_repeated_substring(text)
        assert len(occurrences(text, rep)) >= 2 or not rep
        assert len(rep) == brute_longest(text, lambda s: len(occurrences(text, s)) >= 2), text
        uniq = longest_unique_substring(text)
        assert uniq in text and len(set(uniq)) == len(uniq)
        assert len(uniq) == brute_longest(text, lambda s: len(set(s)) == len(s)), text

        runs = rle_encode(text)
        assert rle_decode(runs) == text and all(a[0] != b[0] for a, b in zip(runs, runs[1:]))
        glob = "".join(rng.choices("ab?*", k=rng.randint(0, 5)))
        assert glob_match(text[:8], glob) == fnmatch.fnmatchcase(text[:8], glob), (text[:8], glob)
    try:
        find_all("abc", "b", algo="boyer_moore")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown algorithm accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
