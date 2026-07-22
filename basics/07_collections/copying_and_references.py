"""References, shallow copies, and deep copies.

Assignment never copies. `b = a` makes a second name for the *same* object, so
mutating through either name is visible through both. This is the source of
most "why did my other list change?" bugs.

A shallow copy (`list(a)`, `a[:]`, `a.copy()`, `dict(d)`) builds a new outer
container holding the *same inner objects*. A deep copy
(`copy.deepcopy`) rebuilds the whole tree.
"""

import copy


def main() -> None:
    a = [1, 2, 3]
    b = a  # not a copy — another name
    b.append(4)
    print(f"a = {a}, b = {b}, same object: {a is b}")

    shallow = a[:]  # or list(a) / a.copy()
    shallow.append(5)
    print(f"after shallow copy + append: a = {a}, shallow = {shallow}")

    # Shallow copies share the *inner* objects.
    nested = [[1, 2], [3, 4]]
    outer_copy = nested[:]
    outer_copy[0].append(99)
    print(f"nested    = {nested}")
    print(f"outer_copy= {outer_copy}   <- the inner list is shared")

    deep = copy.deepcopy(nested)
    deep[0].append(1000)
    print(f"after deepcopy + append: nested = {nested}, deep = {deep}")

    # The same applies to function arguments: they are passed by reference.
    def append_bang(items: list[str]) -> None:
        items.append("!")  # mutates the caller's list

    def rebind(items: list[str]) -> None:
        items = items + ["?"]  # rebinds a local name only

    words = ["hi"]
    append_bang(words)
    rebind(words)
    print(f"after append_bang and rebind: {words}")

    # Immutable values sidestep the whole issue — nothing can mutate them.
    t = (1, 2)
    u = t
    print(f"tuples: t is u -> {t is u}, and neither can be changed")

    print("rule of thumb: copy at the boundary, or hand out immutable values")


if __name__ == "__main__":
    main()
