"""Activity selection: the most non-overlapping activities from a set.

Each activity has a start and a finish time, and two activities conflict if
their intervals overlap. The greedy rule is to sort by finish time and
repeatedly take the first activity that starts at or after the last one taken.

Why earliest finish time is optimal, as an exchange argument: let g be the
activity with the earliest finish among all of them, and let S be any optimal
selection. If S already contains g there is nothing to prove. Otherwise let a be
the first activity in S by finish time. Since g finishes no later than a, and a
conflicts with nothing later in S, swapping a for g leaves a valid selection of
exactly the same size. So there is always an optimal solution containing g;
remove g and everything conflicting with it, and the argument repeats on the
smaller instance.

Sorting dominates, so the cost is O(n log n) and O(1) extra space. Note the
tempting alternatives — earliest start, or shortest duration — are both wrong,
and the code shows counterexamples for each.
"""

Activity = tuple[str, int, int]  # name, start, finish


def select(activities: list[Activity]) -> list[Activity]:
    chosen: list[Activity] = []
    last_finish = float("-inf")
    for act in sorted(activities, key=lambda a: a[2]):
        if act[1] >= last_finish:  # touching endpoints do not overlap
            chosen.append(act)
            last_finish = act[2]
    return chosen


def select_by_start(activities: list[Activity]) -> list[Activity]:
    chosen: list[Activity] = []
    last_finish = float("-inf")
    for act in sorted(activities, key=lambda a: a[1]):
        if act[1] >= last_finish:
            chosen.append(act)
            last_finish = act[2]
    return chosen


def select_by_duration(activities: list[Activity]) -> list[Activity]:
    chosen: list[Activity] = []
    taken: list[Activity] = []
    for act in sorted(activities, key=lambda a: a[2] - a[1]):
        if all(act[2] <= s or act[1] >= f for _, s, f in taken):
            taken.append(act)
            chosen.append(act)
    return sorted(chosen, key=lambda a: a[1])


def is_compatible(chosen: list[Activity]) -> bool:
    ordered = sorted(chosen, key=lambda a: a[1])
    return all(a[2] <= b[1] for a, b in zip(ordered, ordered[1:]))


def names(chosen: list[Activity]) -> list[str]:
    return [a[0] for a in chosen]


def main() -> None:
    schedule: list[Activity] = [
        ("a1", 1, 4), ("a2", 3, 5), ("a3", 0, 6), ("a4", 5, 7),
        ("a5", 3, 9), ("a6", 5, 9), ("a7", 6, 10), ("a8", 8, 11),
        ("a9", 8, 12), ("a10", 2, 14), ("a11", 12, 16),
    ]
    picked = select(schedule)
    print(f"chosen: {names(picked)}")
    print(f"count: {len(picked)}, compatible: {is_compatible(picked)}")

    # Earliest start fails: one long early activity blocks everything after it.
    trap: list[Activity] = [("long", 0, 10), ("x", 1, 2), ("y", 3, 4), ("z", 5, 6)]
    print(f"\nearliest finish on trap:   {names(select(trap))}")
    print(f"earliest start on trap:    {names(select_by_start(trap))}")

    # Shortest duration fails: a short activity can straddle two longer ones.
    trap2: list[Activity] = [("p", 0, 5), ("q", 4, 6), ("r", 5, 10)]
    print(f"\nearliest finish on trap2:  {names(select(trap2))}")
    print(f"shortest duration on trap2:{names(select_by_duration(trap2))}")

    print(f"\nempty input: {select([])}")
    print(f"single: {names(select([('solo', 2, 3)]))}")
    all_overlapping: list[Activity] = [("A", 0, 9), ("B", 1, 8), ("C", 2, 7)]
    print(f"all overlapping: {names(select(all_overlapping))}")
    back_to_back: list[Activity] = [("A", 0, 1), ("B", 1, 2), ("C", 2, 3)]
    print(f"back to back: {names(select(back_to_back))}")


if __name__ == "__main__":
    main()
