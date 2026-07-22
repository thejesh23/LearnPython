"""`while` — loop until a condition goes false.

Use `for` when you know what you are iterating over; use `while` when the
number of iterations depends on something computed inside the loop.

Python has no `do ... while`. The idiom is `while True:` with a `break` at the
point where the exit test naturally belongs — which is often clearer anyway,
because the test sits next to the code that produces the value it tests.
"""


def main() -> None:
    # Countdown: the condition is checked before every iteration.
    n = 5
    while n > 0:
        print(f"n = {n}")
        n -= 1
    print("liftoff")

    # Collatz: the iteration count is not knowable up front.
    value, steps = 27, 0
    while value != 1:
        value = value // 2 if value % 2 == 0 else 3 * value + 1
        steps += 1
    print(f"27 reaches 1 in {steps} Collatz steps")

    # The do-while replacement: run the body once, then decide.
    inputs = iter(["", "  ", "hello"])
    while True:
        line = next(inputs, None)
        if line is None or line.strip():
            break
    print(f"first non-blank line: {line!r}")

    # Newton's method: loop until the answer stops improving.
    target = 2.0
    guess = 1.0
    while abs(guess * guess - target) > 1e-12:
        guess = (guess + target / guess) / 2
    print(f"sqrt(2) ~= {guess:.12f}")

    # Forgetting to advance the state is the classic infinite loop:
    #     while n > 0:
    #         print(n)      # n never changes -> runs forever
    # Always make sure the body moves the condition toward False.


if __name__ == "__main__":
    main()
