"""`lambda` — a small anonymous function, limited to a single expression.

`lambda x: x * 2` is exactly `def f(x): return x * 2` without the name. The
body must be one expression: no statements, no assignments, no `if`/`return`
blocks (though the conditional *expression* `a if c else b` is allowed).

Lambdas earn their place as throwaway `key=` functions. If you find yourself
naming one (`f = lambda x: ...`), write a `def` instead — you get a real name
in tracebacks for free.
"""

from functools import reduce


def main() -> None:
    double = lambda x: x * 2  # noqa: E731 — shown for contrast; prefer def
    print(f"double(21) = {double(21)}")
    print(f"double.__name__ = {double.__name__}  <- unhelpful in a traceback")

    people = [("Ada", 36), ("Grace", 45), ("Alan", 41)]

    # The canonical use: a sort key.
    print(f"by age  -> {sorted(people, key=lambda p: p[1])}")
    print(f"by name -> {sorted(people, key=lambda p: p[0])}")
    print(f"by name length, then name -> {sorted(people, key=lambda p: (len(p[0]), p[0]))}")

    # With the functional built-ins. A comprehension is usually clearer.
    nums = [1, 2, 3, 4, 5, 6]
    print(f"map    -> {list(map(lambda n: n * n, nums))}")
    print(f"filter -> {list(filter(lambda n: n % 2 == 0, nums))}")
    print(f"reduce -> {reduce(lambda a, b: a * b, nums)}")
    print(f"comprehension equivalent -> {[n * n for n in nums if n % 2 == 0]}")

    # A conditional expression is fine; statements are not.
    sign = lambda n: "neg" if n < 0 else "zero" if n == 0 else "pos"  # noqa: E731
    print([sign(n) for n in (-2, 0, 5)])

    # Late binding: a lambda looks its free variables up when *called*.
    bad = [lambda: i for i in range(3)]
    print(f"late binding -> {[f() for f in bad]}  (all 2)")
    good = [lambda i=i: i for i in range(3)]
    print(f"bound via default -> {[f() for f in good]}")


if __name__ == "__main__":
    main()
