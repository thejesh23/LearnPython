"""`pickle` — save almost any Python object, and why never to load a stranger's.

`json` handles dicts, lists, strings and numbers. `pickle` goes much further:
tuples stay tuples, sets stay sets, and instances of your own classes come
back as instances. It does this by writing down *instructions for rebuilding
the object*, and `pickle.loads` follows those instructions.

That is also the danger. A pickle can say "to rebuild me, call this function
with these arguments", and the function can be anything, including one that
deletes files. Loading a pickle runs code chosen by whoever made it, so:

    pickle   only for data you created yourself and stored somewhere safe
    json     for anything that crosses a trust boundary: files from users,
             network messages, data shared with other programs or languages

`shelve`, at the end, is a dict that lives on disk and pickles its values.
"""

import pickle
import pickletools
import tempfile
import threading
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class Task:
    title: str
    due: date
    tags: set[str]


def round_trip_demo() -> None:
    data = {
        "point": (3, 4),                      # a tuple, not a list
        "seen": {"a", "b"},                    # a set
        "task": Task("file taxes", date(2026, 4, 15), {"home"}),
    }
    blob = pickle.dumps(data)  # bytes, not text
    print(f"pickled into {len(blob)} {type(blob).__name__}")

    back = pickle.loads(blob)
    print(f"equal after the round trip: {back == data}")
    print(f"types kept: {type(back['point']).__name__}, "
          f"{type(back['seen']).__name__}, {type(back['task']).__name__}")
    print(f"a new object, not the same one: {back['task'] is not data['task']}")

    # dump/load work with files. Pickles are binary: open with "wb" and "rb".
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "tasks.pickle"
        with path.open("wb") as f:
            pickle.dump(data["task"], f)
        with path.open("rb") as f:
            task = pickle.load(f)
        print(f"from the file: {task.title!r} due {task.due}")


def unpicklable_demo() -> None:
    # Pickle records functions and classes by *name* ("module.qualname"),
    # so they must be importable when loading. A lambda has no usable name.
    same = pickle.loads(pickle.dumps(len)) is len
    print(f"len is saved as the name 'builtins.len' and found again: {same}")

    with tempfile.TemporaryFile() as handle:
        things = {
            "lambda": (lambda x: x + 1, "has no name to import it by"),
            "generator": ((n for n in range(3)), "its paused state is not saved"),
            "open file": (handle, "belongs to this running process"),
            "lock": (threading.Lock(), "belongs to this running process"),
        }
        for label, (thing, reason) in things.items():
            try:
                pickle.dumps(thing)
            except (pickle.PicklingError, TypeError, AttributeError) as exc:
                # The exact exception type differs between Python versions.
                print(f"  {label:<10} {type(exc).__name__:<14} {reason}")
    # Files, locks and network connections belong to the running process;
    # there is nothing meaningful to write down. Save their settings instead.


class Sneaky:
    """An object whose pickle says: "to rebuild me, call print(...)"."""

    def __reduce__(self) -> tuple:
        # pickle stores this callable and its arguments, and loads() calls it.
        # A real attacker would return (os.system, ("some command",)).
        return (print, ("  !! this line was printed by pickle.loads !!",))


def danger_demo() -> None:
    blob = pickle.dumps(Sneaky())
    # Disassembling shows that a pickle is a little program, not just data:
    # push 'builtins' and 'print', look the function up, then call it (REDUCE).
    print("the pickle's instructions:")
    for op, arg, _ in pickletools.genops(blob):
        if op.name not in ("PROTO", "FRAME", "MEMOIZE", "STOP"):
            print(f"  {op.name:<18} {'' if arg is None else repr(arg)}".rstrip())

    print("now loading it:")
    result = pickle.loads(blob)  # calls print; it does not rebuild a Sneaky
    print(f"loads returned {result!r}, not a Sneaky object")
    # Nothing in the file name or size warns you. Checking it "looks okay"
    # is not enough: only unpickle data that you wrote yourself.


def main() -> None:
    round_trip_demo()
    print()
    unpicklable_demo()
    print()
    danger_demo()


if __name__ == "__main__":
    main()
