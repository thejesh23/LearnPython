"""EAFP versus LBYL — two ways to deal with things that might not work.

    LBYL  "Look Before You Leap": check first, then act.
          if key in d: value = d[key]
    EAFP  "Easier to Ask Forgiveness than Permission": just act, and handle
          the exception if it fails.
          try: value = d[key]  except KeyError: ...

Python leans towards EAFP. The check-then-act style has a hidden flaw: the
world can change between the check and the act (another thread, another
process, the user deleting a file), so the check proves nothing. EAFP does
the operation once and reacts to what actually happened.

But EAFP is not always better. LBYL wins when failure is the *common* case
(exceptions cost more than an `if`), when the action is expensive or cannot
be undone halfway, and when a broad `try` would hide unrelated bugs. Both
styles belong in your toolbox; this file shows when to reach for which.
"""


def price_lbyl(prices: dict[str, float], item: str) -> float | None:
    if item in prices:  # look...
        return prices[item]  # ...then leap: a second lookup
    return None


def price_eafp(prices: dict[str, float], item: str) -> float | None:
    try:
        return prices[item]  # one lookup
    except KeyError:
        return None


def two_styles_demo() -> None:
    prices = {"tea": 2.5, "cake": 3.0}
    for item in ("tea", "soup"):
        lbyl, eafp = price_lbyl(prices, item), price_eafp(prices, item)
        print(f"{item}: lbyl={lbyl} eafp={eafp}")
    # For this exact case, Python has a third, best way: a method that already
    # handles "missing" for you.
    print(f"soup with .get(): {prices.get('soup', 0.0)}")

    # The same idea with attributes: hasattr() versus try/except.
    class Cat:
        def speak(self) -> str:
            return "meow"

    class Rock:
        pass

    for thing in (Cat(), Rock()):
        try:
            said = thing.speak()  # type: ignore[attr-defined]
        except AttributeError:
            said = "(silence)"
        print(f"{type(thing).__name__}: {said}")


def main() -> None:
    two_styles_demo()


if __name__ == "__main__":
    main()
