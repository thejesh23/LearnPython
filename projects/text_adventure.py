"""Project: a small text adventure game.

You build it in four steps:

    1. the world     rooms, exits and items described as plain data, then
                     checked so a typo in an exit name is caught at start-up
    2. the parser    turn typed text into a Command with a match statement
    3. the game      move between rooms, pick things up, carry an inventory,
                     open a locked door, see nothing in the dark without a lamp
    4. winning       escape with the crown; the demo plays a scripted
                     walkthrough, `python text_adventure.py --play` lets you type

Keeping the world as data and the rules as code means you can design a new
adventure by editing only the ROOMS dict.

Uses:
    04_strings             split, join, lower
    05_control_flow        match statements with guards and captures
    07_collections         dicts, lists, copy.deepcopy
    09_classes             dataclasses, class patterns in match
"""

import copy
from dataclasses import dataclass, field


ROOMS = {
    "hall": {
        "description": "A dusty entrance hall. The front door creaks in the wind.",
        "exits": {"north": "library", "east": "kitchen", "down": "cellar"},
        "items": [],
    },
    "kitchen": {
        "description": "A cold kitchen that smells of old soup.",
        "exits": {"west": "hall"},
        "items": ["lamp", "spoon"],
    },
    "library": {
        "description": "Shelves of mouldy books. A ladder leads up to a trapdoor.",
        "exits": {"south": "hall", "up": "tower"},
        "items": ["book"],
        "locked": {"up": "brass key"},  # exit -> item that unlocks it
    },
    "cellar": {
        "description": "A damp cellar full of broken barrels.",
        "exits": {"up": "hall"},
        "items": ["brass key"],
        "dark": True,
    },
    "tower": {
        "description": "A round tower room. Moonlight falls on a velvet cushion.",
        "exits": {"down": "library"},
        "items": ["crown"],
    },
}


@dataclass
class Room:
    name: str
    description: str
    exits: dict[str, str]
    items: list[str] = field(default_factory=list)
    locked: dict[str, str] = field(default_factory=dict)
    dark: bool = False


def build_world(data: dict[str, dict]) -> dict[str, Room]:
    # deepcopy so a game that moves items around never edits ROOMS itself;
    # every new game then starts from the same untouched world.
    world = {name: Room(name, **copy.deepcopy(spec)) for name, spec in data.items()}
    for room in world.values():
        for direction, target in room.exits.items():
            if target not in world:
                raise ValueError(f"{room.name}: exit {direction} -> unknown {target!r}")
    return world


def world_demo() -> None:
    world = build_world(ROOMS)
    for room in world.values():
        notes = ["dark" if room.dark else "", "locked" if room.locked else ""]
        extra = ", ".join(n for n in notes if n)
        print(f"{room.name:<8} exits {sorted(room.exits)} {extra}".rstrip())
    try:
        build_world({"hall": {"description": "", "exits": {"north": "nowhere"}}})
    except ValueError as exc:
        print(f"ValueError: {exc}")


def main() -> None:
    world_demo()


if __name__ == "__main__":
    main()
