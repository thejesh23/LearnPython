"""Slicing — `s[start:stop:step]`, the single most useful Python syntax.

Rules worth memorising:
  - `start` is included, `stop` is excluded (so `s[0:3]` has 3 characters).
  - Omitted bounds mean "from the beginning" and "to the end".
  - Negative indices count from the right: -1 is the last character.
  - A negative step walks backwards, which is why `s[::-1]` reverses.
  - Slices never raise IndexError — out-of-range bounds are clamped.

The same syntax works on every sequence: str, list, tuple, range, bytes.
"""


def main() -> None:
    s = "LearnPython"
    print(f"s          = {s}")
    print(f"s[0:5]     = {s[0:5]}")
    print(f"s[5:]      = {s[5:]}")
    print(f"s[:5]      = {s[:5]}")
    print(f"s[-6:]     = {s[-6:]}")
    print(f"s[::2]     = {s[::2]}   (every second character)")
    print(f"s[::-1]    = {s[::-1]}   (reversed)")
    print(f"s[1:8:3]   = {s[1:8:3]}")

    # Out-of-range bounds clamp instead of raising.
    print(f"s[5:999]   = {s[5:999]}")
    print(f"s[99:]     = {s[99:]!r}   (empty, not an error)")
    # A bare index does raise, though.
    try:
        s[99]
    except IndexError as exc:
        print(f"s[99] -> IndexError: {exc}")

    # Slicing a list copies; slicing assignment mutates in place.
    xs = [0, 1, 2, 3, 4, 5]
    print(f"xs[2:4]    = {xs[2:4]}")
    xs[2:4] = ["a", "b", "c"]  # replacement need not be the same length
    print(f"after xs[2:4] = ['a','b','c'] -> {xs}")
    del xs[0:2]
    print(f"after del xs[0:2] -> {xs}")

    # s[:] is the idiom for a shallow copy.
    original = [1, 2, 3]
    copy = original[:]
    copy.append(4)
    print(f"original = {original}, copy = {copy}")


if __name__ == "__main__":
    main()
