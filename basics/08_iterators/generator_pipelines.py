"""Generator pipelines: chaining lazy steps so data flows one item at a time.

A *generator expression* looks like a list comprehension with round brackets:
`(n * n for n in numbers)`. Instead of building the whole list, it produces
each value only when asked for it.

Chain several of them, each reading from the one before, and you get a
*pipeline*. Nothing runs until the last step asks for a value; then a single
item travels through every step before the next item is read. So memory use
stays small and flat, however much data passes through, and a pipeline can
even read from an endless source as long as something stops it.

basics/08_iterators/generators.py introduces `yield`. This file is about
connecting generators together. advanced/lazy_evaluation_pipelines.py goes
further.
"""


def genexp_demo() -> None:
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]

    squares_list = [n * n for n in numbers]  # built now, all at once
    squares_gen = (n * n for n in numbers)  # built later, one at a time
    print(f"list comprehension: {squares_list}")
    print(f"generator expression: {type(squares_gen).__name__} object")
    print(f"next() -> {next(squares_gen)}, next() -> {next(squares_gen)}")

    # As the only argument to a function, the extra brackets can be dropped.
    print(f"sum of squares = {sum(n * n for n in numbers)}")
    print(f"any above 8?   = {any(n > 8 for n in numbers)}")
    print(f"longest word   = {max(len(w) for w in ['fig', 'banana', 'kiwi'])}")

    # A generator is used up after one pass; it does not restart.
    evens = (n for n in numbers if n % 2 == 0)
    print(f"first pass:  {list(evens)}")
    print(f"second pass: {list(evens)}   <- already exhausted")


def main() -> None:
    genexp_demo()


if __name__ == "__main__":
    main()
