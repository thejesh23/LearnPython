"""Greatest common divisor by Euclid's algorithm, and lcm derived from it.

The key insight is one line: any number dividing both a and b also divides
a - b, and therefore divides a % b. So gcd(a, b) == gcd(b, a % b), and each
step shrinks the pair. Repeat until the second number is 0; the first is then
the answer, because gcd(g, 0) == g.

Because a % b at least halves the larger argument every two steps, the number
of iterations is O(log min(a, b)) — the worst case is consecutive Fibonacci
numbers. Each step is one modulo, so on machine-sized ints the whole thing is
effectively constant time.

Least common multiple follows for free: a * b counts every prime factor once
too often for the shared part, so lcm(a, b) == a // gcd(a, b) * b. Dividing
before multiplying keeps the intermediate value small.
"""

import math


def gcd_iterative(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def gcd_recursive(a: int, b: int) -> int:
    if b == 0:
        return abs(a)
    return gcd_recursive(b, a % b)


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0  # every multiple of 0 is 0, so the smallest common one is 0
    # Divide first: a // g * b never exceeds the answer, a * b // g can be huge.
    return abs(a) // gcd_iterative(a, b) * abs(b)


def gcd_many(values: list[int]) -> int:
    result = 0  # gcd(0, x) == x, so 0 is the correct identity element
    for value in values:
        result = gcd_iterative(result, value)
        if result == 1:
            break  # cannot get any smaller
    return result


def main() -> None:
    print(f"gcd_iterative(48, 18) = {gcd_iterative(48, 18)}")
    print(f"gcd_recursive(48, 18) = {gcd_recursive(48, 18)}")
    print(f"math.gcd(48, 18)      = {math.gcd(48, 18)}")

    print(f"lcm(4, 6)      = {lcm(4, 6)}")
    print(f"math.lcm(4, 6) = {math.lcm(4, 6)}")

    print(f"gcd_many([12, 18, 30]) = {gcd_many([12, 18, 30])}")

    # Edge cases: zero, negatives, coprime pairs, and the Fibonacci worst case.
    print(f"gcd(0, 5)    = {gcd_iterative(0, 5)}")
    print(f"gcd(0, 0)    = {gcd_iterative(0, 0)}")
    print(f"gcd(-12, 18) = {gcd_iterative(-12, 18)}")
    print(f"lcm(0, 7)    = {lcm(0, 7)}")
    print(f"gcd(17, 5)   = {gcd_iterative(17, 5)}")
    print(f"gcd(fib 30, fib 29) = {gcd_iterative(832040, 514229)}")


if __name__ == "__main__":
    main()
