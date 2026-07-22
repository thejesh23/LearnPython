"""Sliding window maximum: the max of every k-length window, in O(n) total.

A monotonic deque holds *indices* whose values decrease from front to back.
Before pushing i, pop every smaller value from the back — they can never be the
maximum again, because i is both larger and newer. The front is always the
current window's max; pop it once it slides out of range.

Each index is pushed and popped at most once: O(n) time, O(k) space.
"""

from collections import deque


def sliding_window_max(values: list[int], k: int) -> list[int]:
    if k <= 0 or not values:
        return []
    window: deque[int] = deque()  # indices, values decreasing
    out: list[int] = []
    for i, value in enumerate(values):
        while window and values[window[-1]] <= value:
            window.pop()  # smaller and older: never useful again
        window.append(i)
        if window[0] <= i - k:
            window.popleft()  # front has slid out of the window
        if i >= k - 1:
            out.append(values[window[0]])
    return out


def sliding_window_min(values: list[int], k: int) -> list[int]:
    return [-v for v in sliding_window_max([-v for v in values], k)]


def main() -> None:
    data = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"max k=3 -> {sliding_window_max(data, 3)}")
    print(f"min k=3 -> {sliding_window_min(data, 3)}")
    print(f"k=1     -> {sliding_window_max(data, 1)}")
    print(f"k=len   -> {sliding_window_max(data, len(data))}")
    # The naive version is O(n*k) — same answer, quadratic cost.
    naive = [max(data[i:i + 3]) for i in range(len(data) - 2)]
    print(f"naive matches: {naive == sliding_window_max(data, 3)}")


if __name__ == "__main__":
    main()
