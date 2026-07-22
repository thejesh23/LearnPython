"""Manacher's algorithm: the longest palindromic substring in O(n).

Two ideas. First, interleave separators ("aba" -> "^#a#b#a#$") so every
palindrome has odd length and the even/odd cases collapse into one. Second,
reuse work: inside a known palindrome centred at C with right edge R, position
i mirrors i' = 2C - i, so radii[i] starts at min(R - i, radii[i']) instead of 0.

Each expansion step advances R, so the total work is linear.
"""


def longest_palindrome(text: str) -> str:
    if not text:
        return ""
    # Transform: separators between and around every character.
    t = "^#" + "#".join(text) + "#$"
    radii = [0] * len(t)
    center = right = 0

    for i in range(1, len(t) - 1):
        if i < right:
            radii[i] = min(right - i, radii[2 * center - i])  # mirror
        while t[i + radii[i] + 1] == t[i - radii[i] - 1]:  # sentinels stop this
            radii[i] += 1
        if i + radii[i] > right:
            center, right = i, i + radii[i]

    best_radius, best_center = max((r, i) for i, r in enumerate(radii))
    start = (best_center - best_radius) // 2  # map back to the original index
    return text[start:start + best_radius]


def count_palindromic_substrings(text: str) -> int:
    """Every centre contributes (radius+1)//2 palindromes in the same pass."""
    t = "^#" + "#".join(text) + "#$"
    radii = [0] * len(t)
    center = right = 0
    total = 0
    for i in range(1, len(t) - 1):
        if i < right:
            radii[i] = min(right - i, radii[2 * center - i])
        while t[i + radii[i] + 1] == t[i - radii[i] - 1]:
            radii[i] += 1
        if i + radii[i] > right:
            center, right = i, i + radii[i]
        total += (radii[i] + 1) // 2
    return total


def main() -> None:
    for s in ("babad", "cbbd", "a", "", "forgeeksskeegfor"):
        print(f"{s!r:20} -> {longest_palindrome(s)!r}")
    print(f"palindromic substrings in 'aaa' = {count_palindromic_substrings('aaa')}")


if __name__ == "__main__":
    main()
