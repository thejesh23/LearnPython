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


def invert(mapping: dict[str, str]) -> dict[str, list[str]]:
    """Swap keys and values, keeping every key that shared a value."""
    result: dict[str, list[str]] = {}
    for key, value in mapping.items():
        result.setdefault(value, []).append(key)
    return result


def reshape_demo() -> None:
    # Counting with get(key, 0): no need to check whether the key exists.
    votes = ["tea", "coffee", "tea", "water", "tea", "coffee"]
    tally: dict[str, int] = {}
    for vote in votes:
        tally[vote] = tally.get(vote, 0) + 1
    print(f"tally = {tally}")

    # A plain inversion silently drops keys when values repeat.
    team = {"ada": "red", "alan": "blue", "grace": "red"}
    naive = {colour: name for name, colour in team.items()}
    print(f"naive invert:  {naive}   <- ada is gone")
    print(f"invert():      {invert(team)}")

    # Grouping records by a field, then summarising each group.
    sales = [("north", 120), ("south", 80), ("north", 45), ("east", 60)]
    by_region: dict[str, list[int]] = {}
    for region, amount in sales:
        by_region.setdefault(region, []).append(amount)
    totals = {region: sum(amounts) for region, amounts in by_region.items()}
    print(f"grouped: {by_region}")
    print(f"totals:  {totals}")
    print(f"best region: {max(totals, key=totals.get)}")


def deep_merge(base: dict, override: dict) -> dict:
    """Merge override into a copy of base, combining nested dicts too."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def nested_demo() -> None:
    config = {
        "server": {"host": "localhost", "port": 8000},
        "database": {"name": "app", "pool": {"min": 1, "max": 5}},
    }

    print(f"config['database']['pool']['max'] = {config['database']['pool']['max']}")

    # A missing level raises KeyError. Chained get() with {} defaults returns
    # None instead, for data where the section is truly optional.
    cache_ttl = config.get("cache", {}).get("ttl")
    print(f"cache ttl (optional section) = {cache_ttl}")

    # Updating one nested value: the inner dict is mutable, so this is direct.
    config["server"]["port"] = 8080
    print(f"server now {config['server']}")

    production = {"server": {"host": "example.org"}, "database": {"pool": {"max": 50}}}
    merged = deep_merge(config, production)
    print(f"deep_merge server   = {merged['server']}")
    print(f"deep_merge database = {merged['database']}")
    # Sections that were not overridden are still shared with config. For a
    # fully independent copy use copy.deepcopy (see copying_and_references.py).


def main() -> None:
    views_demo()
    print()
    order_demo()
    print()
    merge_demo()
    print()
    reshape_demo()
    print()
    nested_demo()


if __name__ == "__main__":
    main()
