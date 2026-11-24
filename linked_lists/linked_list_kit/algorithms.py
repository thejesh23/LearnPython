"""Classic linked-list algorithms, all by relinking nodes in O(1) extra space
unless noted."""

from .nodes import Node, iter_nodes


def reverse(head: Node | None) -> Node | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def reverse_in_groups(head: Node | None, k: int) -> Node | None:
    """Reverse each full block of k nodes; a short tail block stays as it is."""
    if k < 1:
        raise ValueError("k must be at least 1")
    dummy = Node(0, head)
    before = dummy
    while True:
        probe = before
        for _ in range(k):
            probe = probe.next
            if probe is None:
                return dummy.next
        first, after = before.next, probe.next
        prev, node = after, first
        while node is not after:
            node.next, prev, node = prev, node, node.next  # type: ignore[union-attr]
        before.next = prev
        before = first  # type: ignore[assignment]


def middle(head: Node | None) -> Node | None:
    """Tortoise and hare: the second middle for even lengths."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next  # type: ignore[union-attr]
    return slow


def merge_sorted(a: Node | None, b: Node | None) -> Node | None:
    """Stable merge of two sorted lists."""
    dummy = tail = Node(0)
    while a and b:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k(lists: list[Node | None]) -> Node | None:
    """Pairwise rounds: O(N log k) like a heap, with no extra structure."""
    if not lists:
        return None
    while len(lists) > 1:
        merged = [merge_sorted(lists[i], lists[i + 1])
                  for i in range(0, len(lists) - 1, 2)]
        if len(lists) % 2:
            merged.append(lists[-1])
        lists = merged
    return lists[0]


def is_palindrome(head: Node | None) -> bool:
    """Reverse the back half, compare, then restore the caller's list."""
    if head is None or head.next is None:
        return True
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next  # type: ignore[assignment]
    back = reverse(slow.next)
    left, right, same = head, back, True
    while right:
        if left.value != right.value:  # type: ignore[union-attr]
            same = False
            break
        left, right = left.next, right.next  # type: ignore[union-attr]
    slow.next = reverse(back)
    return same


def add_numbers(a: Node | None, b: Node | None) -> Node | None:
    """Digits stored least-significant first: 2->4->3 + 5->6->4 = 7->0->8."""
    dummy = tail = Node(0)
    carry = 0
    while a or b or carry:
        carry, digit = divmod(carry + (a.value if a else 0) + (b.value if b else 0), 10)
        tail.next = Node(digit)
        tail = tail.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next


def find_cycle(head: Node | None) -> tuple[Node, int] | None:
    """Floyd: (entry node, loop length), or None for a list that ends."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next  # type: ignore[union-attr]
        if slow is fast:
            break
    else:
        return None
    probe = head
    while probe is not slow:
        probe, slow = probe.next, slow.next  # type: ignore[union-attr]
    length, node = 1, probe.next  # type: ignore[union-attr]
    while node is not probe:
        length, node = length + 1, node.next  # type: ignore[union-attr]
    return probe, length  # type: ignore[return-value]


def length(head: Node | None) -> int:
    return sum(1 for _ in iter_nodes(head))
