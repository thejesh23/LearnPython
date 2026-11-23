"""Greedy scheduling: earliest finish, earliest free room, furthest reach.

Each function sorts or sweeps once and never revisits a decision; the comment
on each says why the local choice is safe.
"""

import heapq
from collections.abc import Sequence

Interval = tuple[str, int, int]  # name, start, end; touching endpoints do not overlap


def select_activities(activities: Sequence[Interval]) -> list[Interval]:
    """A largest set of non-overlapping activities: always take the earliest finish.

    Exchange argument: any optimal schedule's first activity can be swapped for
    the earliest-finishing one without causing a clash.
    """
    chosen: list[Interval] = []
    free_at = float("-inf")
    for act in sorted(activities, key=lambda a: a[2]):
        if act[1] >= free_at:
            chosen.append(act)
            free_at = act[2]
    return chosen


def assign_rooms(meetings: Sequence[Interval]) -> dict[int, list[Interval]]:
    """Fewest rooms for all meetings, as room number -> meetings in start order.

    Meetings go in by start time; each reuses the room that frees up earliest
    if it is already free, else opens a new room. A heap holds (end, room).
    """
    free: list[tuple[int, int]] = []
    rooms: dict[int, list[Interval]] = {}
    for meeting in sorted(meetings, key=lambda m: m[1]):
        if free and free[0][0] <= meeting[1]:
            _, room = heapq.heappop(free)
        else:
            room = len(rooms)
        rooms.setdefault(room, []).append(meeting)
        heapq.heappush(free, (meeting[2], room))
    return rooms


def min_rooms(meetings: Sequence[Interval]) -> int:
    """Peak number of meetings running at once (= rooms needed)."""
    return len(assign_rooms(meetings))


def min_jumps(nums: Sequence[int]) -> int | None:
    """Fewest jumps from index 0 to the last index (nums[i] = max jump), or None.

    A BFS by levels without a queue: ``window_end`` is the furthest index
    reachable with ``jumps`` jumps, ``furthest`` the furthest with one more.
    """
    jumps = window_end = furthest = 0
    for i in range(len(nums) - 1):
        if i > furthest:
            return None  # a gap nothing earlier can clear
        furthest = max(furthest, i + nums[i])
        if i == window_end:
            jumps += 1
            window_end = furthest
    return jumps if furthest >= len(nums) - 1 else None
