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


def main() -> None:
    views_demo()


if __name__ == "__main__":
    main()
