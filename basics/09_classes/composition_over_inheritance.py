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

from collections.abc import Callable


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


class EmailNotifier:
    def notify(self, text: str) -> str:
        return f"email: {text}"


class SmsNotifier:
    def notify(self, text: str) -> str:
        return f"sms: {text}"


class ShoutingEmailNotifier(EmailNotifier):
    def notify(self, text: str) -> str:
        return super().notify(text.upper() + "!")


class ShoutingSmsNotifier(SmsNotifier):
    # The same shouting logic, written a second time. Add a third channel and
    # a third style and you need nine classes.
    def notify(self, text: str) -> str:
        return super().notify(text.upper() + "!")


def class_explosion_demo() -> None:
    notifiers = [
        EmailNotifier(),
        SmsNotifier(),
        ShoutingEmailNotifier(),
        ShoutingSmsNotifier(),
    ]
    for n in notifiers:
        print(f"{type(n).__name__:22} -> {n.notify('build passed')}")
    print(f"{len(notifiers)} classes for 2 channels x 2 styles")


def plain(text: str) -> str:
    return text


def shouting(text: str) -> str:
    return text.upper() + "!"


class EmailSender:
    def send(self, message: str) -> str:
        return f"email: {message}"


class SmsSender:
    def send(self, message: str) -> str:
        return f"sms: {message}"


class Notifier:
    """Has a formatter and has a sender; delegates the work to each."""

    def __init__(
        self, sender: EmailSender | SmsSender, style: Callable[[str], str] = plain
    ) -> None:
        self.sender = sender
        self.style = style

    def notify(self, text: str) -> str:
        return self.sender.send(self.style(text))


def composed_demo() -> None:
    # Every combination comes from one class plus small parts. A new channel
    # or a new style is one new part, not a new row of subclasses.
    for sender in (EmailSender(), SmsSender()):
        for style in (plain, shouting):
            n = Notifier(sender, style)
            print(f"{type(sender).__name__:11} + {style.__name__:8} -> "
                  f"{n.notify('build passed')}")


class RecordingSender:
    """A fake part for tests: remembers messages instead of sending them."""

    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, message: str) -> str:
        self.sent.append(message)
        return f"recorded: {message}"


def swap_parts_demo() -> None:
    n = Notifier(EmailSender())
    print(n.notify("deploy started"))

    # Change behaviour on a live object by replacing one part.
    n.style = shouting
    print(n.notify("deploy failed"))

    # Swap in a fake sender: no subclassing, no patching needed.
    fake = RecordingSender()
    n.sender = fake  # type: ignore[assignment]
    n.notify("hello")
    n.notify("bye")
    print(f"the fake captured: {fake.sent}")


def main() -> None:
    is_a_vs_has_a_demo()
    print()
    class_explosion_demo()
    print()
    composed_demo()
    print()
    swap_parts_demo()


if __name__ == "__main__":
    main()
