"""Run every solved problem, then self-check: python3 -m project_euler.euler_kit"""

import math
import random
import sys

from . import (
    PROBLEMS,
    collatz_length,
    collatz_sequence,
    fibonacci_below,
    is_prime,
    nth_prime,
    prime_factors,
    primes_below,
    run_all,
    sum_multiples,
)

# The worked examples printed in each problem statement: (arguments, answer).
STATEMENT_EXAMPLES = {1: ((10,), 23), 2: ((100,), 44), 3: ((13195,), 29),
                      7: ((6,), 13), 10: ((10,), 17), 14: ((10,), 9)}


def examples() -> None:
    print("1. every solved problem against its known answer:")
    for r in run_all():
        status = "ok" if r.ok else f"WRONG (expected {r.problem.answer})"
        p = r.problem
        print(f"   #{p.number:<3} {p.title:<26} {r.value:>14}  {status} ({r.seconds * 1000:.1f} ms)")
    small = {n: PROBLEMS[n].solve(*args) for n, (args, _) in STATEMENT_EXAMPLES.items()}
    print("2. the worked examples from the problem statements:", small)
    print("3. primes below 40:", primes_below(40), "| 1000th prime:", nth_prime(1000))
    print("4. 360 =", " * ".join(map(str, prime_factors(360))), "| 13195 =", prime_factors(13195))
    print("5. Collatz from 13:", collatz_sequence(13), "| 27 takes", collatz_length(27), "terms")
    print("6. Fibonacci below 100:", list(fibonacci_below(100)), "| every third is even")
    print("7. closed form beats a loop: multiples of 3 below 10**18 sum to", sum_multiples(3, 10**18))


def even_fibonacci_sum(limit: int) -> int:
    """Independent check for #2: every third term is even, E(n) = 4E(n-1) + E(n-2)."""
    total, prev, cur = 0, 0, 2
    while cur < limit:
        total, prev, cur = total + cur, cur, 4 * cur + prev
    return total


def self_check() -> None:
    results = run_all()
    assert results and all(r.ok for r in results), [r for r in results if not r.ok]
    for number, (args, answer) in STATEMENT_EXAMPLES.items():
        assert PROBLEMS[number].solve(*args) == answer, number
    rng = random.Random(2024)
    assert primes_below(3000) == [n for n in range(3000) if n > 1 and all(n % d for d in range(2, n))]
    for _ in range(300):
        n = rng.randint(1, 10**7)
        factors = prime_factors(n)
        assert math.prod(factors) == n and factors == sorted(factors) and all(map(is_prime, factors)), n
        assert is_prime(n) == (factors == [n] and n > 1), n
        k, limit = rng.randint(1, 50), rng.randint(0, 5000)
        assert sum_multiples(k, limit) == sum(range(k, limit, k)), (k, limit)
        assert PROBLEMS[1].solve(limit) == sum(x for x in range(limit) if x % 3 == 0 or x % 5 == 0)
        limit = rng.randint(1, 10**12)
        assert PROBLEMS[2].solve(limit) == even_fibonacci_sum(limit), limit
    cache: dict[int, int] = {}
    for n in rng.sample(range(1, 100_000), 300):
        assert collatz_length(n, cache) == len(collatz_sequence(n)), n
    assert [nth_prime(i) for i in range(1, 200)] == primes_below(1300)[:199]


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
