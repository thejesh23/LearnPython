"""`unittest` — Python's built-in test framework.

A test is a method whose name starts with `test_` on a class that inherits
from `unittest.TestCase`. Inside, the `assert...` methods check results and,
when one fails, report both the expected and the actual value.

In a real project the tests live in their own files (test_*.py) and run with
`python -m unittest`. Here the code and its tests share a file, and each demo
runs one test class so you can see what passing and failing look like.
Third-party pytest is popular too, and can run these same TestCase classes.
"""

import sys
import unittest


class Stack:
    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, item: int) -> None:
        self._items.append(item)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


def run(case: type[unittest.TestCase]) -> unittest.TestResult:
    """Run one TestCase class and print the report to standard output."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(case)
    return unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)


class StackBasics(unittest.TestCase):
    def test_push_then_pop_returns_last_item(self) -> None:
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)

    def test_len_counts_items(self) -> None:
        s = Stack()
        s.push(5)
        self.assertEqual(len(s), 1)
        self.assertTrue(s)  # a non-empty container is truthy


def first_tests_demo() -> None:
    run(StackBasics)


def main() -> None:
    first_tests_demo()


if __name__ == "__main__":
    main()
