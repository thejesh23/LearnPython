"""Jump game: reachability and fewest jumps by tracking the furthest reach.

Each entry of the array says the maximum jump length from that index. The
question "can the last index be reached" needs no search at all: sweep left to
right keeping the furthest index reachable so far, and if the sweep ever stands
on an index beyond that reach, the array is cut in two and the answer is no.
One pass, O(n) time, O(1) space.

Counting the minimum number of jumps uses the same reach but in levels. Think
of it as breadth-first search where level k is every index reachable in k jumps.
Those indices form a contiguous window, so instead of a queue you only need the
window's right edge. Scan forward; while inside the current window keep
extending the next window's edge; when the scan reaches the current edge, that
is a jump, and the next window becomes current.

The greedy choice is optimal because taking the furthest reach at each level can
never leave you worse off: every index the alternatives could reach is inside
the window the furthest reach gives you.
"""


def can_reach_end(nums: list[int]) -> bool:
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:
            return False  # a gap no earlier index could clear
        reach = max(reach, i + jump)
    return True


def min_jumps(nums: list[int]) -> int | None:
    """Fewest jumps to the last index, or None if it is unreachable."""
    if len(nums) <= 1:
        return 0
    jumps = 0
    current_end = 0   # right edge of the window reachable in `jumps` jumps
    furthest = 0      # right edge of the next window
    for i in range(len(nums) - 1):
        if i > furthest:
            return None
        furthest = max(furthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = furthest
            if current_end >= len(nums) - 1:
                return jumps
    return jumps if furthest >= len(nums) - 1 else None


def jump_path(nums: list[int]) -> list[int] | None:
    """The indices of one optimal jump sequence, for inspection."""
    if len(nums) <= 1:
        return [0] if nums else []
    path = [0]
    i = 0
    while i < len(nums) - 1:
        if nums[i] == 0:
            return None
        if i + nums[i] >= len(nums) - 1:
            path.append(len(nums) - 1)
            return path
        # Among the landing spots, take the one whose own reach goes furthest.
        best = max(range(i + 1, i + nums[i] + 1), key=lambda j: j + nums[j])
        path.append(best)
        i = best
    return path


def main() -> None:
    cases = [
        [2, 3, 1, 1, 4],
        [3, 2, 1, 0, 4],
        [0],
        [],
        [1, 2],
        [2, 0, 0],
        [1, 0, 1],
        [5, 0, 0, 0, 0, 0],
    ]
    for nums in cases:
        print(f"{str(nums):<22} reachable={can_reach_end(nums)!s:<5} "
              f"min_jumps={min_jumps(nums)} path={jump_path(nums)}")

    # A worst case for jump counting: every step advances exactly one index.
    ones = [1] * 1000
    print(f"\n[1]*1000: min_jumps={min_jumps(ones)}")
    big = [1000] + [0] * 999
    print(f"one big jump over 999 zeros: min_jumps={min_jumps(big)}")
    blocked = [1] * 500 + [0] + [1] * 499
    print(f"blocked in the middle: reachable={can_reach_end(blocked)}, "
          f"min_jumps={min_jumps(blocked)}")


if __name__ == "__main__":
    main()
