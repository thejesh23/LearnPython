"""Composition over inheritance — build objects from parts instead of parents.

Inheritance says "is-a": a Dog *is an* Animal, and gets every method Animal
has. Composition says "has-a": a Car *has an* Engine, keeps it in an
attribute, and calls it when needed (this forwarding is called *delegation*).

Inheritance is the right tool when the subclass truly is a special case of the
parent and should support everything the parent does. Reach for composition
when you only want *some* of another class's behaviour, when you need to mix
and match several behaviours, or when you want to swap a part out later (in a
test, or at runtime). The usual symptom that inheritance was the wrong choice
is a pile of subclasses named after combinations: ShoutingEmailNotifier,
QuietSmsNotifier, and so on.
"""


class ListStack(list):
    """Is-a: inherits *every* list method, wanted or not."""

    def push(self, item: str) -> None:
        self.append(item)


class Stack:
    """Has-a: keeps a list inside and exposes only stack operations."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


def is_a_vs_has_a_demo() -> None:
    leaky = ListStack()
    leaky.push("a")
    leaky.push("b")
    # Nothing stops a caller from breaking the "last in, first out" rule.
    leaky.insert(0, "z")
    leaky.sort()
    print(f"ListStack after insert + sort: {leaky}")
    print(f"pop() returns {leaky.pop()!r}, which was never pushed on top")

    stack = Stack()
    stack.push("a")
    stack.push("b")
    print(f"Stack has insert? {hasattr(stack, 'insert')}")
    print(f"Stack pops {stack.pop()!r}, {len(stack)} left")


def main() -> None:
    is_a_vs_has_a_demo()


if __name__ == "__main__":
    main()
