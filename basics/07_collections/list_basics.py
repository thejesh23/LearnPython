"""`list` — an ordered, mutable, growable sequence.

A Python list is an array of references, so it can hold mixed types and it
indexes in O(1). Appending is amortised O(1); inserting or deleting near the
front is O(n) because everything after it shifts.

Sorting is in place with `.sort()` and returns a new list with `sorted()`.
Both are stable: equal elements keep their original order.
"""


def main() -> None:
    xs = [3, 1, 4, 1, 5]
    print(f"xs = {xs}, len = {len(xs)}, xs[0] = {xs[0]}, xs[-1] = {xs[-1]}")

    xs.append(9)
    xs.insert(0, 0)
    xs.extend([2, 6])
    print(f"after append/insert/extend: {xs}")

    xs.remove(1)  # removes the *first* 1 only
    popped = xs.pop()  # from the end by default
    print(f"after remove(1) and pop(): {xs}, popped {popped}")

    print(f"count(1) = {xs.count(1)}, index(4) = {xs.index(4)}")
    print(f"5 in xs -> {5 in xs}")

    # sort mutates; sorted returns a new list.
    xs.sort()
    print(f"sorted in place: {xs}")
    print(f"sorted(reverse=True): {sorted(xs, reverse=True)}")
    print(f"original untouched by sorted(): {xs}")

    # Lists are heterogeneous — they hold references to anything.
    mixed = [1, "two", 3.0, [4], {"five": 5}, None]
    print(f"mixed = {mixed}")

    # Cost model worth remembering.
    print("append/pop at end: O(1) amortised; insert/pop(0): O(n)")
    print("membership `in`: O(n) — use a set for repeated lookups")

    # A list holds references, so nesting with * repeats the same object.
    grid_wrong = [[0] * 3] * 2
    grid_wrong[0][0] = 9
    print(f"[[0]*3]*2 after one write: {grid_wrong}  <- both rows changed")
    grid_right = [[0] * 3 for _ in range(2)]
    grid_right[0][0] = 9
    print(f"comprehension version:      {grid_right}")


if __name__ == "__main__":
    main()
