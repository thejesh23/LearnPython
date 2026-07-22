"""Project Euler 2: sum of the even Fibonacci numbers below four million.

The direct approach generates the sequence and filters. The observation worth
having is that the parity pattern is odd, odd, even, repeating forever — every
third Fibonacci number is even. So you can generate only those, using the
recurrence E(n) = 4*E(n-1) + E(n-2), and do a third of the work.

Answer: 4613732.
"""

from collections.abc import Iterator


def fibonacci_below(limit: int) -> Iterator[int]:
    a, b = 1, 2
    while a < limit:
        yield a
        a, b = b, a + b


def sum_even_filtered(limit: int) -> int:
    return sum(n for n in fibonacci_below(limit) if n % 2 == 0)


def sum_even_direct(limit: int) -> int:
    """Generate only the even terms: E(n) = 4*E(n-1) + E(n-2)."""
    total = 0
    prev, curr = 0, 2  # the first two even Fibonacci numbers
    while curr < limit:
        total += curr
        prev, curr = curr, 4 * curr + prev
    return total


def main() -> None:
    print(f"filtered: {sum_even_filtered(4_000_000)}")
    print(f"direct:   {sum_even_direct(4_000_000)}")
    print(f"agree across limits: "
          f"{all(sum_even_filtered(n) == sum_even_direct(n) for n in range(1, 500))}")

    print(f"first ten Fibonacci terms: {[n for n in fibonacci_below(100)]}")
    print("parity runs odd, odd, even — so every third term is even")
    print(f"even terms below 100: {[n for n in fibonacci_below(100) if n % 2 == 0]}")

    print(f"below 2: {sum_even_direct(2)}")
    print(f"below 10**30: {sum_even_direct(10**30)}")


if __name__ == "__main__":
    main()
