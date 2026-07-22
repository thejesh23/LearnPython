"""Jump search: step forward in blocks of sqrt(n), then scan the final block.

Sits between linear and binary search. It needs sorted data like binary search,
but only ever steps *forward*, which matters on media where seeking backwards
is expensive (tape, some linked structures).

The optimal block size is sqrt(n): n/m jumps plus m-1 scans is minimised at
m = sqrt(n), giving O(sqrt(n)).
"""

import math


def jump_search(values: list[int], target: int) -> int:
    n = len(values)
    if n == 0:
        return -1
    step = max(1, int(math.isqrt(n)))

    # Jump until the block that could contain the target.
    prev, curr = 0, step
    while curr < n and values[curr - 1] < target:
        prev, curr = curr, curr + step

    # Linear scan inside the block.
    for i in range(prev, min(curr, n)):
        if values[i] == target:
            return i
    return -1


def main() -> None:
    data = list(range(0, 100, 3))  # 0, 3, 6, ...
    print(f"len = {len(data)}, block size = {math.isqrt(len(data))}")
    print(f"jump_search(21) = {jump_search(data, 21)}  (data[7] = {data[7]})")
    print(f"jump_search(0)  = {jump_search(data, 0)}")
    print(f"jump_search(99) = {jump_search(data, 99)}")
    print(f"jump_search(20) = {jump_search(data, 20)}  (absent)")
    print(f"jump_search on empty = {jump_search([], 1)}")


if __name__ == "__main__":
    main()
