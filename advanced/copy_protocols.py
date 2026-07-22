"""Controlling how your objects are copied: `__copy__` and `__deepcopy__`.

`copy.copy` makes a shallow copy — a new outer object sharing the inner ones.
`copy.deepcopy` rebuilds the whole graph, and it correctly handles cycles by
keeping a memo dict of everything already copied.

Define `__copy__`/`__deepcopy__` when the default is wrong: a cached
connection that must not be duplicated, a lock that must be fresh, an id that
must be regenerated. `__deepcopy__` must pass the memo down, or shared
substructure becomes duplicated and cycles recurse forever.
"""

import copy


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.links: list["Node"] = []

    def __repr__(self) -> str:
        return f"Node({self.name})"


class Document:
    """A cache that must not be shared, and a body that must be."""

    def __init__(self, title: str, tags: list[str]) -> None:
        self.title = title
        self.tags = tags
        self._render_cache: dict[str, str] = {}

    def __copy__(self) -> "Document":
        clone = Document(self.title, self.tags)  # tags deliberately shared
        return clone

    def __deepcopy__(self, memo: dict) -> "Document":
        clone = Document(self.title, copy.deepcopy(self.tags, memo))
        memo[id(self)] = clone  # register before recursing, for cycles
        return clone  # cache intentionally dropped

    def __repr__(self) -> str:
        return f"Document({self.title!r}, tags={self.tags}, cached={len(self._render_cache)})"


def main() -> None:
    original = [[1, 2], [3, 4]]
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    shallow[0].append(99)
    print(f"after mutating shallow[0]: original={original}")
    print(f"deep is unaffected: {deep}")

    print("cycles:")
    a, b = Node("a"), Node("b")
    a.links.append(b)
    b.links.append(a)  # cycle
    clone = copy.deepcopy(a)
    print(f"  copied cycle terminates: {clone} -> {clone.links[0]} -> {clone.links[0].links[0]}")
    print(f"  and it is a real copy: {clone is not a}, "
          f"cycle preserved: {clone.links[0].links[0] is clone}")

    print("custom hooks:")
    doc = Document("Report", ["draft"])
    doc._render_cache["html"] = "<p>...</p>"
    shallow_doc = copy.copy(doc)
    deep_doc = copy.deepcopy(doc)
    print(f"  original: {doc}")
    print(f"  shallow:  {shallow_doc}  (cache dropped, tags shared: "
          f"{shallow_doc.tags is doc.tags})")
    print(f"  deep:     {deep_doc}  (tags copied: {deep_doc.tags is not doc.tags})")

    print("shared substructure is preserved by the memo:")
    inner = [1, 2]
    outer = [inner, inner]
    copied = copy.deepcopy(outer)
    print(f"  both entries still the same object: {copied[0] is copied[1]}")

    print("immutable objects are returned as-is:")
    t = (1, 2, 3)
    print(f"  deepcopy(tuple) is the same object: {copy.deepcopy(t) is t}")
    print("  slicing, list(), and dict() are shallow copies too")


if __name__ == "__main__":
    main()
