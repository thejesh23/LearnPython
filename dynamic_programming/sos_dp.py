"""Sum over subsets (SOS) DP: aggregate a function over every submask fast.

Given a value f[mask] for each of the 2**n bitmasks, we often want
g[mask] = sum of f[sub] over all submasks sub of mask. Done naively by iterating
each mask's submasks the cost is O(3**n), because summing over all (mask, sub)
pairs with sub a submask of mask is the sum of 2**popcount, which is 3**n.

SOS DP does it in O(n * 2**n) with a clever per-bit relaxation. Process bits one
at a time. After processing bit b, g[mask] holds the sum over exactly those
submasks that agree with mask on all bits above b. To advance, for every mask
whose bit b is set, add g[mask without bit b]: this folds in the submasks that
turn bit b off. Sweeping all n bits leaves the full subset sum.

The same skeleton computes sum over supersets by flipping which masks absorb
their neighbour. This file builds the subset transform and verifies it exactly
against the O(3**n) definition.

Complexity: O(n * 2**n) time, O(2**n) space.
"""


def sum_over_subsets(f: list[int]) -> list[int]:
    """g[mask] = sum of f[sub] for every submask sub of mask."""
    size = len(f)
    n = size.bit_length() - 1  # size must be a power of two, 2**n
    assert size == 1 << n, "input length must be a power of two"
    g = list(f)
    for bit in range(n):
        for mask in range(size):
            if mask & (1 << bit):
                g[mask] += g[mask ^ (1 << bit)]
    return g


def sum_over_supersets(f: list[int]) -> list[int]:
    """h[mask] = sum of f[sup] for every superset sup of mask."""
    size = len(f)
    n = size.bit_length() - 1
    h = list(f)
    for bit in range(n):
        for mask in range(size):
            if not (mask & (1 << bit)):
                h[mask] += h[mask ^ (1 << bit)]
    return h


def naive_subset_sum(f: list[int]) -> list[int]:
    """Reference O(3**n): enumerate each mask's submasks directly."""
    size = len(f)
    g = [0] * size
    for mask in range(size):
        sub = mask
        while True:
            g[mask] += f[sub]
            if sub == 0:
                break
            sub = (sub - 1) & mask
    return g


def naive_superset_sum(f: list[int]) -> list[int]:
    size = len(f)
    h = [0] * size
    for mask in range(size):
        for sup in range(size):
            if sup & mask == mask:
                h[mask] += f[sup]
    return h


def main() -> None:
    f = [3, 1, 4, 1, 5, 9, 2, 6]  # n = 3, eight masks
    g = sum_over_subsets(f)
    print(f"f            = {f}")
    print(f"subset sums  = {g}")
    print(f"  g[0b111] should be sum(f) = {sum(f)}: {g[0b111]}")
    print(f"  g[0b101] = f[000]+f[001]+f[100]+f[101] "
          f"= {f[0]+f[1]+f[4]+f[5]}: {g[0b101]}")
    assert g == naive_subset_sum(f)

    h = sum_over_supersets(f)
    print(f"superset sums= {h}")
    assert h == naive_superset_sum(f)

    import random
    random.seed(1)
    for n in range(1, 8):
        data = [random.randint(-9, 9) for _ in range(1 << n)]
        assert sum_over_subsets(data) == naive_subset_sum(data)
        assert sum_over_supersets(data) == naive_superset_sum(data)
    print("random cross-checks n=1..7: SOS == naive O(3**n)")

    print("\nedge cases:")
    print("  n=0 single element:", sum_over_subsets([7]))


if __name__ == "__main__":
    main()
