"""Everyday dict patterns beyond the basics.

basics/07_collections/dict_basics.py covers creating a dict, `get`,
`setdefault`, `pop` and comprehensions. This file collects the patterns that
come next, once dicts are holding real data:

    views          keys(), values() and items() are live windows, and
                   keys() and items() support set operations
    order          dicts remember insertion order; know what moves an entry
    merging        `|` builds a merged copy, `|=` updates in place,
                   and the right-hand side wins on clashes
    reshaping      counting, inverting and grouping without losing data
    nesting        dicts of dicts for structured records and settings
"""


def views_demo() -> None:
    stock = {"apples": 5, "pears": 0}
    keys = stock.keys()
    print(f"keys view: {keys}")
    stock["plums"] = 7  # the view was not copied, so it sees the change
    print(f"after adding plums: {keys}")

    # keys() and items() behave like sets: compare two dicts in one line.
    old = {"host": "localhost", "port": 8000, "debug": True}
    new = {"host": "localhost", "port": 9000, "workers": 4}
    print(f"added keys:   {new.keys() - old.keys()}")
    print(f"removed keys: {old.keys() - new.keys()}")
    print(f"shared keys:  {sorted(old.keys() & new.keys())}")
    print(f"new or changed pairs: {sorted(new.items() - old.items())}")

    # Changing a dict's size while looping over it is an error...
    attempt = dict(stock)
    try:
        for name in attempt:
            if attempt[name] == 0:
                del attempt[name]
    except RuntimeError as exc:
        print(f"RuntimeError: {exc}")
    # ...so loop over a snapshot copy instead.
    for name in list(stock):
        if stock[name] == 0:
            del stock[name]
    print(f"out of stock removed: {stock}")


def order_demo() -> None:
    queue = {"ada": 1, "alan": 2, "grace": 3}

    # Updating an existing key keeps its place in the order.
    queue["ada"] = 10
    print(f"after update:  {list(queue)}")

    # Removing and re-adding moves the key to the end.
    queue["ada"] = queue.pop("ada")
    print(f"after re-add:  {list(queue)}")

    # popitem() removes the most recently added entry (last in, first out).
    print(f"popitem() -> {queue.popitem()}, left {queue}")

    # First and last keys, without building a list.
    print(f"first key = {next(iter(queue))}, last key = {next(reversed(queue))}")

    # Order is remembered but not compared: equality ignores it.
    x = {"a": 1, "b": 2}
    y = {"b": 2, "a": 1}
    print(f"{x} == {y} -> {x == y}")


DEFAULTS = {"theme": "light", "font_size": 12, "autosave": True}


def merge_demo() -> None:
    user = {"font_size": 14, "theme": "dark"}

    # d1 | d2 makes a new dict. On a clash, the right-hand value wins, so put
    # the defaults on the left and the overrides on the right.
    settings = DEFAULTS | user
    print(f"DEFAULTS | user = {settings}")
    print(f"DEFAULTS unchanged: {DEFAULTS}")

    # |= updates the left dict in place, like .update().
    settings |= {"autosave": False}
    print(f"after |=:         {settings}")

    # Unpacking does the same as | and also works for more than two dicts.
    cli = {"theme": "contrast"}
    print(f"three dicts unpacked: { {**DEFAULTS, **user, **cli} }")

    # The merge is shallow: nested dicts are replaced, not combined.
    a = {"db": {"host": "x", "port": 1}}
    b = {"db": {"port": 2}}
    print(f"shallow merge loses host: {a | b}")


def main() -> None:
    views_demo()
    print()
    order_demo()
    print()
    merge_demo()


if __name__ == "__main__":
    main()
